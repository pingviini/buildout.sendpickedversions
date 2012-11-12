Changelog
=========

1.0a1 (unreleased)
------------------

- Returns a lots of new information about buildout including whole buildout
  section (with defaults and computed values as well).
- Returns absolutely all package requirements with versions numbers (both
  picked version and fuzzy version requirement like zope.interface >= 3.8).
- Picks buildout name from directory name - no need to specify buildoutname
  to buildout config anymore (though you still can if you want to).

0.3 (2012-10-11)
----------------

- Performance optimizations (ported from zc.buildout).

0.2 (2011-10-16)
----------------

- Sends data urlencoded.

0.1 (2011-10-16)
----------------

- Initial import
