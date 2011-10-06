# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = "0.1"

entry_point = 'buildout.sendpickedversions:install'
entry_points = {"zc.buildout.extension": ["default = %s" % entry_point]}

tests_require=['zc.buildout', 'zope.testing', 'zc.recipe.egg']

setup(name='buildout.sendpickedversions',
      version=version,
      description="Send buildout picked versions to wrw server.",
      long_description="",
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
      install_requires=['setuptools',
                        'zc.buildout'
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'buildout.sendpickedversions.tests.test_suite',
      entry_points=entry_points,
      )
