from os import environ
import rauth
import goodreads

GOODREADS_KEY = environ["GOODREADS_KEY"]
GOODREADS_SECRET = environ["GOODREADS_SECRET"]

print GOODREADS_SECRET

gr = goodreads.GoodreadsApi(GOODREADS_KEY, GOODREADS_SECRET)

gr.authorize()

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

def add_book_to_shelf(book_ids):

	for book_id in book_ids:
		gr.add_book_to_shelf(book_id, "to-read")


add_book_to_shelf([18114323])






