#!/usr/bin/env python
"""Setup script fo installing the fififly library."""

from distutils.core import setup

config = {
    'name': 'fififly',
    'version': '0.1',
    'description': 'FIFI-LS flight Python library',
    'long_description': 'Collection of programs to prepare FIFI-LS data',
    'author': 'Dario Fadda',
    'author_email': 'darioflute@gmail.com',
    'url': 'https://github.com/darioflute/fififly.git',
    'download_url': 'https://github.com/darioflute/fififly',
    'license': 'GPLv3+',
    'packages': ['fififly'],
    'scripts': ['bin/scanmaker'],
    'include_package_data': True,
    'package_data': {'fifipy': ['test/*.aor','tes/*.misxml']},
    'install_requires': ['numpy', 'lxml', 'matplotlib', 'astropy']
}

setup(**config)
