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
    # display all categories
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM category")
    all_cat = cur.fetchall()
    # print(all_cat)
    #
    # lista de dictionare
    preprocessed_data = []
    for category in all_cat:
        if category[0] != 'user':
            preprocessed_item = {
                'name': category[0].capitalize(),
                'description': category[1].capitalize(),
            }

            preprocessed_data.append(preprocessed_item)
            print(preprocessed_item)

    cur.close()

    # daca nu e poza atunci una default


    return render_template('main.html', categories = preprocessed_data, logged_in=logged_in)


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
            session['id'] = user[0]
            session['name'] = user[2]
            session['surname'] = user[3]
            session['email'] = user[6]
            session['type'] = user[1]
            return redirect('/main')

        else:
            error = 'Adresa de email sau parolă invalidă'
            return render_template('login.html', error=error, logged_in=False)
    else:
        return render_template('login.html')


@app.route('/main')
def main():
    if 'email' in session:
        name = session['name']
        user_type = session['type']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM category")
        all_cat = cur.fetchall()
        # print(all_cat)
        #
        # lista de dictionare
        preprocessed_data = []
        for category in all_cat:
            if category[0] != 'user':
                preprocessed_item = {
                    'name': category[0].capitalize(),
                    'description': category[1].capitalize(),
                }

                preprocessed_data.append(preprocessed_item)
                print(preprocessed_item)

        cur.close()

        return render_template('main.html', logged_in=True, user_name=name, user_type=user_type, categories = preprocessed_data)  # Pass the user's type to the template
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

        # Check if the email is already taken
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
            'id': program[0],
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

    if 'email' in session:
        name = session['name']
        user_type = session['type']
        return render_template('programs.html', user_name = name, logged_in=True, user_type=user_type, programs=preprocessed_data)
    else:

        return render_template('programs.html', programs=preprocessed_data)


@app.route('/add_programs', methods=['GET', 'POST'])
# @app.route('/add_programs')
def add_programs():
    # display all exercises
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM exercise")
    all_ex = cur.fetchall()
    # print(all_ex)

    # lista de dictionare
    preprocessed_data = []
    for ex in all_ex:
        # print(type(ex))
        # print(ex[0])s
        cur.execute("SELECT name, surname FROM user WHERE id = %s", (str(ex[5]),))
        # therapist_id ex[5]
        # print(ex[5])
        therapist_name_tuple = cur.fetchone()
        therapist_name = therapist_name_tuple[0] + ' ' + therapist_name_tuple[1]
        therapist_name = therapist_name
        # print(therapist_name)

        preprocessed_item = {
            'id': ex[0], #no need to render ID
            'name': ex[1].capitalize(),
            'description': ex[2].capitalize(),
            # 'photo_id': ex[3], !!!!!!!!!!!!!!!!!needed later
            'category_name': ex[4].capitalize(),
            # 'therapist_id': ex[5], therapist ID no need to render to HTML
            'max_reps': ex[6],
            'therapist_name': therapist_name
        }
        preprocessed_data.append(preprocessed_item)
        # print(preprocessed_item)
    # retreive exercise end

    if request.method == 'POST':
        checked_checkboxes = request.form.getlist('exercise_checkbox')
        program_name = request.form['prog_name']
        program_description = request.form['prog_descr']
        category = request.form['categ']
        therapist_id = session['id']

        cur = mysql.connection.cursor()
        cur.callproc('add_program', args=(program_name, program_description, category, therapist_id))

        # retrieve last created UUID
        mysql.connection.commit()
        cur.execute("SELECT id FROM program WHERE id = LAST_INSERT_ID()")
        result = cur.fetchone()
        program_id = result[0]
        print(program_id)

        for cb in checked_checkboxes:
            cur.execute("INSERT INTO exercise_to_prog (program_id, exercise_id) values (%s, %s)", (program_id, cb))
            mysql.connection.commit()
        cur.close()

    if 'email' in session:
        user_type = session['type']
        name = session['name']
    # return render_template('add_prog.html', logged_in=True, user_type=user_type)
        return render_template('add_prog.html', exercises = preprocessed_data, user_name = name, logged_in=True, user_type=user_type, )
    else:
        return redirect('/')

