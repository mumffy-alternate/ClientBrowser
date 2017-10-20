from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from .forms import LoginForm, ProfileForm
from .models import User


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/windex')
def windex():
    user = {'nickname': 'beepee'}  # fake user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Bypassed day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Bypassed movie was so cool!'
        }
    ]
    return render_template('index.html', title='bypassed login', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return login_check(form.user_name.data, form.password.data)

    return render_template('login.html', title="Sign In", form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

def login_check(username, password):
    user = User.query.filter_by(nickname=username).first()

    if user is None:
        flash("{0} is not a registered user".format(username))
        return redirect(url_for('login'))
    else:
        user.follow_self_if_not_already()

    if password != "secret":
        flash("Password incorrect")
        return redirect(url_for('login'))

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me')

    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash ("User {0} not found".format(nickname))
        return redirect(url_for('index'))

    posts = [
        {'author': user, 'body':"Test post 01" },
        {'author': user, 'body':"Test post 02" },
        {'author': user, 'body':"Test post 03" }
    ]

    return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileForm(original_email=g.user.email)
    if form.validate_on_submit():
        g.user.email = form.email.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for('profile_edit'))
    else:
        form.email.data = g.user.email
        form.about_me.data = g.user.about_me
    return render_template('profile.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500