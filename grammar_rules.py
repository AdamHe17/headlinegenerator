from linguistics import parts_of_speech


def delete_articles(tokenized_headline):
	articles = ["a", "an", "the", "A", "An", "The"]
	for word in tokenized_headline:
		if word in articles:
			tokenized_headline.remove(word)
	return tokenized_headline


def conjunction_limiter(tokenized_headline):
	conjunctions = ["and", "but", "or", "for", "nor", "so", "yet", "And", "But", "Or", "For", "Nor", "So", "Yet"]
	while tokenized_headline[0] in conjunctions:
		tokenized_headline.remove(tokenized_headline[0])
	while tokenized_headline[-1] in conjunctions:
		tokenized_headline.remove(tokenized_headline[-1])
	return tokenized_headline

def preposition_limiter(tokenized_headline):
	headline_parts_of_speech = parts_of_speech(" ".join(tokenized_headline))
	while headline_parts_of_speech[0][0] == "IN":
		tokenized_headline.remove(tokenized_headline[0])
		headline_parts_of_speech.remove(headline_parts_of_speech[0][0])
	while headline_parts_of_speech[0][-1] == "IN":
		tokenized_headline.remove(tokenized_headline[-1])
		headline_parts_of_speech.remove(headline_parts_of_speech[0][-1])
	return tokenized_headline		


