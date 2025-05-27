#!/usr/bin/env python3
""" """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import argparse

def compute_order_preserving_encoding(s: str) -> list[int]:
	sorted_indices = sorted(range(len(s)), key=lambda i: (s[i], i))
	rank = [0] * len(s)
	for r, i in enumerate(sorted_indices):
		rank[i] = r
	return rank

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
	assert compute_order_preserving_encoding("") == []
	assert compute_order_preserving_encoding("a") == [0]
	assert compute_order_preserving_encoding("aa") == [0, 1], "expected [0, 1] but got {}".format(compute_order_preserving_encoding("aa"))
	assert compute_order_preserving_encoding("ab") == [0, 1]
	assert compute_order_preserving_encoding("ba") == [1, 0]
	assert compute_order_preserving_encoding("abc") == [0, 1, 2]
	assert compute_order_preserving_encoding("cba") == [2, 1, 0]
	assert compute_order_preserving_encoding("banana") == [3, 0, 4, 1, 5, 2]
	assert compute_order_preserving_encoding("aaaa") == [0, 1, 2, 3]
	assert compute_order_preserving_encoding("abcdabcd") == [0, 2, 4, 6, 1, 3, 5, 7]




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
	test_char_ranks()
	test_compute_prev_encoding()
	test_psv_encoding()
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
