from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sri_venkatesa_enterprises/__init__.py
from sri_venkatesa_enterprises import __version__ as version

setup(
	name="sri_venkatesa_enterprises",
	version=version,
	description="Sri Venkatesa Enterprises",
	author="Thirvusoft",
	author_email="info@thirvusoft.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
