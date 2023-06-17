from flask import Flask, render_template, request, redirect, session, Response
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
        # print(preprocessed_item)

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
        cur.callproc('add_program', args=(program_name, program_description, category, therapist_id, ''))
        mysql.connection.commit()

        # retrieve last created UUID
        cur.execute("SELECT @_add_program_4")
        program_id = cur.fetchone()[0]
        print("Generated ex ID:", program_id)

        for cb in checked_checkboxes:
            cur.execute("INSERT INTO exercise_to_prog (program_id, exercise_id) values (%s, %s)", (program_id, cb))
            mysql.connection.commit()
        cur.close()
    cur.close()
    if 'email' in session:
        user_type = session['type']
        name = session['name']
    # return render_template('add_prog.html', logged_in=True, user_type=user_type)
        return render_template('add_prog.html', exercises = preprocessed_data, user_name = name, logged_in=True, user_type=user_type, )
    else:
        return redirect('/')

@app.route('/edit_program', methods=['GET', 'POST'])
def edit_program():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        name = session['name']
        user_type = session['type']
        program_id = request.args.get('program_id')

        cur.execute("SELECT * FROM exercise")
        all_ex = cur.fetchall()
        # print(all_ex)
        total_nr_of_ex = len(all_ex)

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
                'id': ex[0],  # no need to render ID
                'name': ex[1].capitalize(),
                'description': ex[2].capitalize(),
                # 'photo_id': ex[3], !!!!!!!!!!!!!!!!!needed later
                'category_name': ex[4].capitalize(),
                # 'therapist_id': ex[5], therapist ID no need to render to HTML
                'max_reps': ex[6],
                'therapist_name': therapist_name
            }
            preprocessed_data.append(preprocessed_item)
        #   print('vashee tati: ', preprocessed_data)



        cur.execute("SELECT * FROM program WHERE id = %s", (program_id,))
        program = cur.fetchone()
        mysql.connection.commit()
        program_dict = {
            'id': program[0],
            'name': program[1],
            'description': program[2],
            'photo_id': program[3],
            'category_name': program[4],
            'therapist_id': program[5]
        }
        # print(program_dict)

        cur.execute("SELECT * FROM exercise_to_prog WHERE program_id = %s", (program_id,))
        all_exercise_to_prog = cur.fetchall()
        mysql.connection.commit()
        exercise_ids = []
        # print("all_exercise_to_prog: ", all_exercise_to_prog)
        for _, exercise_id in all_exercise_to_prog:
            # print("Program ID:", program_id)
            # print("Exercise ID:", exercise_id)
            exercise_ids.append(exercise_id)

        cur.close()
        return render_template('edit_program.html', total_nr_of_ex = total_nr_of_ex, exercise_ids=exercise_ids,  exercises=preprocessed_data, program=program_dict,  user_name=name, logged_in=True, user_type=user_type, )

    if request.method == 'POST':
        form_data = request.form.to_dict()
        # print("form_data: ", form_data)

        program = {}
        # extract program details:
        program_id = request.args.get('program_id')
        program['id'] = program_id
        program['name'] = form_data['prog_name']
        program['description'] = form_data['prog_descr']
        program['category_name'] = form_data['categ']


        cur = mysql.connection.cursor()
        cur.callproc('update_program', args=(program_id, program['name'], program['description'], program['category_name']))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM exercise_to_prog WHERE program_id = %s", (program_id,))
        # existing_exercises from db before update
        existing_exercises = cur.fetchall()
        print('existing exercises: ', existing_exercises)

        selected_exercises = []
        # parse the parsed from html template in POST
        for key, value in form_data.items():
            if key.startswith('exercise_checkbox_'):
                selected_exercises.append(value)
        print("selected_exercises: ", selected_exercises)

        existing_exercises_set = set(existing_exercises)
        exercises_to_add = []
        exercises_to_remove = []

        # Find newly added exercises
        for exercise_id in selected_exercises:
            if (program_id, exercise_id) not in existing_exercises_set:
                exercises_to_add.append((program_id, exercise_id))

        # Find exercises to remove
        for exercise in existing_exercises:
            if exercise[1] not in selected_exercises:
                exercises_to_remove.append(exercise)

        print("exercises_to_add: ", exercises_to_add)
        print("exercises_to_remove: ", exercises_to_remove)

        # Add newly added exercises to the database
        for exercise in exercises_to_add:
            cur.execute("INSERT INTO exercise_to_prog (program_id, exercise_id) VALUES (%s, %s)", exercise)

        # Remove exercises that are no longer selected from the database
        for exercise in exercises_to_remove:
            cur.execute("DELETE FROM exercise_to_prog WHERE program_id = %s AND exercise_id = %s", exercise)

        mysql.connection.commit()
        cur.close()

        return redirect('/programs')



