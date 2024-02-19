import cv2
import base64
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# Set camera resolution
CAM_WIDTH = 640
CAM_HEIGHT = 480

# Capture video from camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

# Function to capture frames and send them to the client
def send_frames():
    while True:
        success, frame = camera.read()
        if success:
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('frame', {'image': frame_bytes})
        else:
            break

@app.route('/')
def index():
    return render_template('live.html')

# Start streaming when a client connects
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    thread = Thread(target=send_frames)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True, port=80)
