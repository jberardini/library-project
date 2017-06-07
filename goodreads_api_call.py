import xmltodict
import requests
from os import environ
import rauth

GOODREADS_KEY = environ["GOODREADS_KEY"]
GOODREADS_SECRET = environ["GOODREADS_SECRET"]

goodreads = rauth.OAuth1Service(
	consumer_key = GOODREADS_KEY,
	consumer_secret = GOODREADS_SECRET,
	name = 'goodreads',
	access_token_url = 'http://www.goodreads.com/oauth/access_token',
	authorize_url = 'http://www.goodreads.com/oauth/authorize',
        request_token_url = 'http://www.goodreads.com/oauth/request_token',
	base_url = 'http://www.goodreads.com/' 
)

request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

authorize_url = goodreads.get_authorize_url(request_token)

print "Visit this URL in your browser " + authorize_url
accepted = 'n'
while accepted == 'n':
	print "Have you authorized me? (y/n) "
	accepted = raw_input()

session = goodreads.get_auth_session(request_token, request_token_secret)

def get_goodreads_book_id(books_list):

	book_ids = []

	for book_title, author in books_list.iteritems():
		payload = {'key': GOODREADS_KEY, 'q': book_title}
		response = requests.get("https://www.goodreads.com/search/index.xml", params=payload)
		search_result = xmltodict.parse(response.text)
		all_matches = search_result['GoodreadsResponse']['search']['results']['work']
		

		for match in all_matches:
			goodreads_author_name = match['best_book']['author']['name']
			library_last_name, library_first_name = books_list[book_title].split(', ')
			library_author_name = "{} {}".format(library_first_name, library_last_name)

			if goodreads_author_name == library_author_name:
				if match['ratings_count']['#text'] > 1000:
					goodreads_id = match['best_book']['id']['#text']
					book_ids.append(goodreads_id)
					book_titles.append(match['best_book'])

				break

	return book_ids

def add_book_to_shelf(book_ids, session):

	for book_id in book_ids:
		data = {'name': 'to-read', 'book_id': book_id}
		response = session.post('http://www.goodreads.com/shelf/add_to_shelf.xml', data)


add_book_to_shelf([18114322], session)






