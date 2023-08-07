#!/usr/bin/python3
from setuptools import setup

NAME = "crossover"
EMAIL = "contact@checkfirst.network"
AUTHOR = "CheckFirst OY"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "1.0.0"

REQUIRED = [
    "argparse",
    "datetime",
	"requests",
	"beautifulsoup4",
    "unidecode",
    "selenium",
    "youtube_dl"
]

setup(
	name=NAME,
    version=VERSION,
	author=AUTHOR,
	author_email=EMAIL,
	python_requires=REQUIRES_PYTHON,
	packages=['crossover'],
	entry_points={
		'console_scripts':[
			'crossover = crossover.crossover:__callMe__',
		],
	},
	install_requires=REQUIRED
)