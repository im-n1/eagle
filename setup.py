#!/usr/bin/env python3

import setuptools
from eagle.meta import CONFIG


# Long description
with open("README.rst", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="eagle-cli",
    version=CONFIG["version"],
    description=CONFIG["description"],
    long_description=long_description,
    author="n1",
    url="https://gitlab.com/n1_/eagle",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["eagle = eagle.eagle:eagle"]},
    python_requires=">=3.6",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business :: Scheduling ",
    ],
)
