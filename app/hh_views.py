from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from config import POSTS_PER_PAGE
from .forms import LoginForm, ProfileForm, PostForm
from .models import Person
from .hh_forms import ClientForm

@app.route('/hh/clients')
def clients():
    form = ClientForm()
    if form.validate_on_submit():
       pass

    clients = Person.query.all()
    return render_template('hh_clients.html', clients=clients, form=form)