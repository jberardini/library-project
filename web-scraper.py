# -*- coding: utf-8 -*-


import mechanize
import cookielib
from bs4 import BeautifulSoup
import requests
import html2text
import sys
from os import environ
from goodreads_api_call import get_goodreads_book_id

reload(sys)
sys.setdefaultencoding('utf-8')


br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

br.open('https://sfpl.bibliocommons.com/user/login')


br.select_form(nr=2)



br.form['name'] = environ['LIBRARY_BARCODE']
br.form['user_pin'] = environ['LIBRARY_PIN']

br.submit()

r = requests.get('https://sfpl.bibliocommons.com/collection/show/718567772_jilberar/library/for_later')

data = r.text

soup = BeautifulSoup(data, "html5lib")

mydivs = soup.findAll('div', {'class': 'info'})

my_books = {}

for div in mydivs:

	book_title= div.find('a')['title']
	book_title = book_title[:-7]

	author = div.find(testid='author_search')
	author = author.string

	my_books[book_title] = author

get_goodreads_book_id(my_books)



