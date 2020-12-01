import os
from flask import Flask, render_template, url_for, redirect, request

from models.db import DB, DB_URI
from models.models import Employee

template_dir = os.path.abspath('../templates')


def register_extensions(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.app_context().push()
    DB.init_app(app)
    DB.engine.dialect.description_encoding = None


def create_app():
    app = Flask(__name__, template_folder=template_dir)
    register_extensions(app)

    return app


app = create_app()


@app.route('/login', methods=['GET', 'POST'])
def get_main_page():

    if request.method == 'POST':
        record = Employee.query.filter(Employee.emp_name == request.form['username']).first()
        if not record:
            return render_template('login.html', error="user doest not exist")
        record_pass = record.password




        if request.form['password'] != record_pass:
            error = 'Invalid Credentials. Please try again.'
        else:
            return 'True'
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run()
