buildout.sendpickedversions
===========================

This package is heavily inspired by buildout.dumppickedversions_ and its purpose
is to gather the buildout information and send it as json data to a specified
remote server.

Remote server can be anything that can handle json data, but there is already
working server for that - Whiskers_. Whiskers is developed hand in hand
with buildout.sendpickedversions to store and display the data.

Configuration
-------------

To use buildout.sendpickedversions with buildout your buildout.cfg should have
buildout.sendpickedversions in you extensions-line and following fields
configured:

buildoutname
    This is the name of the buildout. Whiskers_ uses this information to create
    new buildout object with the package data. If buildout configuration doesn't
    contain `buildoutname` the script picks the folders name where buildout is
    located.

send-data-url
    This is the url where data is sent after buildout has been run. If you
    leave this empty or don't set at all buildout.sendpickedversions just
    displays the data dict. In earlier versions of buildout.sendpickedversions
    this setting was called `whiskers-url` - this works until next major
    version (2.x).

To get most out of buildout.sendpickedversions above configuration should be in
buildouts global configuration at $HOME/.buildout/default.cfg.

Example
-------

Here's small example configuration. ::

    [buildout]
    extensions = buildout.sendpickedversions
    buildoutname = test
    send-data-url = http://localhost:6543

    parts = nose

    [nose]
    recipe = zc.recipe.egg
    eggs = nose

Above example configuration assumes you have Whiskers_ server running locally on
port 6543. If you run buildout it will install nose normally to your buildout
environment. After buildout has set up the environment 
buildout.sendpickedversions will try to send following json formatted data to
the url specified in configuration: ::

    {"buildoutname": "test",
     "packages": [
        {"version": "0.6.24", "name": "distribute"},
        {"version": "1.18", "name": "mr.developer"},
        {"version": "1.1.2", "name": "nose"},
        {"required_by": ["mr.developer 1.18"], "version": "1.5.2",
         "name": "zc.buildout"},
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
