from flask import Flask, flash, g, redirect, render_template, request, url_for, Blueprint
from challengeme.db import get_db
from challengeme.auth import login_required

challenger=Blueprint('addchallenge', __name__)


@challenger.route('/addchallenge', methods=('GET', 'POST'))
@login_required
def addchallenge():
	db = get_db()
	gamelist = db.execute(
	'SELECT gamename FROM games'
	).fetchall()
	if request.method == 'POST':
		game = request.form['game']
		points = int(request.form['format'])
		try:
			(position_lat, position_lng)=request.form['position'][7:-1].split(',')
		except:
			return redirect('/')
		chal = request.form['challenge']
		year, month, day = request.form['date'].split('-')
		day = f'{year}-{month}-{day}'
		if position_lat!='' and position_lng!='':
			gameid = db.execute(
			'SELECT id FROM games WHERE gamename=?', (game,)
			).fetchone()
			db.execute(
			'INSERT INTO challenges (author_id, format, body, place_lat, place_lng, game_id, gamedate) VALUES (?, ?, ?, ?, ?, ?, strftime(?))',
			(g.user['id'],points, chal, float(position_lat.strip()), float(position_lng.strip()), gameid['id'], day)
			)
			db.commit()
			return redirect(url_for('mapper.opponentmap'))
		else:
			flash('You must set a marker on map.')

	return render_template('challenge.html', gamelist=gamelist)
