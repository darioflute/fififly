#!/usr/bin/env python
"""Setup script fo installing the fififly library."""

from distutils.core import setup
import json

with open('fififly/version.json') as fp:
    _info = json.load(fp)

config = {
    'name': 'fififly',
    'version': _info['version'],
    'description': 'FIFI-LS Python library',
    'long_description': 'Collection of programs to reduce FIFI-LS data',
    'author': 'Dario Fadda',
    'author_email': 'darioflute@gmail.com',
    'url': 'https://github.com/darioflute/fififly.git',
    'download_url': 'https://github.com/darioflute/fififly',
    'license': 'GPLv3+',
    'packages': ['fififly','fififly.scanmaker'],
    'scripts': ['bin/scanmaker'],
    'include_package_data': True,
    'package_data': {'fififly': ['data/*png','version.json','scanmaker/data/*txt','scanmaker/greenstylesheet.css','scanmaker/icons/*png','scanmaker/copyright.txt']},
    'install_requires': ['numpy', 'matplotlib', 'astropy']
}

setup(**config)
