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

	for mapping in product(all_strings, repeat=2):
		yield {'a': 'a', 'b': mapping[0], 'c': mapping[1]}

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


pure_morphic_squarefree_morphism = { 'a' : 'abc', 'b' : 'ac', 'c': 'b' }

my_parameterized_encoding = { 'a' : 'a', 'b' : 'b', 'c': 'cbbbc' }
# my_orderweak_encoding = { 'a' : 'a', 'b' : 'baabb', 'c': 'c' }
my_order_encoding = { 'a' : 'a', 'b' : 'b', 'c': 'ac' }
my_cart_encoding = {'a': 'bac', 'b': 'ccb', 'c': 'a'}



def check_encoding(encoding, rootlength, matching):
	text = 'a'
	for _ in range(1,8):
		text = apply_morphism(pure_morphic_squarefree_morphism, text)
		enctext = apply_morphism(encoding, text)
		assert is_square_free(rootlength, matching, enctext)


encodinglength = 5
morphism_iteration=6
rootminlength=3
if __name__ == "__main__":
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
			# if not is_square_free(rootminlength, compute_order_preserving_weak_encoding, enctext):
			# if not is_square_free(rootminlength, psv_encoding, enctext):
			if not is_square_free(rootminlength, psv_encoding, enctext):
				isSquareFree = False
				break
		if isSquareFree:
			print(encoding)
