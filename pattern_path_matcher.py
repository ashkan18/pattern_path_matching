import collections
from pattern_model import PatternModel

__author__ = 'Ashkan Nasseri'


class PatternPathMatcher(object):
    """
    This class does Pattern to Path matching, it gets pattern and paths as constructor inputs.
    It builds an efficient data structure using the input patterns which makes it easier to do the matching
    """
    pattern_items_count_hash = {}
    paths = None

    def __init__(self, patterns, paths):
        self.__sort_patterns_by_importance(patterns)
        self.paths = paths

    def get_matching(self):
        """
        This method will go through the paths and for each of them finds the "best match" and return
        the results as a list of matches, if there was no match it will output No Match
        @return: a list of matches, if we had a successful match we add PatternModel of the match otherwise we add None
        """
        final_matches = []
        for path in self.paths:
            path_sections = path.split("/")
            number_of_sections = len(path_sections)

            # check if we have patterns with this number of sections
            if number_of_sections not in self.pattern_items_count_hash:
                final_matches.append(None)
                continue
            else:
                best_match = None
                current_wildcard_position_sum = None
                # get the list of patterns with this number of sections
                for wild_card_count, patterns in self.pattern_items_count_hash[number_of_sections].items():
                    for pattern in patterns:
                        matched = self.match(path=path, pattern_model=pattern)
                        if matched and (current_wildcard_position_sum is None
                                        or pattern.wildcard_locations_sum > current_wildcard_position_sum):
                            best_match = pattern
                            current_wildcard_position_sum = pattern.wildcard_locations_sum
                    if best_match is not None:
                        break
                if best_match is not None:
                    final_matches.append(best_match)
                else:
                    final_matches.append(None)
        return final_matches

    def match(self, path, pattern_model):
        """
        This method gets a path and a pattern and tries to match, in result it will return the match results
        and also the sum of
        @param path: String containing the path we are trying to check the match
        @param pattern_model: String containing the pattern we are trying to match with path
        @return: boolean showing if it was a match or not
        """
        path_sections = path.split("/")
        pattern_sections = pattern_model.pattern.split(",")

        for i, path_section in enumerate(path_sections):
            if i not in pattern_model.wildcard_locations:
                if path_section != pattern_sections[i]:
                    return False
        return True

    def __sort_patterns_by_importance(self, patterns):
        """
        This private method will read a list of patterns and from that it will populate a data structure that helps
        using patterns and match them with paths,
        The data structure is basically a hashmap(directory) of a sorted by key directory.
        The key in the parent hashmap is the count of sections in a pattern, for example 'a,*' will have a count of
        two since it has two sections and 'a,*,*' will have a count of 3. so first one would end up in the bucket 2 in
        the parent hashmap and second one will end up in the bucket 3 of the hashmap.
        inside each bucket of the hashmap is a sorted hashmap of of pattern models where the key of the hashmap is
        the number of wildcards of each pattern this way when we want to match we first start with the patterns with
        less wildcards and if we didn't find a match we try patterns with more wildcards,
        this way we can easier find "best match",

        a sample hash structure for these patterns:
            a,
            foo,
            *,
            a,b,c
            a,*,*
            *,*,foo
            *, bar, foo

        would be this:
            {
             1: {
                    0:['a', 'foo'], # this is basically saying there are two patterns with one section without wildcard
                    1:['*'] # same as above with one wildcard
                },
             3: {
                    0:['a, b, c', 'foo, bar, baz'], # three sections in pattern and no wildcard
                    1:['*, bar, foo'] # three sections, one wildcard
                    2:['a, *, *', '*, *, foo'] # three sections, two wildcards
                }

            }
        @param patterns: list of patterns we got from the user.
        """

        # first lets construct a dictionary of a dictionary of a list of patterns based on number of matches in the
        # pattern and number of wildcards
        pattern_match_count_hash = {}
        for pattern in patterns:
            matches = pattern.split(',')
            number_of_wildcard = matches.count('*')
            number_of_matches = len(matches)

            pattern_model = PatternModel(pattern)

            if number_of_matches not in pattern_match_count_hash:
                # we don't have patterns with this number of matches yet, add a new count to final hash
                pattern_match_count_hash[number_of_matches] = {number_of_wildcard: [pattern_model]}
            else:
                wildcard_count_pattern_list_hash = pattern_match_count_hash[number_of_matches]
                # we already have patterns with the same number of matches, get the current hash
                # and add this pattern to proper key based on its number of wildcards
                if number_of_wildcard in wildcard_count_pattern_list_hash:
                    # we already had patterns with this many wildcard in wildcard count hash, get that hash value
                    # since we want to modify it
                    wildcard_count_pattern_list_hash[number_of_wildcard].append(pattern_model)
                else:
                    # add this new value to wildcard count hash
                    wildcard_count_pattern_list_hash[number_of_wildcard] = [pattern_model]

        # now that we have generated the hash, lets go through the hash and crete sorted array from it
        for match_count, wildcard_count_pattern_hash in pattern_match_count_hash.items():
            # each item in this hash is a hash of number of wildcard and their patterns
            self.pattern_items_count_hash[match_count] = {}
            # now we sort the dictionary of patterns based on their count of wildcards and we add all of them
            # in that order to the list of patterns in that bucket
            wildcard_count_sorted_dict = collections.OrderedDict(sorted(wildcard_count_pattern_hash.items()))
            for number_of_wildcards, patterns_list in wildcard_count_sorted_dict.items():
                self.pattern_items_count_hash[match_count][number_of_wildcards] = patterns_list