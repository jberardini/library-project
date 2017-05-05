from flask import Flask, jsonify, render_template, redirect, request, flash, session, g
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = 'secret'

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():

	 return render_template('homepage.html')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

