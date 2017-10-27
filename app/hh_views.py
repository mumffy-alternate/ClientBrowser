import json
from datetime import datetime
from flask import render_template, redirect, session, url_for, request, g, request
from flask_login import login_user, logout_user, current_user, login_required


from app import app, db, lm
from config import POSTS_PER_PAGE
from .forms import LoginForm, ProfileForm, PostForm
from .models import Person, Case
from .hh_forms import ClientForm, CaseForm
from .hh_utilities import flash

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
        flash("Client [{0} {1}] has been added.".format(p.first_name, p.last_name))
        return redirect(url_for('clients'))

    clients = Person.query.all()
    return render_template('hh_clients.html', clients=clients, form=form)

@app.route('/hh/cases/', methods=['GET', 'POST'])
def cases(case_name_front=None, case_name_back=None):
    form = CaseForm()
    if form.validate_on_submit():
        c = Case()
        c.date_opened = datetime.strptime(form.date_opened.data, '%Y-%m-%d') if form.date_opened.data else None
        c.date_closed = datetime.strptime(form.date_closed.data, '%Y-%m-%d') if form.date_closed.data else None
        c.case_name = form.case_name.data
        c.court_case_number = form.court_case_number.data
        db.session.add(c)
        db.session.commit()
        flash("Case [{0}] has been added.".format(c.case_name))

        return redirect(url_for('cases', case_name_front=c.case_name))

    cases = Case.query.all()
    return render_template('hh_cases.html', cases=cases, form=form)

@app.route('/hh/cases/<case_name_front>/<case_name_back>/', methods=['GET', 'POST'])
def case_by_name(case_name_front=None, case_name_back=None):
    if case_name_front != None and case_name_back != None:
        case_name = case_name_front + '/' + case_name_back
        case = Case.query.filter_by(case_name=case_name).first()
        if case == None:
            flash("Case [{0}] was not found.".format(case_name), 'warning')
            return redirect(url_for('cases'))
        clients = case.clients.all()
        logs = case.phone_logs.all()

        form = CaseForm()
        if form.validate_on_submit():
            c = case
            c.date_opened = datetime.strptime(form.date_opened.data, '%Y-%m-%d') if form.date_opened.data else None
            c.date_closed = datetime.strptime(form.date_closed.data, '%Y-%m-%d') if form.date_closed.data else None
            c.case_name = form.case_name.data
            c.court_case_number = form.court_case_number.data
            db.session.add(c)
            db.session.commit()
            flash("Case [{0}] has been updated.".format(c.case_name), "success") # TODO display which exact fields were changed and how
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))
        else:
            form = CaseForm(case)
            return render_template('specific_case.html', form=form, clients=clients, logs=logs)

@app.route('/api/table/clients')
def get_clients():
    draw = request.args['draw']
    d = {
  "draw": draw,
  "recordsTotal": 57,
  "recordsFiltered": 57,
  "data": [
    [
      "Gloria",
      "Little",
      "Systems Administrator",
      "New York",
      "10th Apr 09",
      "$237,500"
    ],
    [
      "Haley",
      "Kennedy",
      "Senior Marketing Designer",
      "London",
      "18th Dec 12",
      "$313,500"
    ],
    [
      "Hermione",
      "Butler",
      "Regional Director",
      "London",
      "21st Mar 11",
      "$356,250"
    ],
    [
      "Herrod",
      "Chandler",
      "Sales Assistant",
      "San Francisco",
      "6th Aug 12",
      "$137,500"
    ],
    [
      "Hope",
      "Fuentes",
      "Secretary",
      "San Francisco",
      "12th Feb 10",
      "$109,850"
    ],
    [
      "Howard",
      "Hatfield",
      "Office Manager",
      "San Francisco",
      "16th Dec 08",
      "$164,500"
    ],
    [
      "Jackson",
      "Bradshaw",
      "Director",
      "New York",
      "26th Sep 08",
      "$645,750"
    ],
    [
      "Jena",
      "Gaines",
      "Office Manager",
      "London",
      "19th Dec 08",
      "$90,560"
    ],
    [
      "Jenette",
      "Caldwell",
      "Development Lead",
      "New York",
      "3rd Sep 11",
      "$345,000"
    ],
    [
      "Jennifer",
      "Chang",
      "Regional Director",
      "Singapore",
      "14th Nov 10",
      "$357,650"
    ]
  ]
    }
    return json.dumps(d)


