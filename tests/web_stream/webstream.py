from flask import Flask, Response, render_template
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
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(js.interpret_json(json_data), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
