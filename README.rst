buildout.sendpickedversions
===========================

This package is based on buildout.dumppickedversions_ and its purpose is to
gather the package name and version information from buildout. The main
difference with buildout.dumppickedversions_ is that instead of displaying
picked versions, or dumping everything to a file, we'll send package information
to a predefined URL.

Original use case is that there is Whiskers_ server on the other end which stores
the data. There's nothing special about the data, so other end can just as well
be anything that can handle json.


Configuration
-------------

To use buildout.sendpickedversions with buildout your buildout.cfg should have
buildout.sendpickedversions in you extensions-line and following fields
configured:

buildoutname
    This is the name of the buildout. Whiskers_ uses this information to create
    new buildout object with the package data. If name is not set we use default
    'dummy_buildout' as a name.

whiskers-url
    This is the url to whiskers server. As stated above, you can use here
    anything that can just eat the json-data we're sending. If you leave this
    empty or don't set at all buildout.sendpickedversions just displays the data
    dict.

Example
-------

Here's small example configuration. ::

    [buildout]
    extensions = buildout.sendpickedversions
    buildoutname = test
    whiskers-url = http://localhost:6543/buildouts/add

    parts = nose

    [nose]
    recipe = zc.recipe.egg
    eggs = nose

Above example configuration assumes you have Whiskers_ server running locally on
port 6543. If you run buildout it will install nose normally to your buildout
environment and after everything is ready it will try to send following data in
json-format to localhost:6543/buildouts/add URL: ::

    {"buildoutname": "test",
     "packages": [
        {"version": "0.6.24", "name": "distribute"},
        {"version": "1.18", "name": "mr.developer"},
        {"version": "1.1.2", "name": "nose"},
        {"required_by": ["mr.developer 1.18"], "version": "1.5.2", "name": "zc.buildout"},
        {"version": "1.3.2", "name": "zc.recipe.egg"}
      ]
    }

Thanks
------

Code is mainly based to Mustapha Benali's buildout.dumppickedversions_. This
buildout extension has probably saved thousands of buildouts from nasty version
conflicts or total havoc. Huge thanks!

.. _buildout.dumppickedversions: http://pypi.python.org/pypi/buildout.dumppickedversions
.. _Whiskers: http://github.com/pingviini/whiskers
