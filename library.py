import mechanize
import cookielib
from bs4 import BeautifulSoup
import requests
import html2text
import sys

class Library():
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')


		self.br = mechanize.Browser()

		cj = cookielib.LWPCookieJar()
		self.br.set_cookiejar(cj)

		self.br.set_handle_equiv(True)
		self.br.set_handle_gzip(True)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_robots(False)
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		self.br.addheaders = [('User-agent', 'Chrome')]

	def log_in(self, barcode, pin):

		self.br.open('https://sfpl.bibliocommons.com/user/login')

		self.br.select_form(nr=2)

		self.br.form['name'] = barcode
		self.br.form['user_pin'] = pin

		self.br.submit()

	def scrape_shelf(self):
		r = requests.get('https://sfpl.bibliocommons.com/collection/show/718567772_jilberar/library/for_later')

		data = r.text

		soup = BeautifulSoup(data, "html5lib")

		mydivs = soup.findAll('div', {'class': 'info'})

		self.my_books = {}

		for div in mydivs:

			book_title= div.find('a')['title']
			book_title = book_title[:-7]

			author = div.find(testid='author_search')
			author = author.string

			self.my_books[book_title] = author

		return self.my_books