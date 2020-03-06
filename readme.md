# Setting up Blender for Development with Engine

## Setting up pip

``` bash
# Navidate to blender's python directory. (Directory may be different.)
cd /c/Program Files/Blender Foundation/Blender 2.82/2.82/python/bin

# Acquire get-pip script.
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Install pip.
./python.exe get-pip.py

# Remove get-pip script.
rm get-pip.py

# Update pip and setuptools.
./python.exe -m pip install --upgrade pip setuptools
```

## Installing Mongodb

``` bash
# Navidate to blender's python directory. (Directory may be different.)
cd /c/Program Files/Blender Foundation/Blender 2.82/2.82/python/bin

# Install the fake blender API module.
./python.exe -m pip install fake-bpy-module-2.82

# Install pymongo.
./python.exe -m pip install pymongo
```

## VSCode Setup

``` bash
# Navidate to blender's python directory. (Directory may be different.)
cd /c/Program Files/Blender Foundation/Blender 2.82/2.82/python/bin

# Install the linter and formatter.
# (This will keep your existing linter and formatter safe.)
./python.exe -m pip install -U pylint autopep8
```

- Make sure that the `.vscode/settings.json` file's `python.pythonPath` and `python.autoComplete.extraPaths` values match the actual path of your blender installation.

## The initial addon setup

- See the `samples/the-initial-addon.py` file.
- At this point, it should not be announcing any syntax or formatting errors.
- 