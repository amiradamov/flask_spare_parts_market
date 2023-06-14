from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash
# from db import get_db

# Create a Flask Instance
app = Flask(__name__)


# FILTERS!!!

# safe
# capitalize
# lower
# upper
# title
# trim
# striptags

@app.route('/')
def index():
    first_name = 'John'
    stuff = 'This is <strong>Bold</strong> Text'
    stuff1 = 'this is Bold Text'

    favorite_pizza = ["Pepperoni", "CHeese", "Something Else", 32]
    return render_template('index.html', first_name = first_name, stuff = stuff, stuff1 = stuff1, favorite_pizza = favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)

# Create Custom Error Pages
if __name__ == "__main__":
    app.run(debug = True)

