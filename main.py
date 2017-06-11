from os import environ
import rauth
import goodreads
import library

GOODREADS_KEY = environ["GOODREADS_KEY"]
GOODREADS_SECRET = environ["GOODREADS_SECRET"]
LIBRARY_BARCODE = environ["LIBRARY_BARCODE"]
LIBRARY_PIN = environ["LIBRARY_PIN"]

lib = library.Library()

lib.log_in(LIBRARY_BARCODE, LIBRARY_PIN)

library_books = lib.scrape_shelf()


gr = goodreads.GoodreadsApi(GOODREADS_KEY, GOODREADS_SECRET)

gr.authorize()

def get_goodreads_book_id(books_list):

	book_ids = []

	for book_title, author in books_list.iteritems():
		all_matches = gr.search_by_title(book_title)

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