@app.route('/delete_program')
def delete_program():
    cur = mysql.connection.cursor()
    program_id = request.args.get('program_id')

    # delete from exercise_to_prog:
    cur.execute("DELETE FROM exercise_to_prog WHERE program_id = %s", (program_id,))
    mysql.connection.commit()

    # delete program:
    cur.execute("DELETE FROM program WHERE id = %s", (program_id,))  # step[0] e ID-ul la step
    mysql.connection.commit()
    cur.close()

    print(program_id)
    return redirect('/programs')


@app.route('/view_program')
def view_program():
    photo = "img.jpg"

    cur = mysql.connection.cursor()
    name = session['name']
    user_type = session['type']
    program_id = request.args.get('program_id')


    cur.execute("SELECT * FROM program WHERE id = %s", (program_id,))
    db_program = cur.fetchone()
    cur.execute("SELECT * FROM user WHERE id = %s", (db_program[5],))
    db_user = cur.fetchone()
    therapist_name = db_user[2] + " " + db_user[3]

    program = {
        'id': db_program[0],
        'name': db_program[1],
        'description': db_program[2],
        'photo_id': db_program[3],
        'category_name': db_program[4],
        'therapist_name': therapist_name
    }

    cur.execute("SELECT * FROM exercise_to_prog WHERE program_id = %s", (program_id,))
    # toate exercitiile care au program id-ul meu
    db_tuple_pro_ex = cur.fetchall()
    print(db_tuple_pro_ex)

    all_ex = []
    for _, exercise_id in db_tuple_pro_ex:
        cur.execute("SELECT * FROM exercise WHERE id = %s", (exercise_id,))
        result = cur.fetchone()
        all_ex.append(result)
    print(all_ex)

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
            'id': ex[0],  # no need to render ID
            'name': ex[1].capitalize(),
            'description': ex[2].capitalize(),
            # 'photo_id': ex[3], !!!!!!!!!!!!!!!!!needed later
            'category_name': ex[4].capitalize(),
            # 'therapist_id': ex[5], therapist ID no need to render to HTML
            'max_reps': ex[6],
            'therapist_name': therapist_name
        }
        preprocessed_data.append(preprocessed_item)
    #   print('vashee tati: ', preprocessed_data)




    # return render_template('add_prog.html', logged_in=True, user_type=user_type)
    return render_template('view_program.html', program=program, exercises=preprocessed_data, photo=photo)


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
        # print(preprocessed_item)

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
    # print(session['type'])

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
        # print(steps_list)
        session['steps_list']=steps_list
        return render_template('edit_ex.html', user_name=name, logged_in=True, user_type=user_type, exercise_dict=exercise_dict, steps_list=steps_list)

    if request.method == 'POST':
        # print("POST step_list: ", session['steps_list'])
        # retrive all inputs from html page
        form_data = request.form.to_dict()
        # print("form_data: ", form_data)

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

        # add the missing IDs from session['steps_list'], the ones I could not retrieve from form
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
        # print("POST exercise_dict: ", exercise_dict)
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
            # old values
            step_id = step['id']
            body_part_angles = step['body_part_angles']
            # new values
            existing_step = None

            # Find the corresponding step in exercise_dict
            for existing_step in exercise_dict['steps']:
                if existing_step['id'] == step_id:

                    # Update the existing step's description and permissive_error
                    step['description'] = existing_step['description']
                    step['permissive_error'] = existing_step['permissive_error']
                    # new values
                    existing_angles = existing_step['body_part_angles']
                    cur.callproc('update_step', args=(step['id'], step['description'], step['permissive_error']))
                    mysql.connection.commit()

                    # Update or add body_part_angles in the existing step
                    for bd_part_angle in body_part_angles:
                        # old values, if exists, and new if does not
                        bd_name = bd_part_angle['bd_name']
                        angle_value = bd_part_angle['angle']
                        # angle_id = angle['id']
                        existing_angle = None

                        # Find the corresponding angle in the existing step
                        # new values
                        for existing_angle in existing_angles:
                            if existing_angle['bd_name'] == bd_name:
                                print(existing_angle['bd_name'], ' ', existing_angle['angle'])
                                break

                        if existing_angle is None:
                            print("new body_part_angle")
                            # Angle doesn't exist in the existing step, create a new angle
                            # functia de adauagare de body_part_angle!!!
                            # new_angle = {
                            #     'bd_name': bd_name,
                            #     'angle': angle_value,
                            #     'id': angle_id
                            # }
                            # existing_angles.append(new_angle)
                            print("step_id: ", step['id'])
                            print("bd_name: ", bd_name)
                            print("angle_value: ", angle_value)
                            cur.callproc('add_body_part_angle',
                                args=(step['id'], bd_name, angle_value))
                            mysql.connection.commit()

                        else:
                            print("update")
                            cur.callproc('update_body_part_angle',
                                         args=(existing_angle['id'], existing_angle['angle']))
                            mysql.connection.commit()

        cur.close()

    return redirect('/exercise')

