import setuptools
from __init__ import __doc__ as desc

setuptools.setup(
    name="pyfoot",
    version="0.1.1",
    description=desc,
    packages=setuptools.find_packages(),
    url="https://github.com/Threated/pyfoot",
    author="Jan Skiba",
    author_email="jan2001.07@gmail.com",
    python_requires=">=3.6",
    intall_requires=[
        "pygame"
    ]
)