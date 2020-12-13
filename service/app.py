import os
from flask import Flask, render_template, url_for, redirect, request, session

from models.db import DB, DB_URI
from models.models import Employee, Department

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

@app.route("/smoketest")
def smoketest():
    return "OK Smoke Test"



@app.route('/')
def base_page():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
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
    return render_template('login.html', error=error)


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

    return render_template('info.html', information=emplyee, head_info=head)

    return "Users!"


@app.route('/addinfo', methods=['GET', 'POST'])
def add_info():
    department_all = []
    department_all.extend(Department.query.all())
    if request.method == 'POST':
        form_data = request.form
        username = form_data['username']
        birthday_date = form_data['date']
        position = form_data['position']
        salary = form_data['salary']
        password = form_data['username'].lower()
        dep_id = form_data.get('department')

        new_employee = Employee(

            username,
            birthday_date,
            position,
            salary,
            dep_id,
            password
        )
        DB.session.add(new_employee)
        DB.session.commit()
    return render_template('addinfo.html', departmentall=department_all)


@app.route('/deleteinfo', methods=['GET', 'POST'])
def delete_info():
    employee_info = []
    employee_info.extend(Employee.query.filter(Employee.id > 0).all())
    if request.method == 'POST':
        username = []

        form_data = request.form
        username.extend(form_data.getlist('people'))
        for i in username:
            DB.session.query(Employee).filter_by(id=i).delete()

        DB.session.commit()

    return render_template('deleteinfo.html', employee_info=employee_info)


@app.route('/updateinfo/<user_id>', methods=['GET', 'POST'])
def update_info(user_id):
    if request.method == 'GET':
        emloyee = Employee.query.filter(Employee.id == user_id).first()
    if request.method == "POST":
        emloyee = Employee.query.filter(Employee.id == user_id).first()
        form_data = request.form
        username = form_data['username']
        birthday_date = form_data['date']
        position = form_data['position']
        salary = form_data['salary']
        password = form_data['username'].lower()
        dep_id = form_data.get('department')
        emloyee.emp_name = username
        emloyee.birthday_date = birthday_date
        emloyee.position = position
        emloyee.salary = salary
        emloyee.password = password
        emloyee.dep_id = dep_id
        DB.session.commit()

    return render_template('updateinfo.html', employee_info=emloyee)


@app.route('/adddep', methods=['GET', 'POST'])
def add_dep():
    res = dict()
    if request.method == 'GET':
        employee_nid = []

        head_id = list(map(lambda x: x[0], DB.session.query(Department.head_id).all()))
        employee_nid.extend(Employee.query.filter(Employee.id.notin_(head_id)).all())
        res.update({"employees": employee_nid, "message": ""})

    if request.method == 'POST':
        form_data = request.form
        depname = form_data['depname']
        head = form_data.get('head')
        new_dep = Department(

            depname,
            head
        )
        DB.session.add(new_dep)
        DB.session.commit()
        res.update({"message": "added dep"})
    return render_template('adddep.html', res=res)


if __name__ == '__main__':
    app.run()
