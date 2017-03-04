import pickle

"""HOW TO RUN FROM COMMAND LINE:

>python generateprobabilities.py
>>>from generateprobabilities import *
>>>count_all_occurrences(ANY_NEW_ARTICLES.pkl, False)


*Note, if we fuck up our LEXICON.pkl, we can just clear 
it from the beginning by setting the "clear" parameter to True

"""



def add_word_to_headline_words(word, HEADLINE_WORDS):
	"adds the word to our dictionary of ALL headline words"
	HEADLINE_WORDS[word] = {}
	HEADLINE_WORDS[word]["headline"] = {}
	HEADLINE_WORDS[word]["gap"] = {}

def add_word_to_gap_words(word, GAP_WORDS):
	"adds the word to our dictionary of ALL gap words"
	GAP_WORDS[word] = {}
	GAP_WORDS[word]["headline"] = {}
	GAP_WORDS[word]["gap"] = {}


def make_headline_dict(headline):
	"""makes a dictionary out of the tokenized headline list for fast hash lookup"""

	headline_dict = {}
	for word in headline:
		headline_dict[word] = 1
	return headline_dict


def count_occurences_in_story(headline, story, HEADLINE_WORDS, GAP_WORDS):
	"""for each word in our story, determine whether it is a headline or a gap word. 
	If it is a headline word, determine whether the NEXT word is headline or gap. 
	Update the counts in the table accordingly"""

	evaluated_story = []

	for i in range(0, len(story)):
		if len(headline) > 0:
			if story[i] == headline[0]:
				evaluated_story.append([story[i],True])
				headline = headline[1::]
			else:
				evaluated_story.append([story[i],False])
		else:
			evaluated_story.append([story[i], False])


	for i in range(0, len(evaluated_story)-1):

		if not evaluated_story[i][1] and not evaluated_story[i+1][1]:
			if evaluated_story[i][0] not in GAP_WORDS:
				add_word_to_gap_words(evaluated_story[i][0], GAP_WORDS)
			if evaluated_story[i+1][0] not in GAP_WORDS[evaluated_story[i][0]]["gap"]:
				GAP_WORDS[evaluated_story[i][0]]["gap"][evaluated_story[i+1][0]] = 1
			else:
				GAP_WORDS[evaluated_story[i][0]]["gap"][evaluated_story[i+1][0]] += 1



		elif not evaluated_story[i][1] and evaluated_story[i+1][1]:
			if evaluated_story[i][0] not in GAP_WORDS:
				add_word_to_gap_words(evaluated_story[i][0], GAP_WORDS)
			if evaluated_story[i+1][0] not in GAP_WORDS[evaluated_story[i][0]]["headline"]:
				GAP_WORDS[evaluated_story[i][0]]["headline"][evaluated_story[i+1][0]] = 1
			else:
				GAP_WORDS[evaluated_story[i][0]]["headline"][evaluated_story[i+1][0]] += 1


		elif evaluated_story[i][1] and not evaluated_story[i+1][1]:
			if evaluated_story[i][0] not in HEADLINE_WORDS:
				add_word_to_headline_words(evaluated_story[i][0], HEADLINE_WORDS)
			if evaluated_story[i+1][0] not in HEADLINE_WORDS[evaluated_story[i][0]]["gap"]:
				HEADLINE_WORDS[evaluated_story[i][0]]["gap"][evaluated_story[i+1][0]] = 1
			else:
				HEADLINE_WORDS[evaluated_story[i][0]]["gap"][evaluated_story[i+1][0]] += 1


		elif evaluated_story[i][1] and evaluated_story[i+1][1]:
			if evaluated_story[i][0] not in HEADLINE_WORDS:
				add_word_to_headline_words(evaluated_story[i][0], HEADLINE_WORDS)
			if evaluated_story[i+1][0] not in HEADLINE_WORDS[evaluated_story[i][0]]["headline"]:
				HEADLINE_WORDS[evaluated_story[i][0]]["headline"][evaluated_story[i+1][0]] = 1
			else:
				HEADLINE_WORDS[evaluated_story[i][0]]["headline"][evaluated_story[i+1][0]] += 1


def count_all_occurrences(new_articles, clear):
	"iterate through all of our stories and headlines"
	f = open(new_articles,'rb')
	article_data = pickle.load(f)
	f.close()

	f = open("LEXICON.pkl",'rb')
	lexicon = pickle.load(f)
	f.close()

	HEADLINE_WORDS = lexicon[0]
	GAP_WORDS = lexicon[1]

	if clear:
		HEADLINE_WORDS = {}
		GAP_WORDS = {}


	start_hdline_prob = 0.0

	for i in range(0, len(article_data)):
		count_occurences_in_story(article_data[i][0], article_data[i][1], HEADLINE_WORDS, GAP_WORDS)
		if article_data[i][1][0] in article_data[i][0]:
			start_hdline_prob += 1.0

	start_hdline_prob = start_hdline_prob/len(article_data)

	f = open("LEXICON.pkl", 'wb')
	pickle.dump([HEADLINE_WORDS, GAP_WORDS, start_hdline_prob], f)
	f.close()
