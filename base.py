#!/usr/bin/env python3
""" This module provides various encoding functions and utilities for string analysis. """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import enum
import argparse

def common_argparse(parser: argparse.ArgumentParser):
	""" Adds common arguments to the provided parser. """
	parser.add_argument("--sigma", "-s", type=int, help="The size of the alphabet (e.g., 2 for {a, b}).", default=2)
	parser.add_argument("-o", type=str, choices=list(StructureTypes.__members__.keys()), help="The type of structure to search.", default="SQUARE")
	parser.add_argument("--type", "-t", type=str, choices=list(EquivTypes.__members__.keys()), help="The type of matching to use (string or parameterized).", default="PARAMETERIZED")
	parser.add_argument("--length", "-l", type=int, help="The maximum length of allowed roots.", default=1)


class EquivTypes(enum.StrEnum):
	""" Enumeration of equivalence types for strings. """
	STRICT = enum.auto()
	PARAMETERIZED = enum.auto()
	ORDER_PRESERVING = enum.auto()
	WEAK_ORDER_PRESERVING = enum.auto()
	CARTESIAN = enum.auto()


class StructureTypes(enum.StrEnum):
	""" Enumeration of equivalence types for strings. """
	SQUARE = enum.auto()
	CUBE = enum.auto()

def get_structure_checker(structure_type: StructureTypes):
	""" Returns a function to check if a string is square-free or cube-free based on the structure type. """
	if structure_type == StructureTypes.SQUARE:
		return is_square_free
	elif structure_type == StructureTypes.CUBE:
		return is_cube_free
	else:
		raise ValueError(f"Unknown structure type: {structure_type}")

def get_comparator(equiv_type: EquivTypes):
	""" Returns a comparator function based on the equivalence type. """
	if equiv_type == EquivTypes.STRICT:
		return lambda x: x
	elif equiv_type == EquivTypes.PARAMETERIZED:
		return compute_prev_encoding
	elif equiv_type == EquivTypes.ORDER_PRESERVING:
		return compute_order_preserving_encoding
	elif equiv_type == EquivTypes.WEAK_ORDER_PRESERVING:
		return compute_order_preserving_weak_encoding
	elif equiv_type == EquivTypes.CARTESIAN:
		return psv_encoding
	else:
		raise ValueError(f"Unknown equivalence type: {equiv_type}")

def compute_order_preserving_weak_encoding(s: str) -> list[int]:
	sorted_indices = sorted(range(len(s)), key=lambda i: (s[i], i))
	rank = [0] * len(s)
	for r, i in enumerate(sorted_indices):
		rank[i] = r
	return rank

def compute_order_preserving_encoding(s: str) -> list[int]:
	unique_sorted = sorted(set(s))
	rank_map = {char: rank for rank, char in enumerate(unique_sorted)}
	return [rank_map[c] for c in s]

def psv_encoding(s: str) -> list[int]:
	stack = []  # stores (char, index)
	result = [0] * len(s)
	for i, c in enumerate(s):
		while stack and stack[-1][0] > c:
			stack.pop()
		if stack:
			result[i] = i - stack[-1][1]
		else:
			result[i] = 0
		stack.append((c, i))
	return result

def test_psv_encoding():
	assert psv_encoding("") == []
	assert psv_encoding("a") == [0]
	assert psv_encoding("aa") == [0, 1], "expected [0, 1] but got {}".format(psv_encoding("aa"))
	assert psv_encoding("ab") == [0, 1], "expected [0, 1] but got {}".format(psv_encoding("ab"))
	assert psv_encoding("ba") == [0, 0], "expected [0, 0] but got {}".format(psv_encoding("ba"))
	assert psv_encoding("abc") == [0, 1, 1]
	assert psv_encoding("cba") == [0, 0, 0]
	assert psv_encoding("banana") == [0, 0, 1, 2, 1, 2]
	assert psv_encoding("aaaa") == [0, 1, 1, 1], "expected [0, 1, 1, 1] but got {}".format(psv_encoding("aaaa"))
	assert psv_encoding("abcdabcd") == [0, 1, 1, 1, 4, 1, 1, 1], "expected [0, 1, 1, 1, 4, 1, 1, 1] but got {}".format(psv_encoding("abcdabcd"))


