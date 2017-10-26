import flask

def flash(message, type='info'):
    flask.flash(message, type)