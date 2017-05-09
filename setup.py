from setuptools import setup, find_packages

setup(
    name         = 'cookpad',
    version      = '1.1',
    packages     = find_packages(),
    install_requires=[
        'distribute',
        'scrapy',
        'psycopg2',
        'bs4',
        'pymongo',
		'pymssql'
    ],
    entry_points = {'scrapy': ['settings = cookpad.settings']},
    scripts = ['bin/testargs.py']
)