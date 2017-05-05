from os import environ
import xmltodict
import requests

api_key = environ["GOODREADS_KEY"]


def get_goodreads_book_id(books_list):

	for book_title, author in books_list.iteritems():
		payload = {'key': api_key, 'q': book_title}
		response = requests.get("https://www.goodreads.com/search/index.xml", params=payload)
		search_result = xmltodict.parse(response.text)
		all_matches = search_result['GoodreadsResponse']['search']['results']['work']
		

		for match in all_matches:
			goodreads_lastname = match['best_book']['author']['name']
			library_last_name, library_first_name = books_list[book_title].split(', ')


			if goodreads_lastname == library_last_name:
				if match['ratings_count']['#text'] > 1000:
					goodreads_id = match['best_book']['id']['#text']


