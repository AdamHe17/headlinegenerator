# coding: utf-8

import requests, json, string, unicodedata

# sample = "President Trump on Saturday accused former President Barack Obama of tapping his phones at Trump Tower the month before the election, leveling the explosive allegation without offering any evidence.\nMr. Trump called his predecessor a “bad (or sick) guy” on Twitter as he fired off a series of messages claiming that Mr. Obama “had my ‘wires tapped.’” He likened the supposed tapping to “Nixon/Watergate” and “McCarthyism,” though he did not say where he had gotten his information.A spokesman for Mr. Obama said any suggestion that the former president had ordered such surveillance was “simply false.”\nDuring the 2016 campaign, the federal authorities began an investigation into links between Trump associates and the Russian government, an issue that continues to dog Mr. Trump. His aides declined to clarify on Saturday whether the president’s allegations were based on briefings from intelligence or law enforcement officials — which could mean that Mr. Trump was revealing previously unknown details about the investigation — or on something else, like a news report.\nBut a senior White House official said that Donald F. McGahn II, the president’s chief counsel, was working to secure access to what Mr. McGahn believed to be an order issued by the Foreign Intelligence Surveillance Court authorizing some form of surveillance related to Mr. Trump and his associates.\nThe official offered no evidence to support the notion that such an order exists. It would be a highly unusual breach of the Justice Department’s traditional independence on law enforcement matters for the White House to order it to turn over such an investigative document.\nAny request for information from a top White House official about a continuing investigation would be a stunning departure from protocols intended to insulate the F.B.I. from political pressure. It would be even more surprising for the White House to seek information about a case directly involving the president or his advisers, as does the case involving the Russia contacts.\nAfter the White House received heavy criticism for the suggestion that Mr. McGahn would breach Justice Department independence, a different administration official said that the earlier statements about his efforts had been overstated. The official said the counsel’s office was looking at whether there was any legal possibility of gleaning information without impeding or interfering with an investigation. The counsel’s office does not know whether an investigation exists, the official said.\nLast month, Reince Priebus, the White House chief of staff, came under fire for asking a top F.B.I. official to publicly rebut news reports about contacts between Trump campaign officials and the Russian government.\nSean Spicer, the White House press secretary, said in a statement that the “White House counsel is reviewing what options, if any, are available to us.” Mr. McGahn did not respond to a request for comment. He was traveling on Saturday to Florida to join the president at his estate, Mar-a-Lago.\nThe president’s decision on Saturday to lend the power of his office to accusations against his predecessor of politically motivated wiretapping — without offering any proof — was remarkable, even for a leader who has repeatedly shown himself willing to make assertions that are false or based on dubious sources.\nIt would have been difficult for federal agents, working within the law, to obtain a wiretap order to target Mr. Trump’s phone conversations. It would have meant that the Justice Department had gathered sufficient evidence to convince a federal judge that there was probable cause to believe Mr. Trump had committed a serious crime or was an agent of a foreign power, depending on whether it was a criminal investigation or a foreign intelligence one.\nFormer officials pointed to longstanding laws and procedures intended to ensure that presidents cannot wiretap a rival for political purposes.\n“A cardinal rule of the Obama administration was that no White House official ever interfered with any independent investigation led by the Department of Justice,” said Kevin Lewis, a spokesman for Mr. Obama. “As part of that practice, neither President Obama nor any White House official ever ordered surveillance on any U.S. citizen.”\nMr. Trump asserted just the opposite in a series of five Twitter messages beginning just minutes before sunrise in Florida, where the president is spending the weekend.\nIn the first message, the president said he had “just found out” that “Obama had my ‘wires tapped’ in Trump Tower” before the election. Mr. Trump’s reference to “wires tapped” raised the possibility that he was referring to some other type of electronic surveillance and was using the idea of phone tapping loosely."

def get_key_phrases(sample):
	endpoint = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases"
	api_key = "9d338b0731454e45bbf22cc2765d6fb8"

	headers = {
	    # Request headers
	    'Content-Type': 'application/json',
	    'Ocp-Apim-Subscription-Key': api_key
	}

	data = {"documents": [{"language": "en", "id": "string", "text": sample}]}
	r = requests.post(endpoint, headers=headers, data=json.dumps(data))

	d = r.json()
	return d["documents"][0]["keyPhrases"]


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode("utf-8")

def tokenize(s):
	accepted = string.ascii_lowercase + string.ascii_uppercase + " $%-'’"
	new_s = ''
	for char in remove_accents(s):
		char = char.decode('utf-8')
		if char in accepted:
			new_s += char
		elif char != '-':
			new_s += ' '
	return new_s.split()

def find_phrase(p, tokens):
	p_tokens = tokenize(p)
	return [(i, i+len(p_tokens)) for i in range(len(tokens)) if tokens[i:i+len(p_tokens)] == p_tokens]

def find_clusters(phrases, sample, sort_by_score=False):
	tokens = tokenize(sample)
	in_bigram = [0 for i in range(len(tokens))]

	for p in phrases:
		locs = find_phrase(p, tokens)
		for l in locs:
			start = l[0]
			end = l[1]
			lower = max(start - 1, 0)
			upper = min(end + 1, len(tokens) - 1)
			in_bigram[start:end] = list(map(lambda x: x + 2, in_bigram[start:end]))
			if lower is not start:
				in_bigram[lower] += 1
			if upper is not end:
				in_bigram[upper] += 1

	# turn boolean into clusters
	clusters = []
	current = ""
	weight = 0
	for i in range(len(tokens)):
		t = tokens[i]
		if in_bigram[i] >= 1:
			current += t
			current += " "
			weight += in_bigram[i]
		elif current is not "":
			# Function for scoring cluster "value" with heuristic
			# currently done by subtracting index of final word from sum of overlap values
			val = 1.8 * weight - 0.7 * i ** 1.2
			clusters.append((current[:-1], val))

			current = ""
			weight = 0


	if sort_by_score:
		return list(map(lambda x: x[0], sorted(clusters, key=lambda x: -x[1])))

	return list(map(lambda x: x[0], clusters))

def score_cluster(cluster, phrases):
	"""
	Assumes that phrases are in some order of significance, where phrases earlier in the list are more significant than those later in the list.
	"""

	score = 0

	for i in range(len(phrases)):
		p = phrases[i]
		if p in cluster:
			score += len(phrases) - i

	return score

# phrases = get_key_phrases(sample)
# print(find_clusters(phrases, sample))