def test_char_ranks():
	assert compute_order_preserving_weak_encoding("") == []
	assert compute_order_preserving_weak_encoding("a") == [0]
	assert compute_order_preserving_weak_encoding("aa") == [0, 1], "expected [0, 1] but got {}".format(compute_order_preserving_encoding("aa"))
	assert compute_order_preserving_weak_encoding("ab") == [0, 1]
	assert compute_order_preserving_weak_encoding("ba") == [1, 0]
	assert compute_order_preserving_weak_encoding("abc") == [0, 1, 2]
	assert compute_order_preserving_weak_encoding("cba") == [2, 1, 0]
	assert compute_order_preserving_weak_encoding("banana") == [3, 0, 4, 1, 5, 2]
	assert compute_order_preserving_weak_encoding("aaaa") == [0, 1, 2, 3]
	assert compute_order_preserving_weak_encoding("abcdabcd") == [0, 2, 4, 6, 1, 3, 5, 7]

	assert compute_order_preserving_encoding("") == []
	assert compute_order_preserving_encoding("a") == [0]
	assert compute_order_preserving_encoding("aa") == [0, 0], "expected [0, 1] but got {}".format(compute_order_preserving_encoding("aa"))
	assert compute_order_preserving_encoding("ab") == [0, 1]
	assert compute_order_preserving_encoding("ba") == [1, 0]
	assert compute_order_preserving_encoding("abc") == [0, 1, 2]
	assert compute_order_preserving_encoding("cba") == [2, 1, 0]
	assert compute_order_preserving_encoding("banana") == [1, 0, 2, 0, 2, 0]
	assert compute_order_preserving_encoding("aaaa") == [0, 0, 0, 0]
	assert compute_order_preserving_encoding("abcdabcd") == [0, 1, 2, 3, 0, 1, 2, 3]



def compute_prev_encoding(s):
	"""
	Compute the prev-encoding of a string.
	"""
	prev_indices = {}
	encoding = []
	for i, char in enumerate(s):
		if char in prev_indices:
			encoding.append(i - prev_indices[char])
		else:
			encoding.append(0)
		prev_indices[char] = i
	return encoding

def is_square_free(minlength, encoder, T):
	"""
	Check if the string T is parameterized square-free.
	"""
	n = len(T)

	# Iterate over all substrings of even length
	for start in range(n):
		for length in range(minlength*2, n - start + 1, 2):  # Ensure length is even
			m = length
			mid = start + m // 2
			end = start + m

			# Split into two halves
			S1 = T[start:mid]
			S2 = T[mid:end]

			# Check if their prev-encodings are identical
			if encoder(S1) == encoder(S2):
				# print(f'square found at {start} with length {length}: {S1} and {S2}')
				return False
	return True

def is_cube_free(minlength, encoder, T):
	"""
	Check if the string T is parameterized cube-free.
	"""
	n = len(T)

	# Iterate over all substrings of length divisible by 3
	for start in range(n):
		for length in range(minlength * 3, n - start + 1, 3):  # Ensure length divisible by 3
			m = length
			third1 = start + m // 3
			third2 = start + 2 * m // 3
			end = start + m

			# Split into three equal parts
			S1 = T[start:third1]
			S2 = T[third1:third2]
			S3 = T[third2:end]

			# Check if all three encoded parts are identical
			if encoder(S1) == encoder(S2) == encoder(S3):
				# print(f'cube found at {start} with length {length}: {S1}, {S2}, {S3}')
				return False
	return True


def test_compute_prev_encoding():
	"""Tests for the compute_prev_encoding function."""
	# Test 1: Simple case with unique characters
	assert compute_prev_encoding("abc") == [0, 0, 0], "Test 1 Failed"

	# Test 2: Repeated characters
	assert compute_prev_encoding("abca") == [0, 0, 0, 3], "Test 2 Failed"

	# Test 3: Complex case with multiple repeats
	assert compute_prev_encoding("abacabad") == [0, 0, 2, 0, 2, 4, 2, 0], "Test 3 Failed"

	# Test 4: Single character string
	assert compute_prev_encoding("a") == [0], "Test 4 Failed"

	# Test 5: Empty string
	assert compute_prev_encoding("") == [], "Test 5 Failed"

	# Test 6: All characters are the same
	assert compute_prev_encoding("aaaa") == [0, 1, 1, 1], "Test 6 Failed"

	# print("All tests passed for compute_prev_encoding!")


test_char_ranks()
test_compute_prev_encoding()
test_psv_encoding()
