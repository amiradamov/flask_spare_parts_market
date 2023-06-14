from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash
# from db import get_db

# Create a Flask Instance
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return "<h1>Hello {}</h1>".format(name)
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)

#         db = get_db()
#         cursor = db.cursor()
#         cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)',
#                        (username, hashed_password))
#         db.commit()
#         cursor.close()

#         return 'User registered successfully!'
#     return render_template('register.html')

if __name__ == "__main__":
    app.run(debug = True)

