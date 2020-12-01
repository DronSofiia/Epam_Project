from sqlalchemy import ForeignKey

from models.db import DB

class Department(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    dep_name = DB.Column(DB.String(60), unique=True)
    head_id = DB.Column(DB.Integer, ForeignKey('employee.id'))

    def __init__(self, dep_name, head_id):
        self.dep_name = dep_name
        self.head_id = head_id


    def __repr__(self):
        return '<User %r>' % self.dep_name


class Employee(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    emp_name = DB.Column(DB.String(60))
    birthday_date = DB.Column(DB.Date)
    position = DB.Column(DB.String(20))
    salary = DB.Column(DB.String(20))
    dep_id = DB.Column(DB.Integer, ForeignKey('department.id'))
    password = DB.Column(DB.String(60))

    def __init__(self, emp_name, birthday_date,position,salary,dep_id, password):
        self.emp_name = emp_name
        self.birthday_date = birthday_date
        self.position = position
        self.salary = salary
        self.dep_id = dep_id
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.emp_name

def test ():
    return 123


if __name__ == '__main__':
    # run tables creation if it is first run

    DB.create_all()

    # fillup database

    employee1 = Employee('Sofii','2020-12-12','Manager',3000, dep_id=None,password='sofii')
    employee2 = Employee('Ket','1999-12-12','Engineer',3000, dep_id=None,password='ket')
    DB.session.add(employee1)
    DB.session.add(employee2)
    DB.session.commit()

    dep1 = Department('Lviv', head_id=employee2.id)
    DB.session.add( dep1)
    DB.session.commit()