@app.route('/delete_exercise')
def delete_exercise():

    cur = mysql.connection.cursor()
    # cur.callproc('update_body_part_angle', args=(existing_angle['id'], existing_angle['angle']))
    # mysql.connection.commit()
    exercise_id = request.args.get('exercise_id')
    print("exercise_id: ", exercise_id)

    cur.execute("SELECT * FROM exercise WHERE id = %s", (exercise_id,))
    exercise = cur.fetchone()
    print(exercise)


    cur.execute("SELECT * FROM step WHERE exercise_id = %s", (exercise_id,))
    steps = cur.fetchall()
    print(steps)

    # all body_part_angles for all steps
    all_body_part_angles = []
    for step in steps:

        cur.execute("SELECT * FROM body_part_angle WHERE step_id = %s", (step[0],))
        # for one step
        bp_angles = cur.fetchall()
        print(bp_angles)
        for bp_angle in bp_angles:
            cur.execute("DELETE FROM body_part_angle WHERE id = %s", (bp_angle[0],)) #bp_angle[0] e ID-ul la body_part_angle
            mysql.connection.commit()

        cur.execute("DELETE FROM step WHERE id = %s", (step[0],))  # step[0] e ID-ul la step
        mysql.connection.commit()

    # delete from exercise_to_prog:
    cur.execute("DELETE FROM exercise_to_prog WHERE exercise_id = %s", (exercise_id,))
    mysql.connection.commit()


    # delete_exercise:
    cur.execute("DELETE FROM exercise WHERE id = %s", (exercise_id,))  # step[0] e ID-ul la step
    mysql.connection.commit()
    cur.close()

    return redirect('/exercise')

@app.route('/profile')
def profile():
    name = session['name']
    surname = session['surname']
    user_type = session['type']
    mail = session['email']

    if user_type == "therapist":
        photo = "doctor.jpg"
        # photo = "user.jpg"
        type = "Fizioterapeut"

    else:
        user_type = "Pacient"
        photo = "user.jpg"

    return render_template('profile.html', logged_in=True, user_name=name, photo=photo, mail=mail, name=name, surname=surname, user_type=user_type)

@app.route('/view_exercise')
def view_ex():
    return render_template('view_ex.html', logged_in=True)



import core.interpret_JSON as js

json_data = '''{
  "Name": "Exercise Hand",
  "Count_max": 4,
  "Permissive_error": 10,
  "Steps": {
            "step_0": {
              "RIGHT_ELBOW": 90,
              "LEFT_ELBOW": 90
            },
            "step_1": {
              "RIGHT_ELBOW": 180,
              "LEFT_ELBOW": 180
            }
  }
}'''
@app.route('/video_feed')
def video_feed():
    return Response(js.interpret_json(json_data), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
