import logging
import urllib2
import urllib
import zc.buildout.easy_install
import pkg_resources
from pprint import pprint
try:
    import json
except ImportError:
    import simplejson as json


logger = zc.buildout.easy_install.logger
packages = []
processed = []


def _log_requirement(ws, req):
    # if not logger.isEnabledFor(logging.DEBUG):
    ws = list(ws)
    ws.sort()
    for dist in ws:
        if dist.project_name not in processed:
            parse_specs(dist)


def parse_specs(dist):
    """Parse specs of package requirements and store them to global list"""

    requirements = []

    for requirement in dist.requires():
        req = {}

        if requirement.specs:
            info = requirement.specs[0]
            req = {'name': requirement.project_name,
                   'equation': info[0],
                   'version': info[1]}
        else:
            req = {'name': requirement.project_name}

        requirements.append(req)

    processed.append(dist.project_name)
    packages.append({'name': dist.project_name,
                     'requirements': requirements,
                     'version': getattr(dist, 'version', None)})


def enable_sending_picked_versions(old_get_dist):
    def get_dist(self, requirement, ws, always_unzip):
        dists = old_get_dist(self, requirement, ws, always_unzip)
        for dist in dists:
            if not (dist.precedence == pkg_resources.DEVELOP_DIST or \
                    (len(requirement.specs) == 1 and requirement.specs[0][0] == '==')):
                self.__picked_versions[dist.project_name] = dist.version
        return dists
    return get_dist


def send_picked_versions(old_logging_shutdown, **kw):

    def logging_shutdown():

        data = {'packages': {}}

        for package in packages:
            data['packages'][package['name']] = {'requirements': package['requirements'],
                                     'version': package['version']}
        buildout_name = getattr(kw, 'buildout_name', None) or\
                kw['directory'].rsplit('/',1)[-1]
        data.update({'buildoutname': buildout_name})

        if getattr(kw, 'whiskers_url', None):
            res = send_picked_versions_data(kw['whiskers_url'], json.dumps(data))
            if res:
                print res
            else:
                print "Got error sending the data to %s" % kw['whiskers_url']
        else:
            pprint(data)

        old_logging_shutdown()
    return logging_shutdown


def send_picked_versions_data(whiskers_url, data):
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

    zc.buildout.easy_install.Installer.__picked_versions = {}
    zc.buildout.easy_install._log_requirement = _log_requirement
    zc.buildout.easy_install.Installer._get_dist = enable_sending_picked_versions(
                                  zc.buildout.easy_install.Installer._get_dist)

    logging.shutdown = send_picked_versions(logging.shutdown, **kw)
