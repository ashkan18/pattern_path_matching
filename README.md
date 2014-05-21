Pattern Path Matching
=====================

This is a command line program which reads the patterns and paths from the input and finds "The Best Match" for each
path if any match exists.

In order to run:
python pattern_matching.py < input.txt > output

The way it works is, it iterates through the list of patterns once o(n) and generates a dictionary of a dictionary
of a list of Patterns Models. The idea behind this structure is to create a data structure that helps in finding
the match the easiest and fastest possible way. We build this structure once and we use it many times with o(1)
(since its hashmap). Here is a model of data structure (assume <Key, value> is a hash an [] shows a list):

<number of sections in pattern, <number of wildcards in asc order, [pattern models]>>

This way when we get a path, we first check in parent dict to see if there is a row in hash for this path's number of
sections. For example if path is a/b and we don't have any pattern in the parent dict
where number of sections in pattern is 2 it means there is no match, so we don't have to check every where, o(1).
In case we found a row in parent dict, it means there are patterns that have same number of sections, now we
iterate through the second dict. Second dict key values (number of wildcards) are in asc order, the reason is we first
want to check patterns with less number of wildcards and if we didn't find them we want to go to the next list.
In each list we check all the patterns to make sure we pick the best match*.


* definition of best match is:  prefer the pattern whose leftmost wildcard appears in a field further to the right.
If multiple patterns' leftmost wildcards appear in the same field position, apply this rule recursively
to the remainder of the pattern.
In order to gains this, I used this algorithm where I find the index of each wildcard in a pattern and I add them up
the best pattern is the one that has the max sum.

