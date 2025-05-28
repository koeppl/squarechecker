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

		# If the current string length is less than max length, expand it
		for letter in alphabet:
			# if letter == 'a' and current_string.endswith('aa'):
			# 	continue
			# if letter == 'b' and current_string.endswith('b'):
			# 	continue
			# if letter == 'c' and current_string.endswith('c'):
			# 	continue
			# if letter == 'd' and current_string.endswith('d'):
			# 	continue
			stack.append(current_string + letter)

# print(is_parameterized_square_free('abbababbaa'))

if __name__ == "__main__":
	# Argument parser for command line usage
	parser = argparse.ArgumentParser(description="Check maximal length for a square-free word under a specific matching and alphabet size")
	#alphabet size:
	parser.add_argument("--sigma", "-s", type=int, help="The size of the alphabet (e.g., 2 for {a, b}).", default=2)
	parser.add_argument("--type", "-t", type=str, choices=["strict", "parameterized", "order", "cart"], help="The type of matching to use (string or parameterized).", default="parameterized")
	# matching length:
	parser.add_argument("--length", "-l", type=int, help="The maximum length of allowed roots.", default=1)
	args = parser.parse_args()

	alphabet = list(map(chr, range(ord('a'),(ord('a')+ args.sigma))))
	encoder = lambda x : x
	if args.type == "parameterized":
		encoder = compute_prev_encoding
	elif args.type == "order":
		encoder = compute_order_preserving_encoding
	elif args.type == "cart":
		encoder = psv_encoding

	depth_first_search(alphabet, lambda x: is_square_free(args.length, encoder, x))
