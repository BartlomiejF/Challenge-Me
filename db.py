import sqlite3

import os, click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            '/home/Bartlomiej/instance/challenge-me.sqlite'
            )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    if not os.listdir('/home/Bartlomiej/instance'):
       with current_app.open_resource('/home/Bartlomiej/challengeme/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))