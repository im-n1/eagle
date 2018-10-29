#!/usr/bin/env python3

import setuptools

with open("description.rst", "r") as f:
    description = f.read()

setuptools.setup(
    name="eagle-cli",
    version="0.1",
    # version="0.1-4",
    description="Simple TODO tool for CLI.",
    long_description=description,
    author="n1",
    url="https://gitlab.com/n1_/eagle",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["eagle = eagle.eagle:eagle"]
    },
    python_requires=">=3.6",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business :: Scheduling ",
    ]
)
