from setuptools import setup, find_packages

setup(
    name         = 'cookpad',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = cookpad.settings']},
    scripts = ['bin/testargs.py']
)