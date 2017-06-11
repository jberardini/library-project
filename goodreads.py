import rauth
import xmltodict

API_BASE_URL = 'http://www.goodreads.com/'

class GoodreadsApi():
	def __init__(self, key, secret):

                self.key = key
		self.service = rauth.OAuth1Service(
			consumer_key = key,
			consumer_secret = secret,
			name = 'libsync',
			access_token_url = API_BASE_URL + 'oauth/access_token',
			authorize_url = API_BASE_URL + 'oauth/authorize',
		        request_token_url = API_BASE_URL + 'oauth/request_token',
			base_url = API_BASE_URL
		)

	def authorize(self):
		request_token, request_token_secret = self.service.get_request_token(header_auth=True)
		authorize_url = self.service.get_authorize_url(request_token)

		print "Visit this URL in your browser " + authorize_url
		accepted = 'n'
		while accepted == 'n':
			print "Have you authorized me? (y/n) "
			accepted = raw_input()

		self.session = self.service.get_auth_session(request_token, request_token_secret)

	def add_book_to_shelf(self, book_id, shelf_name):
		data = {'name': shelf_name, 'book_id': book_id}
                api_url = API_BASE_URL + 'shelf/add_to_shelf.xml'
		response = self.session.post(api_url, data)

		return response.status_code == 201

        def search_by_title(self, book_title):
                """takes a book title and returns a list of dicts like:
                [
                  {
                    id: integer
                    books_count: integer
                    ratings_count: integer
                    text_reviews_count: integer
                    original_publication_year: integer
                    original_publication_month: integer
                    original_publication_day: integer
                    average_rating: float
                    best_book: {
                      id: integer
                      title: string
                      author: {
                        id: integer
                        name: string

                      }
                      image_url: string
                      small_image_url: string
                    }
                  }
                ]
                """
                payload = {'q': book_title}
		response = self.session.get(API_BASE_URL + 'search/index.xml', params=payload)
                print response.status_code
                print response.text
		search_result = xmltodict.parse(response.text)
		return search_result['GoodreadsResponse']['search']['results']['work']
