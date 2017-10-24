import random
import re
import os

def clean_file(text):
	file = open(text, "r+")
	file_data = file.read()
	file_data = re.sub(" +", " ", file_data).lstrip()
	file.seek(0)
	file.truncate()
	file.write(file_data)

def make_markov(text):
	file = open(text)
	file_data = file.read()
	modified_data = file_data.replace("\n", "\n ")
	chain = {}
	words = modified_data.split(" ")
	w1, w2 = None, None
	chain[(w1, w2)] = chain.get((w1, w2), []) + [words[0]]
	for index in range(len(words)):
		word = words[index]
		w1, w2 = w2, word
		if index + 1 < len(words):
			next_word = words[index + 1]
			chain[(w1, w2)] = chain.get((w1, w2), []) + [next_word]
		else:
			chain[(w1, w2)] = chain.get((w1, w2), []) + [None]
	return chain

def combine_markov(markov_list):
	first = markov_list[0]
	for addition in markov_list[1:]:
		for key, value in addition.items():
			first[key] = first.get(key, []) + value
	return first

def make_poem(max_length, chain):
	assert max_length > 0, "Length of poem must be a nonnegative integer!"
	store_max = max_length
	prev1, prev2 = None, None
	poem = ""
	while max_length:
		possible_words = chain.get((prev1, prev2), [])
		assert len(possible_words) > 0, "Strange Error Occurred!"
		new_word = random.choice(possible_words)
		if new_word == None:
			break
		elif "\n" in new_word:
			poem += new_word
		else:
			poem += new_word + " "
		prev1, prev2 = prev2, new_word
		max_length -= 1
	if poem.lstrip():
		return poem
	else:
		return new_make_poem(store_max, chain)

def poetry(max_length, texts):
	for text in texts:
		clean_file(text)
	chains = [make_markov(text) for text in texts]
	chain = combine_markov(chains)
	return make_poem(max_length, chain)

print(poetry(20, ["rupis/" + file for file in os.listdir(os.getcwd()+"/rupis/")]))