@app.route('/view_program')
def view_program():
    photo = "img.jpg"
    # return render_template('add_prog.html', logged_in=True, user_type=user_type)
    return render_template('view_program.html', photo=photo)


@app.route('/exercise')
def exercise():
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
        print()
        therapist_name = therapist_name_tuple[0] + ' ' + therapist_name_tuple[1]
        therapist_name = therapist_name
        # print(therapist_name)

        preprocessed_item = {
            'id': ex[0],
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

    if 'email' in session:
        user_type = session['type']
        name = session['name']
        return render_template('exercise.html', user_name = name, logged_in=True, user_type=user_type, exercises=preprocessed_data)
    else:



        return render_template('exercise.html', exercises=preprocessed_data)


@app.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    print(session['type'])
    if int(session['type']) == 0:
        user_type = session['type']
        name = session['name']
        if request.method == 'POST':

            therapist_id = session['id']

            # retrive all inputs from html page
            form_data = request.form.to_dict()
            # print(form_data)

            # Extract exercise details
            exercise_name = form_data['exercise_name']
            exercise_description = form_data['exercise-description']
            category = form_data['categ']
            max_reps = form_data['rep']
            permissive_error = form_data["permissive-error"]

            # Extract step descriptions and joint values
            step_descriptions = {}
            joint_values = {}

            for key, value in form_data.items():
                if key.startswith('step_description_'):
                    step_number = key.split('_')[2]  # Extract the step number
                    step_descriptions[step_number] = value
                elif key.startswith(('RIGHT_', 'LEFT_')):
                    joint, step_number = key.rsplit('_', 1)  # Split the joint name and step number
                    joint_values[(joint, step_number)] = value

            # Print the extracted information
            # print("Exercise Name:", exercise_name)
            # print("Exercise Description:", exercise_description)
            # print("Category:", category)
            # print("Repetition:", max_reps)
            # print("Step Descriptions:")
            # for step_number, description in step_descriptions.items():
            #     print("  Step", step_number + ":", description)
            # print("Joint Values:")
            # for (joint, step_number), value in joint_values.items():
            #     print(f"  Joint: {joint}\tStep: {step_number}\tValue: {value}")

            cur = mysql.connection.cursor()
            cur.callproc('add_exercise', args=(exercise_name, exercise_description, category, therapist_id, int(max_reps), ''))
            mysql.connection.commit()
            cur.execute("SELECT @_add_exercise_5")
            exercise_id = cur.fetchone()[0]
            # print("Generated ex ID:", exercise_id)

            for step_number, description in step_descriptions.items():
                # cur = mysql.connection.cursor()
                cur.callproc('add_step', args=(exercise_id, description, int(permissive_error), int(step_number), ''))
                # retrieve last created UUID
                mysql.connection.commit()
                cur.execute("SELECT @_add_step_4")
                last_step_id = cur.fetchone()[0]
                # print("Generated step ID:", last_step_id)

                step_id = last_step_id
                for (joint, joint_step_number), angle in joint_values.items():
                    if angle != '' and (step_number == joint_step_number):
                        # print("joint values: ", joint)
                        # print(step_id)
                        # print(joint)
                        # print(angle)
                        cur.callproc('add_body_part_angle', args=(step_id, joint, int(angle)))
                        mysql.connection.commit()
            cur.close()

        return render_template('add_ex.html', user_name=name, logged_in=True, user_type=user_type)
    else:
        return redirect('/exercise')

@app.route('/edit_exercise', methods=['GET', 'POST'])
def edit_exercise():
    print(session['type'])
    if int(session['type']) == 0:
        user_type = session['type']
        name = session['name']

        exercise_id = request.args.get('exercise_id')
        print(exercise_id)

        return render_template('edit_ex.html', user_name=name, logged_in=True, user_type=user_type)
    else:
        return redirect('/exercise')


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
