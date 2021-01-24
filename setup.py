import setuptools
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = re.sub(r':.*:', '', long_description)  # remove Github emojis

setuptools.setup(
    name="hun-date-parser",
    version="0.0.4",
    author="Soma Nagy",
    author_email="nagysomabalint@gmail.com",
    description="A tool for extracting datetime intervals from Hungarian sentences and turning datetime objects into Hungarian text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/szegedai/hun-date-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
