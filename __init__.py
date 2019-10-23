import os

from flask import Flask, flash, g, redirect, render_template, request, url_for, session
from challengeme.db import get_db


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
	SECRET_KEY = b'',
	DATABASE = os.path.join(app.instance_path, 'challenge-me.sqlite'),
	)

	if test_config is None:
	# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
	# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	with app.app_context():
	    db.init_db()

	from . import challenger
	app.register_blueprint(challenger.challenger)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import mapper
	app.register_blueprint(mapper.mapper)

	from . import discussion
	app.register_blueprint(discussion.bp)

	@app.route('/')
	@app.route('/index')
	def index():
		db=get_db()
		chalnum=len(db.execute(
		'SELECT id FROM challenges'
		).fetchall())
		return render_template('index.html', num=chalnum)

	return app

app=create_app()