__author__ = 'Ashkan Nasseri'


class PatternModel(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self.wildcard_locations = self.__get_wildcard_locations()
        self.wildcard_locations_sum = sum(self.wildcard_locations)

    def __get_wildcard_locations(self):
        pattern_sections = self.pattern.split(",")
        return [i for i, section in enumerate(pattern_sections) if section == "*"]

