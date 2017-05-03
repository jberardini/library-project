# -*- coding: utf-8 -*-


import mechanize
import cookielib
from bs4 import BeautifulSoup
import requests
import html2text


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


br.form['name'] = 'barcode'
br.form['user_pin'] = 'pin'

response = br.submit()

