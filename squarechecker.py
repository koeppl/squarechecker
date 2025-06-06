#!/usr/bin/env python3
""" """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import argparse
from base import *

def depth_first_search(alphabet, predicate):
	# Initialize the stack with an empty string
	stack = [""]

	while stack:
		# Pop a string from the stack
		current_string = stack.pop()

		# Test the current string with the predicate
		if not predicate(current_string):
			continue

		# Print the current string as it satisfies the predicate
		print(current_string)

		for letter in alphabet:
			stack.append(current_string + letter)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Check maximal length for a square-free word under a specific matching and alphabet size")
	common_argparse(parser)
	args = parser.parse_args()
	alphabet = list(map(chr, range(ord('a'),(ord('a')+ args.sigma))))
	encoder = get_comparator(EquivTypes[args.type.upper()])
	check_fun = get_structure_checker(StructureTypes[args.o.upper()])

	depth_first_search(alphabet, lambda x: check_fun(args.length, encoder, x))
