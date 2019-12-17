#!/usr/bin/env python

import os
import json
import re
from itertools import chain

import black
from click.testing import CliRunner
from pathlib import Path

from jinja2 import Environment, DictLoader, ChoiceLoader, TemplateNotFound


# line to look for in the original source file
SEPARATOR = "    # AUTO-GENERATED-API-DEFINITIONS #"
# global substitutions for python keywords
SUBSTITUTIONS = {"type": "doc_type", "from": "from_"}
# api path(s)
CODE_ROOT = Path(__file__).absolute().parent
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


BASE_TEMPLATES = {
    "url": """{% if api.url_parts.0 %}_make_path({{ api.url_parts.1|join(", ")}}){% else %}{{ api.url_parts.1|tojson }}{% endif %}""",
    "required": """{% if api.required_parts.1 %}
        for param in ({{ api.required_parts|join(", ")}}):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        {% elif api.required_parts %}
        if {{ api.required_parts.0 }} in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument '{{ api.required_parts.0 }}'.")

        {% endif %}""",
    "substitutions": """{% for p, info in api.params %}
        {% if p in substitutions and p not in api.url_parts.1 %}
        # {{ substitutions[p] }} is a reserved word so it cannot be used, use {{ p }} instead
        if "{{ p }}" in params:
            params["{{ substitutions[p] }}"] = params.pop("{{ p }}")

        {% endif %}
        {% endfor %}""",
    "base": '''
    @query_params({{ api.query_params|map("tojson")|join(", ")}})
    def {{ api.name }}(self, {{ api.func_params|join(", ") }}):
        """
        {% if api.description %}
        {{ api.description|replace("\n", " ")|wordwrap(wrapstring="\n        ") }}
        {% endif %}
        {% if api.doc_url %}
        `<{{ api.doc_url }}>`_
        {% endif %}
        {% if api.params %}

        {% for p, info in api.params %}
        {% filter wordwrap(72, wrapstring="\n            ") %}
        :arg {{ p }}: {{ info.description }} {% if info.options %}Valid choices: {{ info.options|join(", ") }}{% endif %} {% if info.default %}Default: {{ info.default }}{% endif %}
        {% endfilter %}

        {% endfor %}
        {% endif %}
        """
        {% include "substitutions" %}
        {% include "required" %}
        {% if api.body.body.serialize == "bulk" %}
        body = self._bulk_body(body)
        {% endif %}
        {% block request %}
        return self.transport.perform_request("{{ api.method }}", {% include "url" %}, params=params{% if api.body.body %}, body=body{% endif %})
        {% endblock %}
    ''',
}

OVERRIDE_TEMPLATES = {
    "__init__.ping": """
    {% extends "base" %}
    {% block request %}
        try:
            {{ super()|trim }}
        except TransportError:
            return False
    {% endblock %}
    """,
    "__init__.scroll": """
    {% extends "base" %}
    {% block request %}
        if scroll_id in SKIP_IN_PATH and body in SKIP_IN_PATH:
            raise ValueError("You need to supply scroll_id or body.")
        elif scroll_id and not body:
            body = {"scroll_id": scroll_id}
        elif scroll_id:
            params["scroll_id"] = scroll_id

        return self.transport.perform_request("{{ api.method }}", "/_search/scroll", params=params, body=body)
    {% endblock %}
    """,
    "__init__.clear_scroll": """
    {% extends "base" %}
    {% block request %}
        if scroll_id in SKIP_IN_PATH and body in SKIP_IN_PATH:
            raise ValueError("You need to supply scroll_id or body.")
        elif scroll_id and not body:
            body = {"scroll_id": [scroll_id]}
        elif scroll_id:
            params["scroll_id"] = scroll_id

        return self.transport.perform_request("{{ api.method }}", "/_search/scroll", params=params, body=body)
    {% endblock %}
    """,
}

jinja_env = Environment(
    loader=ChoiceLoader((DictLoader(OVERRIDE_TEMPLATES), DictLoader(BASE_TEMPLATES))),
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
        if api.name in self.descriptions and not api.description:
            api.description = self.descriptions[api.name]

    def parse_orig(self):
        self.descriptions = {}
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
                        if line.startswith('class'):
                            break
                self.header = "\n".join(header_lines)
                defined_apis = re.findall(
                    r'\n    def ([a-z_]+)\([^\n]*\n *"""\n *([\w\W]*?)(?:`<|""")',
                    content,
                    re.MULTILINE,
                )
                self.descriptions = dict(
                    map(lambda i: (i[0], i[1].strip()), defined_apis)
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

    def _all_parts(self):
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
        parts = self._all_parts()
        return chain(
            ((p, parts[p]) for p in parts if parts[p]["required"]),
            self.body.items() if self.body["body"] else (),
            ((p, parts[p]) for p in parts if not parts[p]["required"]),
            sorted(self._def.get("params", {}).items()),
        )

    @property
    def body(self):
        b = self._def.get("body", {})
        if b:
            b.setdefault("required", False)
        return {"body": b}

    @property
    def query_params(self):
        return sorted(self._def.get("params", {}).keys())

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
    def func_params(self):
        parts = self._all_parts()
        return chain(
            (p for p in parts if parts[p]["required"]),
            (b for b in self.body if self.body[b].get("required")),
            (f"{b}=None" for b in self.body if not self.body[b].get("required", True)),
            (f"{p}=None" for p in parts if not parts[p]["required"]),
            ("params=None",),
        )

    @property
    def required_parts(self):
        parts = self._all_parts()
        return [p for p in parts if parts[p]["required"]] + [
            b for b in self.body if self.body[b].get("required")
        ]

    def to_python(self):
        try:
            t = jinja_env.get_template(f"{self.namespace}.{self.name}")
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
