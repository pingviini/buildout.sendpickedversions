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

    {'buildout_config': {
        'allow-hosts': '*',
        'allow-picked-versions': 'true',
        'bin-directory': '/buildout/example/bin',
        'buildoutname': 'test',
        'develop-eggs-directory': '/buildout/folder/develop-eggs',
        'directory': '/buildout/folder',
        'download-cache': '/home/user/.buildout/download-cache',
        'eggs-directory': '/home/user/.buildout/eggs-directory',
        'executable': '/path/to/python',
        'extends-cache': '/home/user/.buildout/extends-cache',
        'extensions': 'buildout.sendpickedversions',
        'find-links': '',
        'install-from-cache': 'false',
        'installed': '/buildout/folder/.installed.cfg',
        'log-format': '',
        'log-level': 'INFO',
        'newest': 'false',
        'offline': 'false',
        'parts': 'nose',
        'parts-directory': '/buildout/folder/parts',
        'prefer-final': 'true',
        'python': 'buildout',
        'send-data-url': 'http://localhost:6543',
        'show-picked-versions': 'false',
        'socket-timeout': '',
        'update-versions-file': '',
        'use-dependency-links': 'true',
        'versions': 'versions'},
     'finished': '2013-03-20T11:06:42.900950',
     'hostname': 'latitude',
     'ipv4': '127.0.1.1',
     'packages': {
         'Python': {'requirements': [], 'version': '2.7'},
         'argparse': {'requirements': [], 'version': '1.2.1'},
         'buildout.sendpickedversions': {'requirements': [{'name': 'setuptools'},
                                                          {'name': 'zc.buildout'}],
                                         'version': '1.0a1'},
         'distribute': {'requirements': [], 'version': '0.6.35'},
         'nose': {'requirements': [], 'version': '1.2.1'},
         'pip': {'requirements': [], 'version': '1.2.1'},
         'wsgiref': {'requirements': [], 'version': '0.1.2'},
         'zc.buildout': {'requirements': [{'name': 'setuptools'}],
                         'version': '2.0.1'},
         'zc.recipe.egg': {'requirements': [{'equation': '>=',
                                             'name': 'zc.buildout',
                                             'version': '1.2.0'},
                                            {'name': 'setuptools'}],
                           'version': '2.0.0a3'}},
     'pinned_versions': {'zc.buildout': '>=2.0.1', 'zc.recipe.egg': '>=2.0.0a3'},
     'started': '2013-03-20T11:06:42.279059',
     'versionmap': {
         'Python': '2.7',
         'argparse': '1.2.1',
         'buildout.sendpickedversions': '1.0a1',
         'distribute': '0.6.35',
         'nose': '1.2.1',
         'pip': '1.2.1',
         'wsgiref': '0.1.2',
         'zc.buildout': '2.0.1',
         'zc.recipe.egg': '2.0.0a3'}}


Thanks
------

Code is mainly based to Mustapha Benali's buildout.dumppickedversions_. This
buildout extension has probably saved thousands of buildouts from nasty version
conflicts or total havoc. Huge thanks!

.. _buildout.dumppickedversions: http://pypi.python.org/pypi/buildout.dumppickedversions
.. _Whiskers: http://github.com/pingviini/whiskers
