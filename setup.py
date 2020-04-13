import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

desc = "A simple simple and beginner friendly library for writing 2D games based on pygame and inspired by Greenfoot"

setuptools.setup(
    name="pyfoot",
    version="0.1.3",
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=("tests",)),
    url="https://github.com/Threated/pyfoot",
    author="Jan Skiba",
    author_email="jan2001.07@gmail.com",
    python_requires=">=3.6",
    install_requires=[
        "pygame"
    ],
    license="GNU 3",
    include_package_data=True
)
