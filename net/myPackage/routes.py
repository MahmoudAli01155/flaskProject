from flask import render_template, url_for, redirect, flash
from myPackage.__init__ import db, app
from myPackage.forms import RegistrationForm, LoginForm
from myPackage.models import Student
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required

bcrypt = Bcrypt()

# Homepage Endpoint
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',title="home page")

# About Endpoint
@app.route('/about')
def about():
    return render_template('about.html', title='about page')

# logout Endpoint
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# register Endpoint
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf8')
            student = Student(username=form.username.data,
                              email=form.email.data, password=hashed_password)
            db.session.add(student)
            db.session.commit()
        flash(f"Registration Successfull {form.username.data}", "success")
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.Is_authenticated():
    #     return redirect(url_for('home'))
    # else:
    form = LoginForm()
    if form.validate_on_submit():
        username_1 = form.username.data
        with app.app_context():
            student = Student.query.filter_by(username=username_1).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            flash(f"Login Successfull {username_1}", "success")
            return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)
