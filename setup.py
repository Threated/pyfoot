import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

desc = """
    Pyfoot
    ~~~~~~

    Pyfoot is a high-level library for writing simple 2d games.
    It is based upon the Python library pygame and was inspired by the java library Greenfoot.
    Most of the functions provided also accept pygame objects, which can provide more functionality.
    """

setuptools.setup(
    name="pyfoot",
    version="0.0.1",
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
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
