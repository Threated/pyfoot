import setuptools
from __init__ import __doc__ as desc

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfoot",
    version="0.0.1",
    description=desc,
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Threated/pyfoot",
    author="Jan Skiba",
    author_email="jan2001.07@gmail.com",
    python_requires=">=3.6",
    intall_requires=[
        "pygame"
    ]
)
