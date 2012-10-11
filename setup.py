# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

version = "0.3"

entry_point = 'buildout.sendpickedversions:install'
entry_points = {"zc.buildout.extension": ["default = %s" % entry_point]}
requires = ['setuptools', 'zc.buildout']

if sys.version[:3] < '2.6':
    requires.append('simplejson')

tests_require=['zc.buildout', 'zope.testing', 'zc.recipe.egg']

setup(name='buildout.sendpickedversions',
      version=version,
      description="Sends picked packages and versions to a whiskers server.",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      license='GPL',
      keywords='buildout extension send picked versions',
      author='Jukka Ojaniemi',
      author_email='jukka.ojaniemi@jyu.fi',
      url='http://github.com/collective/buildout.sendpickedversions',
      packages = find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['buildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'buildout.sendpickedversions.tests.test_suite',
      entry_points=entry_points,
      )
