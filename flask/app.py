from flask import Flask, render_template, request, redirect, session
from db import connect_db
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

mysql = connect_db(app)


def validate_email(email):
    # Regular expression for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and user['password'] == password:
        session['username'] = username
        session['name'] = user['name']
        return redirect('/main')
    else:
        error = 'Invalid username or password'
        return render_template('login.html', error=error)


@app.route('/main')
def main():
    if 'username' in session:
        username = session['username']
        name = session['name']
        return render_template('main.html', name=name)
    else:
        return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        mail = request.form['mail']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        option = request.form['option']

        # Check if the passwords match
        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)

        # Check if the email is valid
        if not validate_email(mail):
            error = 'Invalid email address'
            return render_template('signup.html', error=error)

        # Check if the username is already taken
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            error = 'Username already exists'
            return render_template('signup.html', error=error)

        # Insert the new user into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (Name, Surname, Mail, Username, Password, Type) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, surname, mail, username, password, option))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    else:
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
