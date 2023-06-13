import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)
cap = cv2.VideoCapture(0)




def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break


        _, encoded_frame = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_frame) + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
