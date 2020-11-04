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

"""A command line tool for building and verifying releases
Can be used for building both 'elasticsearch' and 'elasticsearchX' dists.
Only requires 'name' in 'setup.py' and the directory to be changed.
"""

import tempfile
import os
import shlex
import sys
import re
import contextlib
import shutil


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp_dir = None


@contextlib.contextmanager
def set_tmp_dir():
    global tmp_dir
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)
    tmp_dir = None


def run(*argv, expect_exit_code=0):
    global tmp_dir
    if tmp_dir is None:
        os.chdir(base_dir)
    else:
        os.chdir(tmp_dir)

    cmd = " ".join(shlex.quote(x) for x in argv)
    print("$ " + cmd)
    exit_code = os.system(cmd)
    if exit_code != expect_exit_code:
        print(
            "Command exited incorrectly: should have been %d was %d"
            % (expect_exit_code, exit_code)
        )
        exit(exit_code or 1)


def test_dist(dist):
    with set_tmp_dir() as tmp_dir:
        dist_name = re.match(r"^(elasticsearch\d*)-", os.path.basename(dist)).group(1)

        # Build the venv and install the dist
        run("python", "-m", "venv", os.path.join(tmp_dir, "venv"))
        venv_python = os.path.join(tmp_dir, "venv/bin/python")
        run(venv_python, "-m", "pip", "install", "-U", "pip", "mypy")
        run(venv_python, "-m", "pip", "install", dist)

        # Test the sync namespaces
        run(venv_python, "-c", f"from {dist_name} import Elasticsearch")
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import scan, bulk, streaming_bulk, reindex",
        )
        run(venv_python, "-c", f"from {dist_name} import Elasticsearch")
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import scan, bulk, streaming_bulk, reindex",
        )

        # Ensure that async is not available yet
        run(
            venv_python,
            "-c",
            f"from {dist_name} import AsyncElasticsearch",
            expect_exit_code=256,
        )
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import async_scan, async_bulk, async_streaming_bulk, async_reindex",
            expect_exit_code=256,
        )

        # Install aiohttp and see that async is now available
        run(venv_python, "-m", "pip", "install", "aiohttp")
        run(venv_python, "-c", f"from {dist_name} import AsyncElasticsearch")
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import async_scan, async_bulk, async_streaming_bulk, async_reindex",
        )

        # Only need to test 'async_types' for non-aliased package
        # since 'aliased_types' tests both async and sync.
        if dist_name == "elasticsearch":
            run(
                venv_python,
                "-m",
                "mypy",
                "--strict",
                os.path.join(base_dir, "test_elasticsearch/test_types/async_types.py"),
            )

        # Ensure that the namespaces are correct for the dist
        for suffix in ("", "1", "2", "5", "6", "7", "8", "9", "10"):
            distx_name = f"elasticsearch{suffix}"
            run(
                venv_python,
                "-c",
                f"import {distx_name}",
                expect_exit_code=256 if distx_name != dist_name else 0,
            )

        # Check that sync types work for 'elasticsearch' and
        # that aliased types work for 'elasticsearchX'
        if dist_name == "elasticsearch":
            run(
                venv_python,
                "-m",
                "mypy",
                "--strict",
                os.path.join(base_dir, "test_elasticsearch/test_types/sync_types.py"),
            )
        else:
            run(
                venv_python,
                "-m",
                "mypy",
                "--strict",
                os.path.join(
                    base_dir, "test_elasticsearch/test_types/aliased_types.py"
                ),
            )

        # Uninstall the dist, see that we can't import things anymore
        run(venv_python, "-m", "pip", "uninstall", "--yes", dist_name)
        run(
            venv_python,
            "-c",
            f"from {dist_name} import Elasticsearch",
            expect_exit_code=256,
        )


def main():
    run("git", "checkout", "--", "setup.py", "elasticsearch/")
    run("rm", "-rf", "build/", "dist/", "*.egg-info", ".eggs")

    # Grab the major version to be used as a suffix.
    version_path = os.path.join(base_dir, "elasticsearch/_version.py")
    with open(version_path) as f:
        version = re.search(
            r"^__versionstr__\s+=\s+[\"\']([^\"\']+)[\"\']", f.read(), re.M
        ).group(1)
    major_version = version.split(".")[0]

    # If we're handed a version from the build manager we
    # should check that the version is correct or write
    # a new one.
    if len(sys.argv) >= 2:
        # 'build_version' is what the release manager wants,
        # 'expect_version' is what we're expecting to compare
        # the package version to before building the dists.
        build_version = expect_version = sys.argv[1]

        # '-SNAPSHOT' means we're making a pre-release.
        if "-SNAPSHOT" in build_version:
            # If there's no +dev already (as is the case on dev
            # branches like 7.x, master) then we need to add one.
            if not version.endswith("+dev"):
                version = version + "+dev"
            expect_version = expect_version.replace("-SNAPSHOT", "")
            if expect_version.endswith(".x"):
                expect_version = expect_version[:-2]

            # For snapshots we ensure that the version in the package
            # at least *starts* with the version. This is to support
            # build_version='7.x-SNAPSHOT'.
            if not version.startswith(expect_version):
                print(
                    "Version of package (%s) didn't match the "
                    "expected release version (%s)" % (version, build_version)
                )
                exit(1)

        # A release that will be tagged, we want
        # there to be no '+dev', etc.
        elif expect_version != version:
            print(
                "Version of package (%s) didn't match the "
                "expected release version (%s)" % (version, build_version)
            )
            exit(1)

    for suffix in ("", major_version):
        run("rm", "-rf", "build/", "*.egg-info", ".eggs")

        # Rename the module to fit the suffix.
        shutil.move(
            os.path.join(base_dir, "elasticsearch"),
            os.path.join(base_dir, "elasticsearch%s" % suffix),
        )

        # Ensure that the version within 'elasticsearch/_version.py' is correct.
        version_path = os.path.join(base_dir, f"elasticsearch{suffix}/_version.py")
        with open(version_path) as f:
            version_data = f.read()
        version_data = re.sub(
            r"__versionstr__ = \"[^\"]+\"",
            '__versionstr__ = "%s"' % version,
            version_data,
        )
        with open(version_path, "w") as f:
            f.truncate()
            f.write(version_data)

        # Rewrite setup.py with the new name.
        setup_py_path = os.path.join(base_dir, "setup.py")
        with open(setup_py_path) as f:
            setup_py = f.read()
        with open(setup_py_path, "w") as f:
            f.truncate()
            assert 'package_name = "elasticsearch"' in setup_py
            f.write(
                setup_py.replace(
                    'package_name = "elasticsearch"',
                    'package_name = "elasticsearch%s"' % suffix,
                )
            )

        # Build the sdist/wheels
        run("python", "setup.py", "sdist", "bdist_wheel")

        # Clean up everything.
        run("git", "checkout", "--", "setup.py", "elasticsearch/")
        if suffix:
            run("rm", "-rf", "elasticsearch%s/" % suffix)

    # Test everything that got created
    dists = os.listdir(os.path.join(base_dir, "dist"))
    assert len(dists) == 4
    for dist in dists:
        test_dist(os.path.join(base_dir, "dist", dist))

    # After this run 'python -m twine upload dist/*'
    print(
        "\n\n"
        "===============================\n\n"
        "    * Releases are ready! *\n\n"
        "$ python -m twine upload dist/*\n\n"
        "==============================="
    )


if __name__ == "__main__":
    main()
