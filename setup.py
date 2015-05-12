# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import antiweb
import os.path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requires = ['Sphinx>=0.6']

setup(
    name='antiweb',
    version=antiweb.__version__,
    url='http://packages.python.org/antiweb/',
    download_url='http://pypi.python.org/pypi/antiweb',
    license='GPL',
    author='Michael Reithinger',
    author_email='mreithinger@web.de',
    description='antiweb literate programming tool',
    long_description=read(os.path.join("doc", "source", "motivation.rst")),
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
)
