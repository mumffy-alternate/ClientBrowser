import json
from datetime import datetime
from flask import render_template, redirect, session, url_for, request, g, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

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
            flash("Case [{0}] has been updated.".format(c.case_name),
                  "success")  # TODO display which exact fields were changed and how
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))
        else:
            form = CaseForm(case)
            client_form = ClientForm()
            return render_template('specific_case.html', form=form, clients=clients, logs=logs,
                                   case_name_front=case_name_front, case_name_back=case_name_back,
                                   client_form=client_form)


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
            flash("Client [{0}] has been added to this case [{1}].".format(p.first_name + " " + p.last_name, case.case_name))
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))
        else:
            flash("Validation Errors:".format(form.errors), "error")
            return redirect(url_for('case_by_name', case_name_front=case_name_front, case_name_back=case_name_back))


@app.route('/api/table/clients')
def get_clients():
    draw = request.args['draw']
    start = int(request.args['start'])
    page_length = int(request.args['length'])
    query = request.args['search[value]']
    is_regex = bool(request.args['search[regex]'])

    sort_column_number = int(request.args['order[0][column]'])
    sort_column_direction = request.args['order[0][dir]']
    sort_column_name = request.args['columns[{0}][data]'.format(sort_column_number)]
    sort_column_allowed = bool(request.args['columns[{0}][orderable]'.format(sort_column_number)])

    page_number = (start / page_length) + 1
    query_like = '%' + query + '%'

    # people = Person.query.order_by('id').paginate(page_number, page_length, False).items
    people = Person.query.filter((Person.first_name.like(query_like)) | (Person.last_name.like(query_like)))
    total_people_count = Person.query.count()
    count_after_filter = people.count()

    if sort_column_allowed:
        sort_columns = {
            "case_name": "case.case_name"
        }
        sort_column = sort_columns[sort_column_name] if sort_column_name in sort_columns.keys() else sort_column_name

        if (sort_column_direction == 'desc'):
            people = people.order_by(desc(sort_column))
        else:
            people = people.order_by(sort_column)
    people = people.paginate(page_number, page_length, False).items

    data = []
    for person in people:
        item = {}
        item['role'] = person.role.short_name if person.role else "(no defined role)"
        item['first_name'] = person.first_name
        item['last_name'] = person.last_name
        item['case_name'] = person.case.case_name if person.case else "(missing case name)"
        data.append(item)

    result = {
        "draw": draw,
        "recordsTotal": total_people_count,
        "recordsFiltered": count_after_filter,
        "data": data
    }
    return json.dumps(result)
