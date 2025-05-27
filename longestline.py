#!/usr/bin/env python3
"""   """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import sys

def longest_line():
	longest = ""
	for line in sys.stdin:
		line = line.rstrip('\n')
		if len(line) > len(longest):
			longest = line
	print(longest)

if __name__ == "__main__":
	longest_line()

