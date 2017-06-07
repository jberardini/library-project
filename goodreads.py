import rauth

class GoodreadsApi():
	def __init__(self, key, secret):
		self.service = rauth.OAuth1Service(
			consumer_key = key,
			consumer_secret = secret,
			name = 'goodreads',
			access_token_url = 'http://www.goodreads.com/oauth/access_token',
			authorize_url = 'http://www.goodreads.com/oauth/authorize',
		    request_token_url = 'http://www.goodreads.com/oauth/request_token',
			base_url = 'http://www.goodreads.com/' 
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
		response = self.session.post('http://www.goodreads.com/shelf/add_to_shelf.xml', data)

		print response
		return response.status_code == 201


