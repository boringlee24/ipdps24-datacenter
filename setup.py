from setuptools import setup, find_packages
import os
import re

def get_requirements(path: str):
    return [l.strip() for l in open(path)]

here = os.path.realpath(os.path.dirname(__file__))
with open(os.path.join(here, "mining_utils", "__init__.py")) as f:
    meta_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if meta_match:
        version = meta_match.group(1)
    else:
        raise RuntimeError("Unable to find `__version__`.")

setup(
    name='mining_utils',
    version=version,
    packages=find_packages(),
    description='A utility package for association rule mining',
    install_requires=get_requirements("requirements.txt"),
)
