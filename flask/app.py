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
def index(logged_in=False):
    return render_template('main.html', logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and user[5] == password:
            session['name'] = user[2]
            session['surname'] = user[3]
            session['email'] = user[6]
            session['type'] = user[1]
            return render_template('main.html', logged_in=True, user_name=session['name'], user_type=session['type'])
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error, logged_in=False)
    else:
        return render_template('login.html')


@app.route('/main')
def main():
    if 'email' in session:
        name = session['name']
        user_type = session['type']
        return render_template('main.html', logged_in=True, user_name=name, user_type=user_type)  # Pass the user's type to the template
    else:
        return redirect('/')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        option = request.form['option']

        # Check if the passwords match
        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)

        # Check if the email is valid
        if not validate_email(email):
            error = 'Invalid email address'
            return render_template('signup.html', error=error)

        # Check if the username is already taken
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            error = 'Username already exists'
            return render_template('signup.html', error=error)

        # Insert the new user into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (Name, Surname, Email, Pass, Type) VALUES (%s, %s, %s, %s, %s)",
                    (name, surname, email, password, option))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    else:
        return render_template('signup.html')


@app.route('/about')
def about():
    user_type = session['type']
    return render_template('about.html', logged_in=True, user_type=user_type)


@app.route('/profile')
def profile():
    name = session['name']
    surname = session['surname']
    user_type = session['type']
    mail = session['mail']

    if user_type == "therapist":
        photo = "doctor.jpg"
        # photo = "user.jpg"
        type = "Fizioterapeut"

    else:
        user_type = "Pacient"
        photo = "user.jpg"

    return render_template('profile.html', logged_in=True, user_name=name, photo=photo, mail=mail, name=name, surname=surname, user_type=user_type, type=type)


if __name__ == '__main__':
    app.run(debug=True)
