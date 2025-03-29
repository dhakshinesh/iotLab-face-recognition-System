from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import numpy as np
import train_data
import os
import test as face_recogniser

app = Flask(__name__)


# Set up folder paths
TRAINING_FOLDER = "training-data"
if not os.path.exists(TRAINING_FOLDER):
    os.makedirs(TRAINING_FOLDER)
    
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
    


# Route: Homepage
@app.route('/video_gen')
def index():
    face_recogniser.train("training-data")
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route: Upload Images
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        username = request.form["username"].strip()
        file = request.files['file']
        password = request.form["password"].strip()
        
        if username and file and password:
            if password == "123456":
                if file and allowed_file(file.filename):
            	    # Generate a new file name with random characters
            	    new_filename = username + '.jpg'
            	    # Save the file with the new name
            	    file.save(os.path.join(TRAINING_FOLDER, new_filename))
            	    return render_template("thankyou.html", username=username)
            	
		

    return render_template("upload.html", )

# Video Stream Generator (For Face Recognition)
def generate_frames():
    return face_recogniser.start_prediction()

# Route: Video Feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
