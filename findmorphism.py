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


# my_parameterized_encoding = { 'a' : 'a', 'b' : 'b', 'c': 'cbbbc' }
# # my_orderweak_encoding = { 'a' : 'a', 'b' : 'baabb', 'c': 'c' }
# my_order_encoding = { 'a' : 'a', 'b' : 'b', 'c': 'ac' }
# my_cart_encoding = {'a': 'bac', 'b': 'ccb', 'c': 'a'}

pure_morphic_squarefree_morphism = { 'a' : 'abc', 'b' : 'ac', 'c': 'b' }


def check_encoding(encoding, rootlength, matching):
	text = 'a'
	for _ in range(1,8):
		text = apply_morphism(pure_morphic_squarefree_morphism, text)
		enctext = apply_morphism(encoding, text)
		assert is_square_free(rootlength, matching, enctext)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Enumerates morphisms that generate l^+ square-free words under different equivalence types.")
	common_argparse(parser)
	parser.add_argument('--codelength', type=int, default=5, help='The maximum length of the strings in the coding morphism.')
	parser.add_argument('--iterations', type=int, default=6, help='The number of iterations of the morphism to apply to the start word a.')
	args = parser.parse_args()
	args.sigma = 3
	alphabet = list(map(chr, range(ord('a'),(ord('a')+ args.sigma))))
	encoder = get_comparator(EquivTypes[args.type.upper()])
	check_fun = get_structure_checker(StructureTypes[args.o.upper()])

	texts = ['a']

	for it in range(1,args.iterations):
		texts.append(apply_morphism(pure_morphic_squarefree_morphism, texts[-1]))
		assert is_square_free(1, lambda x:x, texts[-1])

	for encoding in enumerate_string_morphisms(alphabet, args.codelength):
		isSquareFree = True
		print(encoding)
		for text in texts:
			enctext = apply_morphism(encoding, text)
			if not check_fun(args.length, encoder, enctext):
				isSquareFree = False
				break
		if isSquareFree:
			print(encoding)
