import datetime
import logging
import urllib2
import urllib
import zc.buildout.easy_install
import pkg_resources
import socket

from buildout.sendpickedversions.wrappers import DistributionWrapper
from pprint import pprint
try:
    import json
    json
except ImportError:
    import simplejson as json


logger = zc.buildout.easy_install.logger
packages = []
processed = []
versionmap = {}
versions = None
start_data = {}


def _log_requirement(ws, req):
    # if not logger.isEnabledFor(logging.DEBUG):
    ws = list(ws)
    ws.sort()
    for dist in ws:
        if dist.project_name not in processed:
            package = DistributionWrapper(dist, versions)
            # Add package to list of processed packages
            processed.append(package.name)
            # Add data to packages list
            packages.append(package.get_dict())
            update_versionmap(package)


def update_versionmap(package):
    if package.version:
        if package.name in versionmap and\
                package.version != versionmap[package.name]:
            # We have some kind of conflict here.
            logging.error("Conflict with %s (%s) - tried to replace with "
                          "version %s" % (package.name,
                                          versionmap[package.name],
                                          package.version))
        else:
            versionmap[package.name] = package.version


def enable_sending_picked_versions(old_get_dist):
    def get_dist(self, requirement, ws, always_unzip):
        dists = old_get_dist(self, requirement, ws, always_unzip)
        for dist in dists:
            if not (dist.precedence == pkg_resources.DEVELOP_DIST or
                    (len(requirement.specs) == 1 and
                     requirement.specs[0][0] == '==')):
                self.__picked_versions[dist.project_name] = dist.version
        return dists
    return get_dist


def send_picked_versions(old_logging_shutdown, **kw):

    def logging_shutdown():

        data = {'packages': {}}

        for package in packages:
            data['packages'][package['name']] = {
                'requirements': package['requirements'],
                'version': package['version']}
        data.update(kw)
        data['versionmap'] = versionmap
        data['finished'] = datetime.datetime.now().isoformat()
        data.update(start_data)

        if kw.get('picked-data-url', None):
            res = send_picked_versions_data(kw['picked-data-url'],
                                            json.dumps(data))
            if res:
                print res
            else:
                print "Got error sending the data to %s" %\
                    kw['picked-data-url']
        elif kw.get('whiskers-url', None):
            res = send_picked_versions_data(kw['whiskers-url'],
                                            json.dumps(data))
            if res:
                print res
            else:
                print "Got error sending the data to %s" % kw['whiskers-url']
        else:
            pprint(data)

        old_logging_shutdown()
    return logging_shutdown


def send_picked_versions_data(whiskers_url, data):
    """Send buildout data to remote."""

    logging.info("Sending data to remote.")
    if whiskers_url[-1] != '/':
        whiskers_url += '/'

    req = urllib2.Request(url=whiskers_url,
                          data=urllib.urlencode({'data': data}))

    try:
        h = urllib2.urlopen(req, timeout=20)
    except TypeError, e:
        # python2.4 doesn't support timeout
        h = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print str(e)
        return None

    return h.msg or None


def install(buildout):

    kw = buildout['buildout']
    versions = kw.get('versions', None)
    # tag_buildout_start(buildout)
    zc.buildout.easy_install.Installer.__picked_versions = {}
    zc.buildout.easy_install._log_requirement = _log_requirement
    zc.buildout.easy_install.Installer._get_dist =\
        enable_sending_picked_versions(
            zc.buildout.easy_install.Installer._get_dist)

    logging.shutdown = send_picked_versions(logging.shutdown, **kw)


def tag_buildout_start_data(buildout):
    """
    Send information we know about the buildout immediately.

    This includes generic buildout config, pinned versions,
    host information.

    We will update the data later with rest of the information.
    """

    data = {'hostname': socket.gethostname(),
            'host_ip': socket.gethostbyname(socket.getfqdn()),
            'pinned_versions': buildout.get('versions', ''),
            'buildout_data': buildout.get('buildout', ''),
            'started': datetime.datetime.now().isoformat()}

    start_data = data
