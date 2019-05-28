from datetime import datetime
import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN_USER=os.environ.get('ADMIN_USER'),
    ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD')
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.date}')"


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Role('{self.title}')"


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    country = db.Column(db.String(4), unique=True, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"Location('{self.country}', '{self.city}')"


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(20), unique=True, nullable=False)
    step1 = db.Column(db.Integer, nullable=False)
    step2 = db.Column(db.Integer, nullable=True)
    step3 = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Projects('{self.name}', '{self.step1}', '{self.step2}', '{self.step3}')"


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/master', methods=['GET', 'POST'])
def master_dashboard():
    return render_template('master_dashboard.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('account'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == os.environ.get('ADMIN_USER') and form.password.data == os.environ.get('ADMIN_PASSWORD'):
            flash('Welcome Master!', 'success')
            return redirect(url_for('master_dashboard'))
        elif form.email.data and form.password.data:
            flash('You have been logged in!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/account", methods=['GET', 'POST'])
def account():
    render_template('master_dashboard.html', title='Account')


if __name__ == '__main__':
    app.run(debug=True)
