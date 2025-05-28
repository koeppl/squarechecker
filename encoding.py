#!/usr/bin/env python3
""" """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import argparse

from itertools import product
import random

from base import *

def enumerate_string_morphisms(alphabet, k):
	"""
	Generate all string morphisms from {a, b, c} to strings of length 1 up to k.

	Each morphism is represented as a dictionary with keys 'a', 'b', and 'c',
	mapping to strings of length 1 up to k.

	Args:
		k (int): The maximum length of strings to map to.

	Yields:
		dict: A dictionary representing the string morphism.
	"""
	# Generate all possible strings of length 1 up to k from the alphabet {a, b, c}
	all_strings = []

	lengths = list(range(1, k + 1))
	random.shuffle(lengths)
	for length in lengths:
		all_strings.extend(''.join(p) for p in product(alphabet, repeat=length))

	# Generate all combinations of mappings for a, b, c
	for mapping in product(all_strings, repeat=len(alphabet)):
		yield {'a': mapping[0], 'b': mapping[1], 'c': mapping[2]}
	# for mapping in all_strings:
	# 	yield {'a': 'aa', 'b': 'bb', 'c': mapping}

def apply_morphism(morphism, string):
	"""
	Apply a string morphism to a given string.

	Args:
		morphism (dict): The string morphism as a dictionary.
		string (str): The input string to transform.

	Returns:
		str: The transformed string.
	"""
	return ''.join(morphism[char] for char in string)

# from itertools import product
#
# def generate_strings(alphabet, max_length):
# 	"""
# 	Generate all strings of a given alphabet up to a maximum length.
#
# 	:param alphabet: List of characters in the alphabet (e.g., ['a', 'b', 'c'])
# 	:param max_length: Maximum length of strings to generate
# 	:return: A list of strings
# 	"""
# 	lengths = list(range(1, max_length + 1))
# 	random.shuffle(lengths)
# 	for length in lengths:
# 		for p in product(alphabet, repeat=length):
# 			yield ''.join(p)

pure_morphic_squarefree_morphism = { 'a' : 'abc', 'b' : 'ac', 'c': 'b' }

my_parameterized_encoding = { 'a' : 'a', 'b' : 'b', 'c': 'cbbbc' }
my_order_encoding = { 'a' : 'a', 'b' : 'ccb', 'c': 'bac' }
my_cart_encoding = {'a': 'bac', 'b': 'ccb', 'c': 'a'}



def check_encoding(encoding, rootlength, matching):
	text = 'a'
	for _ in range(1,8):
		text = apply_morphism(pure_morphic_squarefree_morphism, text)
		enctext = apply_morphism(encoding, text)
		assert is_square_free(rootlength, matching, enctext)


encodinglength = 4
morphism_iteration=6
rootminlength=4
if __name__ == "__main__":
	check_encoding(my_parameterized_encoding, 3, compute_prev_encoding)
	check_encoding(my_order_encoding, 3, compute_order_preserving_encoding)
	check_encoding(my_cart_encoding, 4, psv_encoding)
	print('[start]')

	alphabet = ['a', 'b', 'c']
	texts = ['a']
	for it in range(1,morphism_iteration):
		texts.append(apply_morphism(pure_morphic_squarefree_morphism, texts[-1])) 
		assert is_square_free(1, lambda x:x, texts[-1])

	for encoding in enumerate_string_morphisms(alphabet, encodinglength):
		isSquareFree = True
		for text in texts:
			enctext = apply_morphism(encoding, text)
			if not is_square_free(rootminlength, psv_encoding, enctext):
				isSquareFree = False
				break
		if isSquareFree:
			print(encoding)



	# # Argument parser for command line usage
	# parser = argparse.ArgumentParser(description="Check maximal length for a square-free word under a specific matching and alphabet size")
	# #alphabet size:
	# parser.add_argument("--sigma", "-s", type=int, help="The size of the alphabet (e.g., 2 for {a, b}).", default=2)
	# parser.add_argument("--type", "-t", type=str, choices=["strict", "parameterized", "order", "cart"], help="The type of matching to use (string or parameterized).", default="parameterized")
	# # matching length:
	# parser.add_argument("--length", "-l", type=int, help="The maximum length of allowed roots.", default=1)
	# args = parser.parse_args()
  #
	# alphabet = list(map(chr, range(ord('a'),(ord('a')+ args.sigma))))
	# encoder = lambda x : x
	# if args.type == "parameterized":
	# 	encoder = compute_prev_encoding
	# elif args.type == "order":
	# 	encoder = compute_order_preserving_encoding
	# elif args.type == "cart":
	# 	encoder = psv_encoding
  #
	# depth_first_search(alphabet, lambda x: is_square_free(args.length, encoder, x))
