from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Flask Instance
app = Flask(__name__)

# Add Database

# For SQLITE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# For MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://amir:password@localhost/flask_tutorial'

# Secret key
app.config['SECRET_KEY'] = "my super secret key"
# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Json Thing
# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    favorite_color = db.Column(db.String(120))

    # Password
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        # error message
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def varify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    name = None
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", 
                            form=form,
                            name=name,
                            our_users=our_users)
    except:
        flash("Whoops! There was a problem deleting User")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", 
                            form=form,
                            name=name,
                            our_users=our_users)
# Create a Form User
class UserForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("Error! Looks like there is an error")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update,
                               )

# Create a Password Form Class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators = [DataRequired()])
    password_hash = PasswordField("What's Your Password", validators = [DataRequired()])
    submit = SubmitField('Submit')

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

#Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        # lookup user by email address
        pw_to_check = Users.query.filter_by(email=email).first()
        # check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)
    return render_template("test_pw.html",
        email = email,
        password = password,
        pw_to_check = pw_to_check,
        passed = passed,
        form = form)

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
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # hash password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash("User Added Succesfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
                           form=form,
                           name=name,
                           our_users=our_users)



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
