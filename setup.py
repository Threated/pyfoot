import setuptools
from .__init__ import __doc__ as desc

setuptools.setup(
    name="pyfoot",
    version="0.1.1",
    description=desc,
    packages=setuptools.find_packages()
)