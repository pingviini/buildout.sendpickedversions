class DistributionWrapper(object):
    """Wrapper class for distribution specs."""

    def __init__(self, dist):
        self.dist = dist

    @property
    def name(self):
        return self.dist.project_name

    @property
    def version(self):
        return getattr(self.dist, 'version', None)

    @property
    def requirements(self):
        """Return list of distribution requirements."""
        requirements = []

        for requirement in self.dist.requires():
            requirement_info = dict(name=requirement.project_name)
            if requirement.specs:
                specs = requirement.specs[0]
                requirement_info['equation'] = specs[0]
                requirement_info['version'] = specs[1]
            requirements.append(requirement_info)
        return requirements

    def get_dict(self):
        """Return dict of distribution and its requirements."""
        return {'name': self.name,
                'requirements': self.requirements,
                'version': self.version}
