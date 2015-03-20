#-*- coding: utf-8 -*-

from setuptools import setup, find_packages


def get_long_description_from_file():
    # content of README will be the long description

    fname = 'README'
    with open(fname) as f:
        fcontent = f.read()
    return fcontent


DESCRIPTION = """
MongoMotor: An async document-object mapper for MongoDB
"""
LONG_DESCRIPTION = get_long_description_from_file()

setup(name='asyncblink',
      version='0.1',
      author='Juca Crispim',
      author_email='juca@poraodojuca.net',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url='https://testpypi.python.org/pypi/asyncblink',
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=['blinker>=1.3'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      test_suite='tests',
      provides=['asyncblink'])
