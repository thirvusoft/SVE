from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sve/__init__.py
from sve import __version__ as version

setup(
	name="sve",
	version=version,
	description="Sri Venkatesa Enterprises",
	author="info@thirvusoft.in",
	author_email="info@thirvusoft.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
