# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os.path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requires = ['Sphinx', 'babel', 'beautifulsoup4', 'watchdog', 'Pygments>=2.2.0']

setup(
    name='antiweb',
    version='0.9.0',
    url='http://packages.python.org/antiweb/',
    download_url='http://pypi.python.org/pypi/antiweb',
    license='GPL',
    author='Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, Christian Eitner',
    author_email='antiweb@freelists.org',
    description='antiweb literate programming tool',
    install_requires=requires,
    #long_description=read(os.path.join("doc_old", "source", "motivation.rst")),
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
