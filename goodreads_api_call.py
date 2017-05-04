from os import environ
import xmltodict
import requests

api_key = environ["GOODREADS_KEY"]


def get_goodreads_book_id(books_list):

	for book in books_list:
		payload = {'key': api_key, 'q': book}
		response = requests.get("https://www.goodreads.com/search/index.xml", params=payload)
		search_result = xmltodict.parse(response.text)
		all_matches = search_result['GoodreadsResponse']['search']['results']['work']
		



