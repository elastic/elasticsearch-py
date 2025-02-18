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

import datetime

import elasticsearch

extensions = ["sphinx.ext.autodoc", "sphinx.ext.doctest", "sphinx.ext.intersphinx"]

autoclass_content = "class"
autodoc_class_signature = "separated"

autodoc_typehints = "description"


def client_name(full_name):
    # Get the class name, e.g. ['elasticsearch', 'client', 'TextStructureClient'] -> 'TextStructure'
    class_name = full_name.split(".")[-1].removesuffix("Client")
    # Convert to snake case, e.g. 'TextStructure' -> '_text_structure'
    snake_case = "".join(["_" + c.lower() if c.isupper() else c for c in class_name])
    # Remove the leading underscore
    return snake_case.lstrip("_")


def add_client_usage_example(app, what, name, obj, options, lines):
    if what == "class" and "Client" in name:
        sub_client_name = client_name(name)
        lines.append(
            f"To use this client, access ``client.{sub_client_name}`` from an "
            " :class:`~elasticsearch.Elasticsearch` client. For example::"
        )
        lines.append("")
        lines.append("    from elasticsearch import Elasticsearch")
        lines.append("")
        lines.append("    # Create the client instance")
        lines.append("    client = Elasticsearch(...)")
        lines.append(f"    # Use the {sub_client_name} client")
        lines.append(f"    client.{sub_client_name}.<method>(...)")
        lines.append("")


def setup(app):
    app.connect("autodoc-process-docstring", add_client_usage_example)


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "Python Elasticsearch client"
copyright = "%d, Elasticsearch B.V" % datetime.date.today().year

version = elasticsearch.__versionstr__
release = version

pygments_style = "sphinx"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "elastic-transport": (
        "https://elastic-transport-python.readthedocs.io/en/latest",
        None,
    ),
}
