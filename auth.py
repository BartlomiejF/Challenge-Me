import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from challengeme.db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passwd']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('/register.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['passwd']
		db = get_db()
		error = None
		user = db.execute(
		'SELECT * FROM user WHERE username == ?', (username,)
		).fetchone()
	
		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'
	
		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect('/')
				
		flash(error)

	return render_template('login.html')
    
@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	db=get_db()
	if user_id is None:
		g.user = None
	else:
		g.user = db.execute(
		'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()
		discussions=db.execute(
		f"""SELECT DISTINCT challenges.id, gamedate, gamename FROM challenges
		LEFT JOIN answer ON answer.chal_id = challenges.id
		JOIN games ON challenges.game_id = games.id
		WHERE challenges.author_id={user_id} OR answer.author_id={user_id}"""
		).fetchall()
		g.disc=discussions
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
    
