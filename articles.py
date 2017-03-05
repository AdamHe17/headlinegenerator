from newspaper import Article
from urllib.request import Request, urlopen, URLError
import pickle, json, datetime, string, unicodedata, sys, time

apikey = '&api-key='
guardian_APIkey = apikey + '9eda4b7a-ea8a-4283-b85b-189f7211d7f8'
# nytimes_APIkey = apikey + '44c6ecf7957b48219259958b495b85a3'
# Articles =  pickle.load(open("save.pkl","rb"))
Articles = []
Query = 'politics'

def getArticlesYear(year):
	resetArticles(year)
	guardianArticles(year)

def resetArticles(year):
	"""
	Erases save.pkl
	WARNING: DON'T TOUCH
	"""
	print(year)
	pickle.dump([], open(str(year) + '-' + str(year+1) + ".pkl", "wb"))

def guardianArticles(year):
	yrsago = 2017 - year - 1
	today = datetime.date.today() - datetime.timedelta(days = 365*yrsago)
	i = 0
	numdays = 365
	goalday = today - datetime.timedelta(days = numdays)
	for i in range(numdays): # 500 days of news articles
		t = datetime.timedelta(days = i)
		search_day = str(today - t)
		print("current DAY:", search_day, "; Goal:", goalday, "; DAYS Left:", numdays - i, "; Current Size:", len(Articles))
		url = 'https://content.guardianapis.com/search?q=' + Query + '&type=article&from-date=' + search_day + '&to-date=' + search_day + guardian_APIkey
		addGuardianArticles(url)
		if i % 5 == 0:
			print("AUTOSAVING!")
			pickle.dump(Articles, open(str(year) + '-' + str(year+1) + ".pkl", "wb"))		
	pickle.dump(Articles, open(str(year) + '-' + str(year+1) + ".pkl", "wb"))

def addGuardianArticles(url):
	"""
	given API url, adds  10 (title, text) tuples to articles
	"""
	r = Request(url)
	try:
		response = urlopen(r)
		data = response.read()
	except (URLError, e):
	    print('No data. Got an error code:', e)

	j = json.loads(data.decode('utf-8'))
	j = j['response']['results']
	if len(j) == 0:
		print("No results found")
	all_ten = [j[i] for i in range(len(j))]
	for one_article in all_ten:
		a = Article(one_article['webUrl'])
		try_download(a)

		try:
			a.parse()
			title = one_article['webTitle']
			removeBar = title.find('|')
			if removeBar > 0:
				title = title[:removeBar]
			title = tokenize(title)
			text = tokenize(a.text)
			l = len(a.text)
			if (l >= 100) and len(title) > 0:
				Articles.append((title, text))
				# print("title:", title)
				# print("length:", l, "words")
			# else:
			# 	print("length", l ,"article skipped.")
		except:
			print("Unexpected error:", sys.exc_info()[0])
		
def try_download(article, tries = 0):
	try:
		article.download()
	except:
		if tries > 3:
			print("Unexpected error:", sys.exc_info()[0])
		else:
			try_download(article, tries + 1)

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

