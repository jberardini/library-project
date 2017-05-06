from flask import Flask, jsonify, render_template, redirect, request, flash, session, g
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
import rauth
import urlparse
import urllib
from os import environ


app = Flask(__name__)

app.secret_key = 'secret'

GOODREADS_KEY = environ["GOODREADS_KEY"]
GOODREADS_SECRET = environ["GOODREADS_SECRET"]

app.jinja_env.undefined = StrictUndefined

goodreads = rauth.OAuth1Service(
		consumer_key = GOODREADS_KEY,
		consumer_secret = GOODREADS_SECRET,
		name = 'goodreads',
		request_token_url='http://www.goodreads.com/oauth/request_token',
		authorize_url = 'http://www.goodreads.com/oauth/authorize',
		access_token_url = 'http://www.goodreads.com/oauth/access_token',
		base_url = 'http://www.goodreads.com/' 
		)

request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

authorize_url = goodreads.get_authorize_url(request_token)

@app.route('/')
def index():


	return render_template('homepage.html', authorize_url=authorize_url)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

