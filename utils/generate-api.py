#!/usr/bin/env python
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from functools import lru_cache
from itertools import chain
from pathlib import Path

import black
import unasync
import urllib3
from click.testing import CliRunner
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

http = urllib3.PoolManager()

# line to look for in the original source file
SEPARATOR = "    # AUTO-GENERATED-API-DEFINITIONS #"
# global substitutions for python keywords
SUBSTITUTIONS = {"type": "doc_type", "from": "from_"}
# api path(s)
BRANCH_NAME = "master"
CODE_ROOT = Path(__file__).absolute().parent.parent
GLOBAL_QUERY_PARAMS = {
    "pretty": "Optional[bool]",
    "human": "Optional[bool]",
    "error_trace": "Optional[bool]",
    "format": "Optional[str]",
    "filter_path": "Optional[Union[str, Collection[str]]]",
    "request_timeout": "Optional[Union[int, float]]",
    "ignore": "Optional[Union[int, Collection[int]]]",
    "opaque_id": "Optional[str]",
    "http_auth": "Optional[Union[str, Tuple[str, str]]]",
    "api_key": "Optional[Union[str, Tuple[str, str]]]",
}

jinja_env = Environment(
    loader=FileSystemLoader([CODE_ROOT / "utils" / "templates"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def blacken(filename):
    runner = CliRunner()
    result = runner.invoke(black.main, [str(filename)])
    assert result.exit_code == 0, result.output


@lru_cache()
def is_valid_url(url):
    return 200 <= http.request("HEAD", url).status < 400


class Module:
    def __init__(self, namespace, is_pyi=False):
        self.namespace = namespace
        self.is_pyi = is_pyi
        self._apis = []
        self.parse_orig()

        if not is_pyi:
            self.pyi = Module(namespace, is_pyi=True)
            self.pyi.orders = self.orders[:]

    def add(self, api):
        self._apis.append(api)

    def parse_orig(self):
        self.orders = []
        self.header = "class C:"
        if os.path.exists(self.filepath):
            with open(self.filepath) as f:
                content = f.read()
                header_lines = []
                for line in content.split("\n"):
                    header_lines.append(line)
                    if line == SEPARATOR:
                        break
                # no separator found
                else:
                    header_lines = []
                    for line in content.split("\n"):
                        header_lines.append(line)
                        if line.startswith("class"):
                            break
                self.header = "\n".join(header_lines)
                self.orders = re.findall(
                    r"\n    (?:async )?def ([a-z_]+)\(", content, re.MULTILINE
                )

    def _position(self, api):
        try:
            return self.orders.index(api.name)
        except ValueError:
            return len(self.orders)

    def sort(self):
        self._apis.sort(key=self._position)

    def dump(self):
        self.sort()
        with open(self.filepath, "w") as f:
            f.write(self.header)
            for api in self._apis:
                f.write(api.to_python())

        if not self.is_pyi:
            self.pyi.dump()

    @property
    def filepath(self):
        return (
            CODE_ROOT
            / f"elasticsearch/_async/client/{self.namespace}.py{'i' if self.is_pyi else ''}"
        )


class API:
    def __init__(self, namespace, name, definition, is_pyi=False):
        self.namespace = namespace
        self.name = name
        self.is_pyi = is_pyi

        # overwrite the dict to maintain key order
        definition["params"] = {
            SUBSTITUTIONS.get(p, p): v for p, v in definition.get("params", {}).items()
        }

        self._def = definition
        self.description = ""
        self.doc_url = ""
        self.stability = self._def.get("stability", "stable")

        if isinstance(definition["documentation"], str):
            self.doc_url = definition["documentation"]
        else:
            # set as attribute so it may be overriden by Module.add
            self.description = (
                definition["documentation"].get("description", "").strip()
            )
            self.doc_url = definition["documentation"].get("url", "")

        # Filter out bad URL refs like 'TODO'
        # and serve all docs over HTTPS.
        if self.doc_url:
            if not self.doc_url.startswith("http"):
                self.doc_url = ""
            if self.doc_url.startswith("http://"):
                self.doc_url = self.doc_url.replace("http://", "https://")

            # Try setting doc refs like 'current' and 'master' to our branches ref.
            if BRANCH_NAME is not None:
                revised_url = re.sub(
                    "/elasticsearch/reference/[^/]+/",
                    f"/elasticsearch/reference/{BRANCH_NAME}/",
                    self.doc_url,
                )
                if is_valid_url(revised_url):
                    self.doc_url = revised_url
                else:
                    print(f"URL {revised_url!r}, falling back on {self.doc_url!r}")

    @property
    def all_parts(self):
        parts = {}
        for url in self._def["url"]["paths"]:
            parts.update(url.get("parts", {}))

        for p in parts:
            parts[p]["required"] = all(
                p in url.get("parts", {}) for url in self._def["url"]["paths"]
            )
            parts[p]["type"] = "Any"

        for k, sub in SUBSTITUTIONS.items():
            if k in parts:
                parts[sub] = parts.pop(k)

        dynamic, components = self.url_parts

        def ind(item):
            try:
                return components.index(item[0])
            except ValueError:
                return len(components)

        parts = dict(sorted(parts.items(), key=ind))
        return parts

    @property
    def params(self):
        parts = self.all_parts
        params = self._def.get("params", {})
        return chain(
            ((p, parts[p]) for p in parts if parts[p]["required"]),
            (("body", self.body),) if self.body else (),
            (
                (p, parts[p])
                for p in parts
                if not parts[p]["required"] and p not in params
            ),
            sorted(params.items(), key=lambda x: (x[0] not in parts, x[0])),
        )

    @property
    def body(self):
        b = self._def.get("body", {})
        if b:
            b.setdefault("required", False)
        return b

    @property
    def query_params(self):
        return (
            k
            for k in sorted(self._def.get("params", {}).keys())
            if k not in self.all_parts
        )

    @property
    def all_func_params(self):
        """Parameters that will be in the '@query_params' decorator list
        and parameters that will be in the function signature.
        This doesn't include
        """
        params = list(self._def.get("params", {}).keys())
        for url in self._def["url"]["paths"]:
            params.extend(url.get("parts", {}).keys())
        if self.body:
            params.append("body")
        return params

    @property
    def path(self):
        return max(
            (path for path in self._def["url"]["paths"]),
            key=lambda p: len(re.findall(r"\{([^}]+)\}", p["path"])),
        )

    @property
    def method(self):
        # To adhere to the HTTP RFC we shouldn't send
        # bodies in GET requests.
        default_method = self.path["methods"][0]
        if self.body and default_method == "GET" and "POST" in self.path["methods"]:
            return "POST"
        return default_method

    @property
    def url_parts(self):
        path = self.path["path"]

        dynamic = "{" in path
        if not dynamic:
            return dynamic, path

        parts = []
        for part in path.split("/"):
            if not part:
                continue

            if part[0] == "{":
                part = part[1:-1]
                parts.append(SUBSTITUTIONS.get(part, part))
            else:
                parts.append(f"'{part}'")

        return dynamic, parts

    @property
    def required_parts(self):
        parts = self.all_parts
        required = [p for p in parts if parts[p]["required"]]
        if self.body.get("required"):
            required.append("body")
        return required

    def to_python(self):
        if self.is_pyi:
            t = jinja_env.get_template("base_pyi")
        else:
            try:
                t = jinja_env.get_template(f"overrides/{self.namespace}/{self.name}")
            except TemplateNotFound:
                t = jinja_env.get_template("base")

        return t.render(
            api=self,
            substitutions={v: k for k, v in SUBSTITUTIONS.items()},
            global_query_params=GLOBAL_QUERY_PARAMS,
        )


@contextlib.contextmanager
def download_artifact(version):
    # Download the list of all artifacts for a version
    # and find the latest build URL for 'rest-resources-zip-*.zip'
    resp = http.request(
        "GET", f"https://artifacts-api.elastic.co/v1/versions/{version}"
    )
    packages = json.loads(resp.data)["version"]["builds"][0]["projects"][
        "elasticsearch"
    ]["packages"]
    for package in packages:
        if re.match(r"^rest-resources-zip-.*\.zip$", package):
            zip_url = packages[package]["url"]
            break
    else:
        raise RuntimeError(
            "Could not find the package 'rest-resources-zip-*.zip' in build"
        )

    # Download the .jar file and unzip only the API
    # .json files into a temporary directory
    resp = http.request("GET", zip_url)

    tmp = Path(tempfile.mkdtemp())
    zip = zipfile.ZipFile(io.BytesIO(resp.data))
    for name in zip.namelist():
        if not name.endswith(".json") or name == "schema.json":
            continue
        with (tmp / name.replace("rest-api-spec/api/", "")).open("wb") as f:
            f.write(zip.read(name))

    yield tmp
    shutil.rmtree(tmp)


def read_modules(version):
    modules = {}

    with download_artifact(version) as path:
        for f in sorted(os.listdir(path)):
            name, ext = f.rsplit(".", 1)

            if ext != "json" or name == "_common":
                continue

            with open(path / f) as api_def:
                api = json.load(api_def)[name]

            namespace = "__init__"
            if "." in name:
                namespace, name = name.rsplit(".", 1)

            # The data_frame API has been changed to transform.
            if namespace == "data_frame_transform_deprecated":
                continue

            if namespace not in modules:
                modules[namespace] = Module(namespace)

            modules[namespace].add(API(namespace, name, api))
            modules[namespace].pyi.add(API(namespace, name, api, is_pyi=True))

    return modules


def dump_modules(modules):
    for mod in modules.values():
        mod.dump()

    # Unasync all the generated async code
    additional_replacements = {
        # We want to rewrite to 'Transport' instead of 'SyncTransport', etc
        "AsyncTransport": "Transport",
        "AsyncElasticsearch": "Elasticsearch",
        # We don't want to rewrite this class
        "AsyncSearchClient": "AsyncSearchClient",
    }
    rules = [
        unasync.Rule(
            fromdir="/elasticsearch/_async/client/",
            todir="/elasticsearch/client/",
            additional_replacements=additional_replacements,
        ),
    ]

    filepaths = []
    for root, _, filenames in os.walk(CODE_ROOT / "elasticsearch/_async"):
        for filename in filenames:
            if (
                filename.rpartition(".")[-1]
                in (
                    "py",
                    "pyi",
                )
                and not filename.startswith("utils.py")
            ):
                filepaths.append(os.path.join(root, filename))

    unasync.unasync_files(filepaths, rules)
    blacken(CODE_ROOT / "elasticsearch")


if __name__ == "__main__":
    version = sys.argv[1]
    dump_modules(read_modules(version))
