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


# def translate_category(input_category):
#     if input_category == "hands":
#         return
#     if input_category == "shoulders"
#     if input_category == "hips"
#     if input_category == "feet"


@app.route('/edit_exercise', methods=['GET', 'POST'])
def edit_exercise():
    exercise_id = request.args.get('exercise_id')
    exercise_dict = {}
    steps_list = []

    if request.method == 'GET':
        # print(session['type'])
        if int(session['type']) == 0:
            user_type = session['type']
            name = session['name']

            #takes the parameter from EDITEAZA button from exercise.html

            # print("exercise_id: ", exercise_id)

            #return the exercise
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM exercise WHERE id = %s", (exercise_id,))
            exercise = cur.fetchall()
            # print(exercise)


            exercise_data = exercise[0]  # Extract the inner tuple from the outer tuple
            exercise_dict['id'] = exercise_data[0]
            exercise_dict['name'] = exercise_data[1]
            exercise_dict['description'] = exercise_data[2]
            exercise_dict['photo_id'] = exercise_data[3]
            exercise_dict['category'] = exercise_data[4]
            exercise_dict['therapist_id'] = exercise_data[5]
            exercise_dict['max_reps'] = exercise_data[6]
            # print(exercise_dict)



            cur.execute("SELECT * FROM step WHERE exercise_id = %s", (exercise_id,))
            steps = cur.fetchall()
            # print(steps)



            for step in steps:
                step_dict = {}
                step_dict['id'] = step[0]
                step_dict['exercise_id'] = step[1]
                step_dict['photo_id'] = step[2]
                step_dict['description'] = step[3]
                step_dict['permissive_error'] = step[4]
                step_dict['step_number'] = step[5]
                steps_list.append(step_dict)
                # print("step: ", step_dict)

                cur.execute("SELECT * FROM body_part_angle WHERE step_id = %s", (step[0],))
                body_part_angles = cur.fetchall()

                for bd_angles in body_part_angles:

                    if 'body_part_angles' not in step_dict:
                        step_dict['body_part_angles'] = []
                    body_part_angle_dict = {}
                    body_part_angle_dict['id'] = bd_angles[0]
                    body_part_angle_dict['step_id'] = bd_angles[1]
                    body_part_angle_dict['bd_name'] = bd_angles[2]
                    body_part_angle_dict['angle'] = bd_angles[3]

                    step_dict['body_part_angles'].append(body_part_angle_dict)

                # print("body_part_angles: ", body_part_angles)
            # print(steps_list)

        # for step in steps_list:
        #     print("step:", step)
            # print("body_part_angles:", step['body_part_angles'])
        print(steps_list)
        session['steps_list']=steps_list
        return render_template('edit_ex.html', user_name=name, logged_in=True, user_type=user_type, exercise_dict=exercise_dict, steps_list=steps_list)

    if request.method == 'POST':
        print("POST step_list: ", session['steps_list'])
        # retrive all inputs from html page
        form_data = request.form.to_dict()
        # print(form_data)

        exercise_dict['id'] = request.args.get('exercise_id')
        exercise_dict['name'] = form_data['exercise_name']
        exercise_dict['description'] = form_data['exercise-description']
        exercise_dict['category'] = form_data['categ']
        exercise_dict['max_reps'] = int(form_data['rep'])

        steps = []
        for key, value in form_data.items():
            if key.startswith('step_description_'):
                step_dict = {}
                step_number = key.split('_')[2]
                step_dict['id'] = None
                step_dict['description'] = value
                step_dict['permissive_error'] = int(form_data[f'permissive-error{step_number}'])
                step_dict['body_part_angles'] = []
                for joint in ['RIGHT_ELBOW', 'LEFT_ELBOW', 'RIGHT_SHOULDER', 'LEFT_SHOULDER', 'RIGHT_HIP', 'LEFT_HIP',
                              'RIGHT_KNEE', 'LEFT_KNEE']:
                    angle = form_data.get(f'{joint}_{step_number}', '')
                    if angle != '':
                        body_part_angle_dict = {}
                        # body_part_angle_dict['id'] = None
                        body_part_angle_dict['bd_name'] = joint
                        body_part_angle_dict['angle'] = int(angle)
                        step_dict['body_part_angles'].append(body_part_angle_dict)
                steps.append(step_dict)

        exercise_dict['steps'] = steps

        # add the missing IDs from session['steps_list']
        for i, step in enumerate(exercise_dict['steps']):
            step_order = i + 1  # Step order starts from 1
            for original_step in session['steps_list']:
                if original_step['step_number'] == step_order:
                    step['id'] = original_step['id']
                    for body_part_angle in step['body_part_angles']:
                        for original_body_part_angle in original_step['body_part_angles']:
                            if original_body_part_angle['bd_name'] == body_part_angle['bd_name']:
                                body_part_angle['id'] = original_body_part_angle['id']
                                break
                    break


        # Print the parsed data
        print("POST exercise_dict: ", exercise_dict)


        cur = mysql.connection.cursor()


        # Extract step descriptions and joint values
        # step_descriptions = {}
        # joint_values = {}
        #
        # for key, value in form_data.items():
        #     if key.startswith('step_description_'):
        #         step_number = key.split('_')[2]  # Extract the step number
        #         step_descriptions[step_number] = value
        #     elif key.startswith(('RIGHT_', 'LEFT_')):
        #         joint, step_number = key.rsplit('_', 1)  # Split the joint name and step number
        #         joint_values[(joint, step_number)] = value


        # update the exrcises
        cur.callproc('update_exercise', args=(exercise_dict['id'], exercise_dict['name'], exercise_dict['description'], exercise_dict['category'], exercise_dict['max_reps']))
        mysql.connection.commit()

        # Update the steps in exercise_dict
        for i, step in enumerate(session['steps_list']):
            step_id = step['id']
            body_part_angles = step['body_part_angles']
            existing_step = None

            # Find the corresponding step in exercise_dict
            for existing_step in exercise_dict['steps']:
                if existing_step['id'] == step_id:

                    # Update the existing step's description and permissive_error
                    step['description'] = existing_step['description']
                    step['permissive_error'] = existing_step['permissive_error']
                    existing_angles = existing_step['body_part_angles']
                    print("intrat laupdate_step")
                    print(step['description'])
                    print(step['permissive_error'])
                    cur.callproc('update_step', args=(step['id'], step['description'], step['permissive_error']))
                    mysql.connection.commit()
                #
                # # Update or add body_part_angles in the existing step
                # for angle in body_part_angles:
                #     bd_name = angle['bd_name']
                #     angle_value = angle['angle']
                #     angle_id = angle['id']
                #     existing_angle = None
                #
                #     # Find the corresponding angle in the existing step
                #     for existing_angle in existing_angles:
                #         if existing_angle['bd_name'] == bd_name:
                #             break
                #
                #     if existing_angle is None:
                #         # Angle doesn't exist in the existing step, create a new angle
                #         new_angle = {
                #             'bd_name': bd_name,
                #             'angle': angle_value,
                #             'id': angle_id
                #         }
                #         existing_angles.append(new_angle)
                #     else:
                #         # Update the existing angle's value
                #         existing_angle['angle'] = angle_value
                #
                # # Remove body_part_angles that were removed in the session['step_list']
                # existing_angle_ids = {angle['bd_name']: angle['id'] for angle in existing_angles}
                # for existing_angle in existing_angles:
                #     if existing_angle['bd_name'] not in existing_angle_ids:
                #         existing_angles.remove(existing_angle)

        # Update the database with the modified exercise_dict
        # Your code to update the database goes here

        # steps = exercise_dict['steps']
        # for step in steps:
        #     step_id = step['id']
        #     description = step['description']
        #     permissive_error = step['permissive_error']
        #     body_part_angles = step['body_part_angles']
        #     # update current step
        #     cur.callproc('update_step', args=(step['id'], step['description'], step['permissive_error']))
        #     mysql.connection.commit()
        #
        #     print(f"Step ID: {step_id}")
        #     print(f"Description: {description}")
        #     print(f"Permissive Error: {permissive_error}")
        #     print("Body Part Angles:")
        #     # for body_angle in body_part_angles:
        #     #     # update step after making the updade_step:
        #     #     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #     #     bd_name = int(angle['bd_name'])
        #     #     angle_value = angle['angle']
        #     #     angle_id = angle['id']
        #     #     print(f"- Body Part: {bd_name}, Angle: {angle_value}, ID: {angle_id}")
        #     # print()




        # for step in steps_list:
        #     # print("important ", step)
        #     # cur = mysql.connection.cursor()
        #     cur.callproc('update_step', args=(step['id'], step['description'], step['permissive_error']))
        #     mysql.connection.commit()










        #     cur.execute("SELECT @_add_step_4")
        #     last_step_id = cur.fetchone()[0]
        #     # print("Generated step ID:", last_step_id)
        #
        #     step_id = last_step_id
        #     for (joint, joint_step_number), angle in joint_values.items():
        #         if angle != '' and (step_number == joint_step_number):
        #             # print("joint values: ", joint)
        #             # print(step_id)
        #             # print(joint)
        #             # print(angle)
        #             cur.callproc('add_body_part_angle', args=(step_id, joint, int(angle)))
        #             mysql.connection.commit()
        # cur.close()



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
