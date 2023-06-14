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


# done conn db
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
            error = 'Adresa de email sau parolă invalidă'
            return render_template('login.html', error=error, logged_in=False)
    else:
        return render_template('login.html')


@app.route('/main')
def main():
    if 'username' in session:
        username = session['username']
        name = session['name']
        user_type = session['type']
        return render_template('main.html', logged_in=True, user_name=name, user_type=user_type)  # Pass the user's type to the template
    else:
        return redirect('/')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


# db conn donne
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        option = request.form['option']
        gender = request.form["gender"]
        print(option)
        print(type(option))
        print(gender)
        print(type(gender))

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
            error = 'User already exists'
            return render_template('signup.html', error=error)

        # e nevoie de prelucrat datele inainte de a le trimite spre baza de
        # Insert the new user into the database
        cur = mysql.connection.cursor()
        # cur.execute("",
        #             (name, surname, mail, username, password, option))
        cur.callproc("add_user", args=(int(option), name, surname, gender, password, email))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    else:
        return render_template('signup.html')


@app.route('/about')
def about():
    if 'email' in session:
        user_type = session['type']
        name = session['name']
        return render_template('about.html', logged_in=True, user_type=user_type, user_name=name)
    else:
        return render_template('about.html')


@app.route('/programs')
def programs():
    if 'username' in session:
        user_type = session['type']
        return render_template('programs.html', logged_in=True, user_type=user_type)
    else:
        # display all programs
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM program")
        all_prog = cur.fetchall()
        # print(all_ex)


        # lista de dictionare
        preprocessed_data = []
        for program in all_prog:
            # fetch therapist's name
            cur.execute("SELECT name, surname FROM user WHERE id = %s", (str(program[5]),))
            therapist_name_tuple = cur.fetchone()
            therapist_name = therapist_name_tuple[0] + ' ' + therapist_name_tuple[1]
            therapist_name = therapist_name
            # print(therapist_name)

            preprocessed_item = {
                # 'id': program[0], no need to render photo's ID
                'name': program[1].capitalize(),
                'description': program[2].capitalize(),
                # 'photo_id': program[3], !!!!!!!!!!!!!!!!!needed later
                'category_name': program[4].capitalize(),
                # 'therapist_id': program[5], therapist ID no need to render to HTML
                'therapist_name': therapist_name
            }
            preprocessed_data.append(preprocessed_item)
            print(preprocessed_item)


        cur.close()

        # print(preprocessed_data)

        # daca nu e poza atunci una default

        return render_template('programs.html', programs=preprocessed_data)


@app.route('/add_programs')
def add_programs():
    # return render_template('add_prog.html', logged_in=True, user_type=user_type)
    return render_template('add_prog.html')


@app.route('/view_program')
def view_program():
    photo = "img.jpg"
    # return render_template('add_prog.html', logged_in=True, user_type=user_type)
    return render_template('view_program.html', photo=photo)


@app.route('/exercise')
def exercise():
    if 'username' in session:
        user_type = session['type']
        return render_template('exercise.html', logged_in=True, user_type=user_type)
    else:

        # display all exercises
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM exercise")
        all_ex = cur.fetchall()
        # print(all_ex)


        # lista de dictionare
        preprocessed_data = []
        for ex in all_ex:
            # print(type(ex))
            # print(ex[0])
            cur.execute("SELECT name, surname FROM user WHERE id = %s", (str(ex[5]),))
            # therapist_id ex[5]
            # print(ex[5])
            therapist_name_tuple = cur.fetchone()
            therapist_name = therapist_name_tuple[0] + ' ' + therapist_name_tuple[1]
            therapist_name = therapist_name
            # print(therapist_name)

            preprocessed_item = {
                # 'id': ex[0], no need to render photo's ID
                'name': ex[1].capitalize(),
                'description': ex[2].capitalize(),
                # 'photo_id': ex[3], !!!!!!!!!!!!!!!!!needed later
                'category_name': ex[4].capitalize(),
                # 'therapist_id': ex[5], therapist ID no need to render to HTML
                'max_reps': ex[6],
                'therapist_name': therapist_name
            }
            preprocessed_data.append(preprocessed_item)
            print(preprocessed_item)


        cur.close()

        # print(preprocessed_data)

        # daca nu e poza atunci una default

        return render_template('exercise.html', exercises=preprocessed_data)


@app.route('/add_exercise')
def add_exercise():
    if 'username' in session:
        user_type = session['type']
        return render_template('add_ex.html', logged_in=True, user_type=user_type)
    else:
        return render_template('add_ex.html')


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
