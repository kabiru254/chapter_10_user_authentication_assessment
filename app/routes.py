from app import app, db
from app.models import User
from flask_login import login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for
from app.forms import RegisterForm, Loginform

@app.route('/')
@app.route('/home')
@login_required
def home():
    """Home URL"""
    return render_template('home.html', title='Home')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login URL"""
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {form.username.data}')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register URL"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User {form.username.data} has been registered successfully.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)