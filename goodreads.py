import rauth
import xmltodict

API_BASE_URL = 'http://www.goodreads.com/'

class GoodreadsApi():
	def __init__(self, key, secret):
                self.consumer_key = key
                self.consumer_secret = secret
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
                try:
                        session_file = open(".grsession", "r")
                        saved_session = session_file.readline()
                        [access_token, access_token_secret] = saved_session.split(":")
                        print("got session! (" + access_token + ", " + access_token_secret + ")")
                        self.session = rauth.OAuth1Session(self.consumer_key, self.consumer_secret, access_token, access_token_secret)
                except IOError as err:
                        session_file = open(".grsession", "w")
                        # have to open a new session
                        request_token, request_token_secret = self.service.get_request_token(header_auth=True)
                        authorize_url = self.service.get_authorize_url(request_token)

		        print "Visit this URL in your browser " + authorize_url
		        accepted = 'n'
		        while accepted == 'n':
			        print "Have you authorized me? (y/n) "
			        accepted = raw_input()

                        access_tok, access_tok_secret = self.service.get_access_token(request_token, request_token_secret)
                        self.session = rauth.OAuth1Session(self.consumer_key, self.consumer_secret, access_tok, access_tok_secret)

                        session_file.write(access_tok + ":" + access_tok_secret)
                        session_file.close()

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
