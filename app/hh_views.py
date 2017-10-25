from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from config import POSTS_PER_PAGE
from .forms import LoginForm, ProfileForm, PostForm
from .models import Person
from .hh_forms import ClientForm

@app.route('/hh/clients', methods=['GET', 'POST'])
def clients():
    form = ClientForm()
    if form.validate_on_submit():
        p = Person()
        p.first_name = form.first_name.data
        p.last_name = form.last_name.data
        p.address_line1 = form.address_line1.data
        p.address_line2 = form.address_line2.data
        p.address_city = form.address_city.data
        p.address_state = form.address_state.data
        p.address_postal_code = form.address_postal_code.data
        p.address_country = form.address_country.data
        p.birthdate = datetime.strptime(form.birthdate.data, '%Y-%m-%d')
        p.sex = form.sex.data
        db.session.add(p)
        db.session.commit()
        flash("Client {0} {1} has been added.".format(p.first_name, p.last_name))
        return redirect(url_for('clients'))

    clients = Person.query.all()
    return render_template('hh_clients.html', clients=clients, form=form)