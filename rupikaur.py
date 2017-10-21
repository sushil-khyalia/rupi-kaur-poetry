import random
import re

def clean_file(text):
	file = open(text, "r+")
	file_data = file.read()
	# for i in range(len(file_data) - 1):
	# 	if file_data[i: i + 2] == "  ":
	# 		file_data = file_data[:i] + " " + file_data[i + 2:]
	file_data = re.sub(" +", " ", file_data).lstrip()
	file.seek(0)
	file.truncate()
	file.write(file_data)

def make_markov(text):
	file = open(text)
	file_data = file.read()
	chain = {}

	def find_end(file_data):
		if file_data[0] == "\n":
			return 1
		space = file_data.find(" ", 1)
		newline = file_data.find("\n", 1)
		if space == -1:
			if newline == -1:
				return len(file_data)
			else:
				return newline
		else:
			if newline == -1:
				return space
			else:
				return min(newline, space)

	while file_data:
		end_character = find_end(file_data)
		this_word = file_data[:end_character]

		further = file_data[end_character:]
		if further:
			next_end_character = find_end(further)
			next_word = further[:next_end_character]
			if next_word[0] == " ":
				next_word = next_word[1:]
			chain[this_word] = chain.get(this_word, []) + [next_word]
		else:
			chain[this_word] = chain.get(this_word, []) + [None]
		file_data = file_data[end_character:]
		if file_data and file_data[0] == " ":
			file_data = file_data[1:]

	return chain

def combine_markov(markov_list):
	first = markov_list[0]
	for addition in markov_list[1:]:
		for key, value in addition.items():
			first[key] = first.get(key, []) + value
	return first

def make_poem(max_length, chain):
	assert max_length > 0, "Length of poem must be a nonnegative integer!"
	assert len(chain.get("\n", [])) > 0, "Chain must come from an input of more than one line!"
	previous_word = chain.get("\n", [])[random.randrange(0, len(chain.get("\n", [])))]
	if previous_word == None:
		return make_poem(max_length, chain)
	poem = previous_word + " "
	while max_length:
		possible = chain.get(previous_word, [])
		if possible == []:
			""" LOL I HID THIS ERROR """
			return make_poem(max_length, chain)
		else:
			new_word = possible[random.randrange(0, len(possible))]
		if new_word == None:
			return poem
		elif new_word == "\n":
			poem = poem[:-1]
			poem += new_word
		else:
			poem += new_word + " "
		previous_word = new_word
		max_length -= 1
	return poem

def poetry(max_length, texts):
	for text in texts:
		clean_file(text)
	chains = [make_markov(text) for text in texts]
	chain = combine_markov(chains)
	return make_poem(max_length, chain)

# print(poetry(250, ["davidessay.txt"]))
# print(poetry(100, ["shakespeare.txt"]))
# print(poetry(100, ["eliot.txt"]))
print(poetry(20, ["rupis/rupi1.txt", "rupis/rupi2.txt", "rupis/rupi3.txt", "rupis/rupi4.txt", "rupis/rupi5.txt", "rupis/rupi6.txt", "rupis/rupi7.txt", "rupis/rupi8.txt", "rupis/rupi9.txt", "rupis/rupi10.txt", "rupis/rupi11.txt", "rupis/rupi12.txt", "rupis/rupi13.txt", "rupis/rupi14.txt", "rupis/rupi15.txt", "rupis/rupi16.txt", "rupis/rupi17.txt", "rupis/rupi18.txt", "rupis/rupi19.txt", "rupis/rupi20.txt"]))