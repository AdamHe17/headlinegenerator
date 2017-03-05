import requests, json, en
from microsoft import *

sample = "On Saturday, workers in the middle of a union drive at the Nissan plant in Canton, Miss., stopped to hear from a special guest: Sen. Bernie Sanders. The onetime presidential candidate, now the Democratic caucus’s point man on political outreach, came to the “March on Mississippi” event both to help the United Automobile Workers’ campaign and to send a message about what opponents of President Drumpf should be doing.\n“What I’m going to be saying is that the facts are very clear, that workers in America who are members of unions earn substantially more, 27 percent more, than workers not in unions,” Sanders (I-Vt.) said in an interview before the speech. “They get pensions and better working conditions. I find it very remarkable that Nissan is allowing unions to form at its plants all over the world. Well, if they can be organized everywhere else, they can be organized in Mississippi.”\nIn a statement, new Democratic National Committee Chairman Tom Perez, the former U.S. labor secretary, lent his support to the rally and the union drive."

# sample = "The 39-year-old Sikh man was working on his car in his driveway in Kent, Wash., just south of Seattle, when a man walked up wearing a mask and holding a gun.\nAccording to a report in the Seattle Times, there was an altercation, and the gunman — a stocky, 6-foot-tall white man wearing a mask over the bottom part of his face — said “Go back to your own country” and pulled the trigger.\nAuthorities are investigating the shooting as a suspected hate crime, the newspaper reported.\nThe victim, whose name hasn’t been released, was shot in the arm at about 8 p.m. Friday and suffered injuries that are not life-threatening, the newspaper reported. The man who shot him is still on the loose. Kent Police have reached out to the FBI and other law enforcement agencies for help."


def headline(clusters, length):
	i = 0
	headline = clusters[0]
	lengths = list(map(lambda x: len(tokenize(x)), clusters))
	l = lengths[i]

	while l < length:
		i += 1
		headline += ', '
		headline += clusters[i]
		l += lengths[i]

	return clean_headline(headline)

def parts_of_speech(sample):
	endpoint = "https://westus.api.cognitive.microsoft.com/linguistics/v1.0/analyze"
	api_key = "3b1f167fa0f444aaab874f4fc749e0fa"

	headers = {
	    # Request headers
	    'Content-Type': 'application/json',
	    'Ocp-Apim-Subscription-Key': api_key
	}

	body = {
		"language" : "en",
		"analyzerIds" : ["4fa79af1-f22c-408d-98bb-b7d7aeef7f04"],
		"text" : sample 
	}

	r = requests.post(endpoint, headers=headers, data=json.dumps(body))
	return r.json()[0]['result']

def clean_headline(headline):
	tokens = tokenize(headline)
	# filter out stop words
	stop_words = ['a', 'an', 'and', 'are', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with', 'his', 'her', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

	tokens = [t for t in tokens if not t.lower() in stop_words]
	result = " ".join(tokens)

	# parts of speech analysis
	parts = parts_of_speech(result)

	# rules about ending and beginning
	bad_list = ["IN", "CC", "MD", "RP", "EX"] # could change

	while parts[-1] in bad_list:
		tokens = tokens[:-1]
		parts = parts[:-1]

	while parts[0] in bad_list:
		tokens = tokens[1:]
		parts = parts[1:]

	# could add other rules
	# make first letter uppercase, just in case
	tokens[0] = tokens[0].title()

	tokens = present_tense(tokens)

	return " ".join(tokens)

def present_tense(sentenceList):
	newlist = []
	for i in sentenceList:
		try:
			newlist.append(en.verb.present(i))
		except:
			newlist.append(i)
	return newlist




# phrases = get_key_phrases(sample)
# clusters = find_clusters(phrases, sample)

# print(headline(clusters, 10))
phrases = get_key_phrases(sample)
clusters = find_clusters(phrases, sample)
headline = headline(clusters, 10)
print headline