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

"""Command line tool which changes the branch to be
ready to build and test the given Elastic stack version.
"""

import re
import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).absolute().parent.parent


def find_and_replace(path, pattern, replace):
    # Does a find and replace within a file path and complains
    # if the given pattern isn't found in the file.
    with open(path) as f:
        old_data = f.read()

    if re.search(pattern, old_data, flags=re.MULTILINE) is None:
        print(f"Didn't find the pattern {pattern!r} in {path!s}")
        exit(1)

    new_data = re.sub(pattern, replace, old_data, flags=re.MULTILINE)
    with open(path, "w") as f:
        f.truncate()
        f.write(new_data)


def main():
    if len(sys.argv) != 2:
        print("usage: utils/bump-version.py [stack version]")
        exit(1)

    stack_version = sys.argv[1]
    try:
        python_version = re.search(r"^([0-9][0-9\.]*[0-9]+)", stack_version).group(1)
    except AttributeError:
        print(f"Couldn't match the given stack version {stack_version!r}")
        exit(1)

    # Pad the version value with .0 until there
    # we have the major, minor, and patch.
    for _ in range(3):
        if len(python_version.split(".")) >= 3:
            break
        python_version += ".0"

    find_and_replace(
        path=SOURCE_DIR / "elasticsearch/_version.py",
        pattern=r"__versionstr__ = \"[0-9]+[0-9\.]*[0-9](?:\+dev)?\"",
        replace=f'__versionstr__ = "{python_version}"',
    )

    # These values should always be the 'major.minor-SNAPSHOT'
    major_minor_version = ".".join(python_version.split(".")[:2])
    find_and_replace(
        path=SOURCE_DIR / ".buildkite/pipeline.yml",
        pattern=r'STACK_VERSION:\s+"[0-9]+[0-9\.]*[0-9](?:\-SNAPSHOT)?"',
        replace=f'STACK_VERSION: "{major_minor_version}.0-SNAPSHOT"',
    )


if __name__ == "__main__":
    main()
