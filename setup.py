#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name="eagle",
    version=0.1,
    description="Simple TODO tool for CLI.",
    author="n1",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["eagle = eagle.eagle:eagle"]
    },
    python_requires=">=3.6",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
    ]
)
