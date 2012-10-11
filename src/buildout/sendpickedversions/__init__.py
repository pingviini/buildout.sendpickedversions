import logging
import urllib2
import urllib
import zc.buildout.easy_install
import pkg_resources
try:
    import json
except ImportError:
    import simplejson as json


logger = zc.buildout.easy_install.logger
required_by = {}


def _log_requirement(ws, req):
    if not logger.isEnabledFor(logging.DEBUG):
        ws = list(ws)
        ws.sort()
        for dist in ws:
            if req in dist.requires():
                req_ = str(req)
                dist_ = str(dist)
                if req_ in required_by and dist_ not in required_by[req_]:
                    required_by[req_].append(dist_)
                else:
                    required_by[req_] = [dist_]
                logger.debug("  required by %s." % dist)


def enable_sending_picked_versions(old_get_dist):
    def get_dist(self, requirement, ws, always_unzip):
        dists = old_get_dist(self, requirement, ws, always_unzip)
        for dist in dists:
            if not (dist.precedence == pkg_resources.DEVELOP_DIST or \
                    (len(requirement.specs) == 1 and requirement.specs[0][0] == '==')):
                self.__picked_versions[dist.project_name] = dist.version
        return dists
    return get_dist


def send_picked_versions(old_logging_shutdown, whiskers_url, buildout_name):

    packages = []
    def logging_shutdown():

        packages_dict = sorted(zc.buildout.easy_install.Installer.__picked_versions.items() +\
                      zc.buildout.easy_install.Installer._versions.items())
        for d, v in packages_dict:
            package = dict()
            if d in required_by:
                package['required_by'] = required_by[d]
            package['name'] = d
            package['version'] = v

            packages.append(package)
            data = dict(packages=packages, buildoutname=buildout_name)

        if whiskers_url:
            res = send_picked_versions_data(whiskers_url, json.dumps(data))
            if res:
                print res
            else:
                print "Got error sending the data."
        else:
            print json.dumps(data)

        old_logging_shutdown()
    return logging_shutdown

def send_picked_versions_data(whiskers_url, data):
    req = urllib2.Request(url=whiskers_url, data=urllib.urlencode({'data':data}))
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

    whiskers_url = 'whiskers-url' in buildout['buildout'] and \
              buildout['buildout']['whiskers-url'].strip() or \
              None
    buildout_name = 'buildoutname' in buildout['buildout'] and \
                    buildout['buildout']['buildoutname'].strip() or \
                    'dummy_buildout'

    zc.buildout.easy_install.Installer.__picked_versions = {}
    zc.buildout.easy_install._log_requirement = _log_requirement
    zc.buildout.easy_install.Installer._get_dist = enable_sending_picked_versions(
                                  zc.buildout.easy_install.Installer._get_dist)

    logging.shutdown = send_picked_versions(logging.shutdown, whiskers_url, buildout_name)
