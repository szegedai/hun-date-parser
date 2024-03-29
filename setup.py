import pathlib

import pkg_resources
import setuptools
import re
import hun_date_parser

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = re.sub(r':.*:', '', long_description)  # remove Github emojis

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setuptools.setup(
    name="hun-date-parser",
    version=hun_date_parser.__version__,
    author="Soma Nagy",
    author_email="nagysomabalint@gmail.com",
    description="A tool for extracting datetime intervals from Hungarian sentences and turning datetime objects into Hungarian text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/szegedai/hun-date-parser",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
