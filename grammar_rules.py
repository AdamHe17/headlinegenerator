from linguistics import *

def delete_articles(headline):
	tokenized_headline = tokenize(headline)
	articles = ["a", "an", "the", "A", "An", "The"]
	for word in tokenized_headline:
		if word in articles:
			tokenized_headline.remove(word)
	return " ".join(tokenized_headline)


def conjunction_limiter(headline):
	tokenized_headline = tokenize(headline)	
	conjunctions = ["and", "but", "or", "for", "nor", "so", "yet", "And", "But", "Or", "For", "Nor", "So", "Yet"]
	first_word = tokenized_headline[0]

	while first_word in conjunctions:
		tokenized_headline = tokenized_headline[1:]
		print (tokenized_headline)
		first_word = tokenized_headline[0]

	last_word = tokenized_headline[-1]
	while last_word in conjunctions:
		print(tokenized_headline)
		tokenized_headline = tokenized_headline[:-1]
		last_word = tokenized_headline[-1]
	return " ".join(tokenized_headline)

def preposition_limiter(headline):
	tokenized_headline = tokenize(headline)	
	headline_parts_of_speech = parts_of_speech(headline)
	first_word = headline_parts_of_speech[0][0]
	while first_word in ["IN","RB"]:
		tokenized_headline = tokenized_headline[1:]
		headline_parts_of_speech[0] = headline_parts_of_speech[0][1:]
		first_word = headline_parts_of_speech[0][0]
	last_word = headline_parts_of_speech[0][-1]
	while headline_parts_of_speech[0][-1] in ["IN", "RB"]:
		tokenized_headline = tokenized_headline[:-1]
		headline_parts_of_speech[0] = headline_parts_of_speech[0][:-1]
		last_word = headline_parts_of_speech[0][-1]
	return " ".join(tokenized_headline)

def delete_auxillary_verbs(headline):
	tokenized_headline = tokenize(headline)
	headline_parts_of_speech = parts_of_speech(headline)
	for i in range (0, len(tokenized_headline)):
		if headline_parts_of_speech[0][i] == "MD":
			tokenized_headline.remove(tokenized_headline[i])
			headline_parts_of_speech = headline_parts_of_speech[0][0:i] + headline_parts_of_speech[0][i+1:] 
	return " ".join(tokenized_headline)
