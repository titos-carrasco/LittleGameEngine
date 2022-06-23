# {dist}-{version}(-{build})?-{python}-{abi}-{platform}.whl
#
# Durante el desarrollo:
#   pip install -e .
#
# Para generar el wheel
#   python setup.py bdist_wheel
#   pip install dist/lge-X.Y.Z-py3-none-any.whl

from setuptools import setup

SETUP = {
    "author": "Roberto Carrasco",
    "author_email": "titos.carrasco@gmail.com",
    "description": "Little Game engine",
    "license": "MIT",
    "maintainer": "Roberto Carrasco",
    "maintainer_email": "titos.carrasco@gmail.com",
    "name": "lge",
    "package_dir": {"": "src/rcr"},
    "packages": ["lge"],
    "version": "0.7.1",
}

setup(**SETUP)
