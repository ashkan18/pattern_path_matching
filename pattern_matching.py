import sys
from pattern_model import PatternModel
from pattern_path_matcher import PatternPathMatcher

__author__ = 'Ashkan Nasseri'


"""
   This file will handle pattern matching defined as bellow, it has a main method which will handle the flow
   of the program
"""

NO_MATCH_TEXT = 'NO MATCH'


class InputException(Exception):
    message = "There was a problem in reading the input"


def main():
    """
    Main function of the program, this method handles the main process of the program and the flow which is
    reading the user input, create a match class and call matching and show the results, it also handles errors
    """
    try:
        # first we get number of patterns
        number_of_patterns = read_number_of_patterns_from_input()

        # now based on number of patterns we read them one by one
        patterns = read_patterns_from_input(number_of_patterns)

        # read number of paths
        number_of_paths = read_number_of_paths_from_input()

        # now read the paths
        paths = read_paths_from_input(number_of_paths)

        # create a new pattern matcher instance with patterns and paths we received from input
        pattern_matcher = PatternPathMatcher(patterns, paths)

        # get the matching results from pattern matcher, this is where actual matching happnes
        matches = pattern_matcher.get_matching()

        # show the received patterns to the user
        show_matches(matches)

    except InputException as e:
        # there was an error in reading parameters
        show_error(e)
        show_usage()
    except ValueError as e:
        # when user inputs not integer for where we expect integers
        show_error(e)
        show_usage()


def read_number_of_patterns_from_input():
    """
    This method reads number of patterns from the input, if input is not int it will raise ValueError exception
    """
    number_of_patterns = raw_input("Please enter number of patterns:\n")
    return int(number_of_patterns)


def read_patterns_from_input(number_of_patterns):
    """
    This method reads patterns from input based on number of patterns we are expecting,
    if the number of patterns doesn't match the number of inputs it will raise InputException
    """
    patterns = []
    for i in range(number_of_patterns):
        pattern = sys.stdin.readline()
        #@TODO: validate the pattern
        patterns.append(pattern.rstrip("\n").lstrip(",").rstrip(","))
    return patterns


def read_number_of_paths_from_input():
    """
    This method reads the number of paths from input, if the input is not a valid int it will raise ValueError
    """
    number_of_paths = raw_input("Please enter number of paths:\n")
    return int(number_of_paths)


def read_paths_from_input(number_of_paths):
    """
    This method reads paths from user input based on number of paths,
    if the number of paths doesn't match the number of inputs it will raise InputException
    """
    paths = []
    for i in range(number_of_paths):
        path = sys.stdin.readline()
        if path is None:
            raise InputException

        #@TODO: validate the path
        paths.append(path.rstrip("\n").lstrip("/").rstrip("/"))
    return paths


def show_error(e):
    """
    This method will show users a proper error message based on the input Exception we get
    """
    pass


def show_usage():
    """
    This method will show the usage of this program
    """
    print "Usage:\n python pattern_matching.py \n"
    print "you can pass in a file as input where first line would be the number" \
          "of patterns we have, in the lines after input each pattern. The line after patterns input number of paths" \
          "and in subsequent lines input the actual paths"""


def show_matches(matches):
    """
    This method shows the result of matching, each match can either be a @PatternModel in case of successfull match
     or None in case of not having a match
    @param matches:
    @return:
    """
    for match in matches:
        if match is not None and isinstance(match, PatternModel):
            print u'    {0}'.format(match.pattern)
        else:
            print u'    {0}'.format(NO_MATCH_TEXT)


if __name__ == "__main__":
    # this is where the command line program starts
    # on the start call our main function
    main()
