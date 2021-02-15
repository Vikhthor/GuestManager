# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in guest_manager/__init__.py
from guest_manager import __version__ as version

setup(
	name='guest_manager',
	version=version,
	description='Visitors Management Sysytem',
	author='Victor Maduforo',
	author_email='victor.maduforo@manqala.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
