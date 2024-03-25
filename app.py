from flask import Flask, render_template, request
from rdpy.client import RDPClient
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    server_address = request.form['server_address']
    username = request.form['username']
    password = request.form['password']

    client = RDPClient(server_address)
    client.login(username, password)
    client.share_resources()
    client.create_virtual_channel("mychannel")

    try:
        client.connect()
        while True:
            screen_update = client.get_screen_update()
            if screen_update:
                # Convert screen update to OpenCV image
                image = screen_update.to_cv2_image()
                # Convert image to JPEG format for web display
                _, buffer = cv2.imencode('.jpg', image)
                jpg_image = buffer.tobytes()
                # Send image to client
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpg_image + b'\r\n\r\n')
    finally:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
