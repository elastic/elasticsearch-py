#!/usr/bin/env python

import os
import json
import re
from itertools import chain

import black
from click.testing import CliRunner
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


# line to look for in the original source file
SEPARATOR = "    # AUTO-GENERATED-API-DEFINITIONS #"
# global substitutions for python keywords
SUBSTITUTIONS = {"type": "doc_type", "from": "from_"}
# api path(s)
CODE_ROOT = Path(__file__).absolute().parent.parent
BASE_PATH = (
    CODE_ROOT.parent
    / "elasticsearch"
    / "rest-api-spec"
    / "src"
    / "main"
    / "resources"
    / "rest-api-spec"
    / "api"
)
XPACK_PATH = (
    CODE_ROOT.parent
    / "elasticsearch"
    / "x-pack"
    / "plugin"
    / "src"
    / "test"
    / "resources"
    / "rest-api-spec"
    / "api"
)

jinja_env = Environment(
    loader=FileSystemLoader([CODE_ROOT / "utils" / "templates"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def blacken(filename):
    runner = CliRunner()
    result = runner.invoke(black.main, [str(filename)])
    assert result.exit_code == 0, result.output


class Module:
    def __init__(self, namespace):
        self.namespace = namespace
        self._apis = []
        self.parse_orig()

    def add(self, api):
        self._apis.append(api)

    def parse_orig(self):
        self.orders = []
        self.header = "class C:"
        fname = CODE_ROOT / "elasticsearch" / "client" / f"{self.namespace}.py"
        if os.path.exists(fname):
            with open(fname) as f:
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
                defined_apis = re.findall(
                    r'\n    def ([a-z_]+)\([^\n]*\n *"""\n *([\w\W]*?)(?:`<|""")',
                    content,
                    re.MULTILINE,
                )
                self.orders = list(map(lambda x: x[0], defined_apis))

    def _position(self, api):
        try:
            return self.orders.index(api.name)
        except ValueError:
            return len(self.orders)

    def sort(self):
        self._apis.sort(key=self._position)

    def dump(self):
        self.sort()
        fname = CODE_ROOT / "elasticsearch" / "client" / f"{self.namespace}.py"
        with open(fname, "w") as f:
            f.write(self.header)
            for api in self._apis:
                f.write(api.to_python())
        blacken(fname)


class API:
    def __init__(self, namespace, name, definition):
        self.namespace = namespace
        self.name = name

        # overwrite the dict to maintain key order
        definition["params"] = {
            SUBSTITUTIONS.get(p, p): v for p, v in definition.get("params", {}).items()
        }

        self._def = definition
        self.description = ""
        self.doc_url = ""
        if isinstance(definition["documentation"], str):
            self.doc_url = definition["documentation"]
        else:
            # set as attribute so it may be overriden by Module.add
            self.description = definition["documentation"].get("description", "")
            self.doc_url = definition["documentation"].get("url", "")

    @property
    def all_parts(self):
        parts = {}
        for url in self._def["url"]["paths"]:
            parts.update(url.get("parts", {}))

        for p in parts:
            parts[p]["required"] = all(
                p in url.get("parts", {}) for url in self._def["url"]["paths"]
            )

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
        return chain(
            ((p, parts[p]) for p in parts if parts[p]["required"]),
            (("body", self.body), ) if self.body else (),
            ((p, parts[p]) for p in parts if not parts[p]["required"]),
            sorted(self._def.get("params", {}).items()),
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
    def path(self):
        return max(
            (path for path in self._def["url"]["paths"]),
            key=lambda p: len(re.findall(r"\{([^}]+)\}", p["path"])),
        )

    @property
    def method(self):
        return self.path["methods"][0]

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
        try:
            t = jinja_env.get_template(f"overrides/{self.namespace}/{self.name}")
        except TemplateNotFound:
            t = jinja_env.get_template("base")
        return t.render(
            api=self, substitutions={v: k for k, v in SUBSTITUTIONS.items()}
        )


def read_modules():
    modules = {}

    for path in (BASE_PATH, XPACK_PATH):
        for f in sorted(os.listdir(path)):
            name, ext = f.rsplit(".", 1)

            if ext != "json" or name == "_common":
                continue

            with open(path / f) as api_def:
                api = json.load(api_def)[name]

            namespace = "__init__"
            if "." in name:
                namespace, name = name.rsplit(".", 1)

            if namespace not in modules:
                modules[namespace] = Module(namespace)

            modules[namespace].add(API(namespace, name, api))

    return modules


def dump_modules(modules):
    for mod in modules.values():
        mod.dump()


if __name__ == "__main__":
    dump_modules(read_modules())
