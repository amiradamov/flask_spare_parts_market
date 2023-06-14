from flask import g
from flask_mysqldb import MySQL
from flask import current_app as app

def get_db():
    if 'db' not in g:
        g.db = MySQL(app)
    return g.db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.cursor().executescript(f.read().decode('utf8'))
    db.commit()

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()
        g.pop('db', None)
