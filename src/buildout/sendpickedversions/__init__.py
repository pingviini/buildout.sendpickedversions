import datetime
import logging
import urllib2
import urllib
import zc.buildout.easy_install
import pkg_resources
import socket

from buildout.sendpickedversions.wrappers import DistributionWrapper
# from pprint import pprint
try:
    import json
    json
except ImportError:
    import simplejson as json


logger = zc.buildout.easy_install.logger
buildout_version = pkg_resources.get_distribution('zc.buildout').version


def install(buildout):

    buildoutinfo = BuildoutInfo(buildout)
    zc.buildout.easy_install.Installer.pick_package_info =\
        buildoutinfo.pick_package_info
    zc.buildout.easy_install.Installer._get_dist =\
        buildoutinfo.enable_sending_picked_versions(
            zc.buildout.easy_install.Installer._get_dist)

    logging.shutdown = buildoutinfo.send_picked_versions(logging.shutdown)


class BuildoutInfo(object):
    """Main class containing methods for handling buildout data."""

    def __init__(self, buildout):
        self.packages = []
        self.processed = set()
        self.versionmap = {}

        self.buildout = buildout.get('buildout', None)
        self.hostname = socket.gethostname()
        self.ipv4 = socket.gethostbyname(socket.getfqdn())
        self.pinned_versions = dict(buildout.get('versions', None))
        self.started = datetime.datetime.now().isoformat()

    def pick_package_info(self, ws, req):
        """Parses through package requirements and picks data."""
        ws = list(ws)
        ws.sort()
        for dist in ws:
            if dist.project_name not in self.processed:
                package = DistributionWrapper(dist)
                # Add package to list of processed packages
                self.processed.update([package.name])
                # Add data to packages list
                self.packages.append(package.get_dict())
                self.update_versionmap(package)

    def update_versionmap(self, package):
        """Updates version map information."""
        if package.version:
            self.versionmap[package.name] = package.version

    def enable_sending_picked_versions(self, original_get_dist):
        """
        Enables our custom code to run before zc.buildouts get_dist
        method is being called.
        """
        # Check if we have zc.buildout < 2.x
        if int(buildout_version[0]) < 2:
            def get_dist(self, requirement, ws, always_unzip):
                self.pick_package_info(ws, requirement)
                dists = original_get_dist(self, requirement, ws, always_unzip)
                return dists
        else:
            def get_dist(self, requirement, ws):
                self.pick_package_info(ws, requirement)
                dists = original_get_dist(self, requirement, ws)
                return dists

        return get_dist

    def send_picked_versions(self, old_logging_shutdown):

        def logging_shutdown():
            data = {'packages': {}}

            for package in self.packages:
                data['packages'][package['name']] = {
                    'requirements': package['requirements'],
                    'version': package['version']}

            data['buildout_config'] = dict(self.buildout)
            data['versionmap'] = self.versionmap
            data['started'] = self.started
            data['finished'] = datetime.datetime.now().isoformat()
            data['hostname'] = self.hostname
            data['ipv4'] = self.ipv4
            data['pinned_versions'] = self.pinned_versions

            res = self.send_data(json.dumps(data))
            if res:
                print res
            else:
                print "Got error sending the data to %s" % self.data_url

            old_logging_shutdown()
        return logging_shutdown

    @property
    def data_url(self):
        """Return URL where data should be sent."""
        url = None
        try:
            url = self.buildout['picked-data-url']
        except KeyError:
            # Maybe we have old configuration which uses whiskers-url
            url = self.buildout['whiskers-url']

        if url[-1] != '/':
            url += '/'

        return url

    def send_data(self, data):
        """Send buildout data to remote URL."""

        logging.info("Sending data to remote url (%s)" % self.data_url)

        req = urllib2.Request(
            url=self.data_url,
            data=urllib.urlencode({'data': data}))

        try:
            res = urllib2.urlopen(req, timeout=30)
        except TypeError, e:
            # python2.4 doesn't support timeout
            res = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print str(e)
            return None

        return res.read() or None
