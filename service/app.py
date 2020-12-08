import os
from flask import Flask, render_template, url_for, redirect, request

from models.db import DB, DB_URI
from models.models import Employee,Department

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
def login():
    if request.method == 'POST':
        record = Employee.query.filter(Employee.emp_name == request.form['username']).first()
        if not record:
            return render_template('login.html', error="user doest not exist")
        record_pass = record.password
        user_id = record.id

        if request.form['password'] != record_pass:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('/info/{id}'.format(id=user_id))
    return render_template('login.html')


@app.route('/info/<user_id>', methods=['GET'])
def get_main_page(user_id):
    emplyee = []
    head = None
    dep = Department.query.filter(Department.head_id == user_id).first()
    if not dep:
        emplyee.append(Employee.query.filter(Employee.id == user_id).first())
    else:
        head = Employee.query.filter(Employee.id == user_id).first()
        emplyee.extend(Employee.query.filter(Employee.dep_id == dep.id).all())


    return render_template('info.html', information = emplyee, head_info = head )



    return "Users!"

if __name__ == '__main__':
    app.run()

