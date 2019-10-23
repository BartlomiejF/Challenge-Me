from flask import Flask, flash, g, redirect, render_template, request, url_for, Blueprint
from challengeme.db import get_db

mapper=Blueprint('mapper', __name__)

@mapper.route('/opponentmap')
def opponentmap():
	db = get_db()

	challenges = db.execute(
	'SELECT chal.id, format, body, place_lat, place_lng, username, gamename, gamedate'
	' FROM challenges chal JOIN user u ON chal.author_id = u.id'
	' JOIN games ON chal.game_id = games.id'
	).fetchall()

	return render_template('map.html', challenges=challenges)
