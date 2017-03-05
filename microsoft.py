import requests, json, string, unicodedata

# sample = "WEST PALM BEACH, Fla. — President Trump on Saturday accused former President Barack Obama of tapping his phones at Drumpf Tower the month before the election, leveling the explosive allegation without offering any evidence.\nMr. Trump called his predecessor a “bad (or sick) guy” on Twitter as he fired off a series of messages claiming that Mr. Obama “had my ‘wires tapped.’” He likened the supposed tapping to “Nixon/Watergate” and “McCarthyism,” though he did not say where he had gotten his information."

# phrases = ['President Trump', 'President Barack Obama', 'election', 'phones', 'Nixon', 'Watergate', 'Saturday accused', 'Drumpf Tower', 'month', 'explosive allegation', 'McCarthyism', 'Twitter', 'guy', 'WEST PALM BEACH', 'predecessor', 'series of messages', 'evidence', 'wires', 'information']

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
	return ["documents"][0]["keyPhrases"]


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode("utf-8")

def tokenize(s):
	accepted = string.ascii_lowercase + string.ascii_uppercase + ' $%-'
	new_s = ''
	for char in remove_accents(s):
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
	in_bigram = [False for i in range(len(tokens))]

	for p in phrases:
		locs = find_phrase(p, tokens)
		for l in locs:
			start = max(l[0] - 1, 0)
			end = min(l[1] + 1, len(tokens) - 1)
			in_bigram[start:end] = [True for i in range(start, end)]

	# turn boolean into clusters
	clusters = []
	current = ""
	for i in range(len(tokens)):
		t = tokens[i]
		if in_bigram[i]:
			current += t
			current += " "
		elif current is not "":
			clusters.append(current[:-1])
			current = ""
	
	if sort_by_score:
		return sorted(clusters, key=lambda x: -score_cluster(x, phrases))
	
	return clusters

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

	