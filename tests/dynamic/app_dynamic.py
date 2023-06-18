from flask import Flask, jsonify, render_template

app = Flask(__name__)

count = 0

# Route to get the updated count
@app.route('/get_count')
def get_count():
    global count
    count += 1

    # Return the count as a JSON response
    return jsonify(count=count)

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('index.html', count=count)

if __name__ == '__main__':
    app.run()
