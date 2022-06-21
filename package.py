name = "studiolibrary"

# NOTE: <external_version>.sse.<internal_version>
version = "2.9.6.b1.sse.1.2.0"

authors = [
    "Kurt Rathjen"
]

description = \
    """
    Studio Library is a python-based Qt tool for managing poses and animation in Maya.
    """

with scope("config") as c:
    # Determine location to release: internal (int) vs external (ext)

    # NOTE: Modify this variable to reflect the current package situation
    release_as = "ext"

    # The `c` variable here is actually rezconfig.py
    # `release_packages_path` is a variable defined inside rezconfig.py

    import os
    if release_as == "int":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_INT"]
    elif release_as == "ext":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

requires = [
    "maya",
    "sse_asset_manager",
]

private_build_requires = [
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7"]
]

build_command = "rez python {root}/rez_build.py"

# NOTE: To build a Python-based package with symlink to the source,
# use: rez-build -i --symlink 1

uuid = "repository.studiolibrary"

def commands():
    env.REZ_STUDIOLIBRARY_ROOT = "{root}"
    env.PYTHONPATH.append("{root}/src")

    # TODO: Neil, this config.json doesn't exist anymore, but you can create
    # a new one based on src/studiolibrary/config/default.json
    # Look into config/readme.md for more details.
    #env.STUDIO_LIBRARY_CONFIG_PATH = "{root}/config.json"

    # For any MEL/Python scripts that we want to make available at startup
    env.PYTHONPATH.append("{root}/startup")
    env.MAYA_SCRIPT_PATH.append("{root}/startup")
