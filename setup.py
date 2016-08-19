#-*- coding: utf-8 -*-

from setuptools import setup, find_packages


def get_long_description_from_file():
    # content of README will be the long description

    fname = 'README'
    with open(fname) as f:
        fcontent = f.read()
    return fcontent


DESCRIPTION = """
Signals with coroutines!
"""
LONG_DESCRIPTION = get_long_description_from_file()

setup(name='asyncblink',
      version='0.2',
      author='Juca Crispim',
      author_email='juca@poraodojuca.net',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url='https://pypi.python.org/pypi/asyncblink',
      py_modules=['asyncblink'],
      install_requires=['blinker>=1.3'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      test_suite='tests',
      provides=['asyncblink'])
