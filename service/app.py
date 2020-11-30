import os

from flask import Flask, render_template, url_for,redirect, request

template_dir = os.path.abspath('../templates')

app = Flask(__name__, template_folder=template_dir)


@app.route('/login', methods=['GET', 'POST'])
def get_main_page():
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html')

if __name__ == '__main__':

    app.run()