__author__ = 'Ashkan Nasseri'


class PatternModel(object):
    """
    This class defines a pattern in our app, a pattern model has:
    - pattern: string that's the actual pattern
    - wildcard_locations a list of int showing where in the pattern if any we have wildcards
    - wildcard_locations_sum an int showing the sum of locations of wildcards the more the better pattern
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.wildcard_locations = self.__get_wildcard_locations()
        self.wildcard_locations_sum = sum(self.wildcard_locations)

    def __get_wildcard_locations(self):
        """
        This private method gets a list of locations of wildcard in this pattern and returns the list
        @return: list of locations of wildcards in this pattern
        """
        pattern_sections = self.pattern.split(",")
        return [i for i, section in enumerate(pattern_sections) if section == "*"]

