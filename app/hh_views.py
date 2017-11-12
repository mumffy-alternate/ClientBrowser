import json
from datetime import datetime
from flask import render_template, redirect, session, url_for, request, g, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from app import app, db, lm
from config import POSTS_PER_PAGE
from .forms import LoginForm, ProfileForm, PostForm
from .models import Person, Case, PhoneLogEntry
from .hh_forms import ClientForm, CaseForm, PhoneLogForm
from .hh_utilities import flash


@app.route('/', methods=['GET', 'POST'])
@app.route('/hh/', methods=['GET', 'POST'])
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

        form = CaseForm()
        if form.validate_on_submit():
            c = case
            c.date_opened = datetime.strptime(form.date_opened.data, '%Y-%m-%d') if form.date_opened.data else None
            c.date_closed = datetime.strptime(form.date_closed.data, '%Y-%m-%d') if form.date_closed.data else None
            c.case_name = form.case_name.data
            c.court_case_number = form.court_case_number.data
            db.session.add(c)
            db.session.commit()
            flash("Case [{0}] has been updated.".format(c.case_name),
                  "success")  # TODO display which exact fields were changed and how
            return redirect(url_for('case_by_name', case_name_front=c.get_name_front(), case_name_back=c.get_name_back()))
        else:
            clients = case.clients.all()
            logs = case.phone_logs.order_by(desc(PhoneLogEntry.timestamp))

            form = CaseForm(case)
            client_form = ClientForm()
            phonelog_form = PhoneLogForm()
            return render_template('specific_case.html', form=form, clients=clients, logs=logs, case_id=case.id,
                                   case_name_front=case_name_front, case_name_back=case_name_back,
                                   client_form=client_form, phonelog_form=phonelog_form)


@app.route('/hh/add_client_to_case/<case_name_front>/<case_name_back>/', methods=['POST'])
def add_client_to_case(case_name_front=None, case_name_back=None):
    if case_name_front != None and case_name_back != None:
        case_name = case_name_front + '/' + case_name_back
        case = Case.query.filter_by(case_name=case_name).first()
        if case == None:
            flash("Case [{0}] was not found.".format(case_name), 'warning')
            return redirect(url_for('cases'))
        clients = case.clients.all()
        logs = case.phone_logs.all()
        form = ClientForm()
        if form.validate_on_submit():
            p = Person()
            p.first_name = form.first_name.data
            p.last_name = form.last_name.data
            case.clients.append(p)
            db.session.add(p)
            db.session.add(case)
            db.session.commit()
            flash("Client [{0}] has been added to this case [{1}].".format(p.first_name + " " + p.last_name,
                                                                           case.case_name))
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))
        else:
            flash("Validation Errors:".format(form.errors), "error")
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))


@app.route('/hh/add_phonelog_to_case/<case_name_front>/<case_name_back>/', methods=['POST'])
def add_phonelog_to_case(case_name_front=None, case_name_back=None):
    if case_name_front != None and case_name_back != None:
        case_name = case_name_front + '/' + case_name_back
        case = Case.query.filter_by(case_name=case_name).first()
        if case == None:
            flash("Case [{0}] was not found.".format(case_name), 'warning')
            return redirect(url_for('cases'))
        form = PhoneLogForm()
        if form.validate_on_submit():
            log_entry = PhoneLogEntry()
            if form.logdate.data != None and form.logtime.data != None:
                time_string = form.logdate.data + " " + form.logtime.data
                log_entry.timestamp = datetime.strptime(time_string, "%Y-%m-%d %I:%M %p")
            log_entry.content = form.content.data
            log_entry.case = case
            db.session.add(log_entry)
            db.session.commit()
            flash("Phone log entry for [{0}] has been added to this case [{1}].".format(log_entry.timestamp,
                                                                                        case.case_name))
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))
        else:
            flash("Validation Errors:\n{0}".format(form.errors), "error")
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))
