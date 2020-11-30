from sqlalchemy import ForeignKey

from db import get_db

db = get_db()


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(60), unique=True)
    head_id =  db.Column(db.Integer, ForeignKey('employee.id'))

    def __init__(self, dep_name, head_id):
        self.dep_name = dep_name
        self.head_id = head_id


    def __repr__(self):
        return '<User %r>' % self.dep_name

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(60))
    birthday_date = db.Column(db.Date)
    position = db.Column(db.String(20))
    salary = db.Column(db.String(20))
    dep_id = db.Column(db.Integer, ForeignKey('department.id'))

    def __init__(self, emp_name, birthday_date,position,salary,dep_id):
        self.emp_name = emp_name
        self.birthday_date = birthday_date
        self.position = position
        self.salary = salary
        self.dep_id = dep_id

    def __repr__(self):
        return '<User %r>' % self.emp_name

if __name__ == '__main__':
    # run tables creation if it is first run

    # db.create_all()

    # fillup database

    employee1 = Employee('Sofii','2020-12-12','Manager',3000, dep_id=None)
    employee2 = Employee('Ket','1999-12-12','Engineer',3000, dep_id=None)
    db.session.add(employee1)
    db.session.add(employee2)
    db.session.commit()

    dep1 = Department('Lviv', head_id=employee2.id)
    db.session.add( dep1)
    db.session.commit()

