import json
from datetime import datetime
from flask import render_template, redirect, session, url_for, request, g, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from app import app, db, lm
from .models import Person, Case, PhoneLogEntry


@app.route('/api/table/case/<case_id>/clients/')
def get_clients_by_caseid(case_id):
    return get_people_json(case_id)

@app.route('/api/table/clients')
def get_clients():
    return get_people_json()

def get_people_json(case_id=None):
    draw = request.args['draw']
    start = int(request.args['start'])
    page_length = int(request.args['length'])
    query = request.args['search[value]']
    is_regex = bool(request.args['search[regex]'])

    sort_column_number = int(request.args['order[0][column]'])
    sort_column_direction = request.args['order[0][dir]']
    sort_column_name = request.args['columns[{0}][data]'.format(sort_column_number)]
    sort_column_allowed = bool(request.args['columns[{0}][orderable]'.format(sort_column_number)])
    sort_columns = {
        "case_name": "case.case_name"
    }
    sort_column = None
    if sort_column_allowed:
        sort_column = sort_columns[sort_column_name] if sort_column_name in sort_columns.keys() else sort_column_name

    page_number = (start / page_length) + 1
    query_like = '%' + query + '%'

    people, total_people_count, count_after_filter = \
        get_people(offset=page_number, limit=page_length, do_sort=sort_column_allowed, sort_column=sort_column,
                   sort_direction=sort_column_direction, case_id=case_id, query_like=query_like)

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

def get_people(offset, limit, do_sort, sort_column, sort_direction, case_id=None, query_like=None):
    people = Person.query.filter((Person.first_name.like(query_like)) | (Person.last_name.like(query_like)))

    if case_id != None:
        people = people.filter(Person.case.has(id=case_id))

    total_people_count = Person.query.count()
    count_after_filter = people.count()

    if do_sort:
        if (sort_direction == 'desc'):
            people = people.order_by(desc(sort_column))
        else:
            people = people.order_by(sort_column)

    people = people.paginate(offset, limit, False).items

    return people, total_people_count, count_after_filter