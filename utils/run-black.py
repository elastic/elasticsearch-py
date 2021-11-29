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

import os
import re
import subprocess
import sys
import time


def sleep_if_hot() -> None:
    def is_hot() -> bool:
        try:
            return (
                max(
                    map(
                        int,
                        re.findall(
                            r"\s\+([0-9]{2})\.[0-9]",
                            subprocess.check_output(
                                "sensors",
                                shell=True,
                                stderr=subprocess.STDOUT,
                            ).decode("utf-8"),
                        ),
                    )
                )
                > 80
            )
        except subprocess.CalledProcessError:
            return False

    while is_hot():
        time.sleep(0.1)


def run_on_directory(dir: str, check: bool) -> None:
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".py") or filename.endswith(".pyi"):
                run_on_file(os.path.join(root, filename), check)


def run_on_file(file: str, check: bool) -> None:
    try:
        subprocess.check_call(
            f"black --target-version=py36 {'--check ' if check else ''}{file}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        print(e.output)
        exit(e.returncode)
    sleep_if_hot()


def main() -> None:
    cwd = os.getcwd()
    check = ["--check"] == sys.argv[1:2]
    targets = [
        os.path.expanduser(os.path.join(cwd, target))
        for target in sys.argv[1:]
        if target != "--check"
    ]
    for target in targets:
        if os.path.isdir(target):
            run_on_directory(target, check)
        else:
            run_on_file(target, check)


if __name__ == "__main__":
    main()
