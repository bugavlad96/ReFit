from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the user input from the form
        image_name = request.form['image_name']

        # Create a dictionary with the updated content
        response = {'image_name': image_name, 'other_content': 'Updated content'}

        # Return the response as JSON
        return jsonify(response)

    # Render the initial template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
