# {dist}-{version}(-{build})?-{python}-{abi}-{platform}.whl
#
# Durante el desarrollo:
#   pip install -e .
#
# Para generar el wheel
#   python setup.py bdist_wheel
#   pip install dist/lge-X.Y.Z-py3-none-any.whl

from setuptools import setup
import sys

SETUP = {
    "name"             : "lge",
    "version"          : "0.1.0-pre.1",
    "description"      : "Little Game engine",
    "license"          : "MIT",
    "author"           : "Roberto Carrasco",
    "author_email"     : "titos.carrasco@gmail.com",
    "maintainer"       : "Roberto Carrasco",
    "maintainer_email" : "titos.carrasco@gmail.com",
    "packages"         : [ "lge" ],
    "package_dir"      : { "lge": "lge"},
}

setup( **SETUP )
