from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"
# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators = [DataRequired()])
    submit = SubmitField('Submit')

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

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")

    return render_template("name.html",
        name = name,
        form = form)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug = True)

