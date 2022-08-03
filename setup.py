"""
Markata Slides uses setup tools for packaging.

To Build Markata Slides as a Python package

    $ python setup.py sdist bdist_wheel --bdist-dir ~/temp/bdistwheel

Regular install

    $ pip install -e .

To setup local Development

    $ pip install -e ".[dev]"

"""
from pathlib import Path
from typing import List

from setuptools import find_packages, setup

NAME = "markata_slides"

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")


def get_requirements(file: str) -> List[str]:
    """get the dependencies and installs"""
    with open("requirements.txt", encoding="utf-8") as f:
        # Make sure we strip all comments and options (e.g "--extra-index-url")
        # that arise from a modified pip.conf file that configure global options
        # when running kedro build-reqs
        requires = []
        for line in f:
            req = line.split("#", 1)[0].strip()
            if req and not req.startswith("--"):
                requires.append(req)
        return requires


requires = get_requirements("requirements.txt")
dev_requires = get_requirements("requirements_dev.txt")

with open("requirements_dev.txt", "r", encoding="utf-8") as f:
    dev_requires = [x.strip() for x in f if x.strip()]

setup(
    name=NAME,
    version="0.0.1",
    description="None",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    url="https://github.com/waylonwalker/Markata Slides",
    packages=find_packages(),
    platforms="any",
    license="OSI APPROVED :: MIT LICENSE",
    author="Waylon Walker",
    keywords="None",
    install_requires=requires,
    extras_require={"dev": dev_requires},
    entry_points={
        "console_scripts": ["markata-slides = markata_slides.cli:run"],
    },
)
