# -*- coding: utf-8 -*-

__author__ = "Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, and Christian Eitner"
__copyright__ = "Copyright 2017, antiweb team"
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "antiweb team"
__email__ = "antiweb@freelists.org"

from setuptools import setup, find_packages
import os.path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requires = ['Sphinx', 'babel', 'beautifulsoup4', 'watchdog', 'Pygments>=2.2.0']

setup(
    name='antiweb',
    version='0.9.1',
    url='https://github.com/7enderhead/antiweb',
    download_url='https://github.com/7enderhead/antiweb',
    license='GPL',
    author='Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, Christian Eitner',
    author_email='antiweb@freelists.org',
    description='antiweb literate programming tool',
    install_requires=requires,
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    scripts=['antiweb.py'],
    py_modules=['antisphinx'],
    packages=find_packages(exclude=['tests']), 
)
