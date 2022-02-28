#!/usr/bin/env python
"""Setup script fo installing the fifipy library."""

from distutils.core import setup

config = {
    'name': 'fififly',
    'version': '1.0.29',
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
    'package_data': {'fififly': ['data/*png','version.json'],
                     'fififly.scanmaker':['data/*txt','greenstylesheet.css',
                                          'icons/*png','copyright.txt']}
    'install_requires': ['numpy', 'matplotlib', 'astropy']
}

setup(**config)
