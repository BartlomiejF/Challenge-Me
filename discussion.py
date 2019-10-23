from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from challengeme.db import get_db
from challengeme.auth import login_required

bp = Blueprint('discussion', __name__)

@bp.route('/challengeanswer/<int:nb>', methods=['GET', 'POST'])
@login_required
def challengeanswer(nb):
	db = get_db()
	call = db.execute(
	f"""SELECT challenges.id, gamedate, format, body, username, gamename FROM challenges
	JOIN user ON challenges.author_id = user.id
	JOIN games ON challenges.game_id = games.id
	WHERE challenges.id = {nb}
	"""
	).fetchone()
	
	answers = db.execute(
	f"""SELECT created, post, username FROM answer
	JOIN user ON answer.author_id = user.id
	WHERE answer.chal_id = {nb}
	ORDER BY created DESC
	"""
	).fetchall()

	if request.method == 'POST':
		user_id = int(g.user['id'])
		ans = request.form['answer'].strip()
		chal_id = int(call['id'])
		ret = [user_id, ans, chal_id]
		
		if ans:
			db.execute(
			'INSERT INTO answer (author_id, post, chal_id) VALUES (?, ?, ?)', (user_id, ans, chal_id)
			)
			db.commit()
			return redirect(url_for('discussion.challengeanswer', nb=nb))

	return render_template('discussion.html', call=call, answers=answers)
