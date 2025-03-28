from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import numpy as np
import train_data
import os

app = Flask(__name__)

# Load OpenCV's Haar cascade for face detection 
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
train_data.train(face_recognizer)

def load_subjects():
    global subjects
    subjects = os.listdir("training-data")
    subjects.insert(0, "")
    print(subjects)


# Set up folder paths
TRAINING_FOLDER = "training-data"
if not os.path.exists(TRAINING_FOLDER):
    os.makedirs(TRAINING_FOLDER)

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
#function to draw text on give image starting from
#passed (x, y) coordinates. 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def predict(test_img):
    #make a copy of the image as we don't want to chang original image
    img = test_img.copy()
    #detect face from the image
    face, rect = train_data.detect_face(img)

    #predict the image using our face recognizer 

    if ( type(rect) != np.ndarray ):
        print("The Image does not contain any face")
        return test_img
    label, confidence = face_recognizer.predict(face)

    print("Confidence : ",confidence, "Label : ", subjects[label])
    #get name of respective label returned by face recognizer
    if confidence > 40 :
        label_text = f'{subjects[label]}-{confidence}' 
    else:
        label_text = "Guest"
    #draw a rectangle around face detected
    draw_rectangle(img, rect)
    #draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1]-5)
    
    return img


# Route: Homepage
@app.route('/')
def index():
    load_subjects()
    return render_template('index.html')

# Route: Upload Images
@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        username = request.form["username"].strip()
        files = request.files.getlist("files")  # Get multiple files

        if username and files:
            user_folder = os.path.join(TRAINING_FOLDER, username)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            for file in files:
                if file.filename:  # Ensure the file is not empty
                    file_path = os.path.join(user_folder, file.filename)
                    file.save(file_path)

            return redirect(url_for("index"))

    return render_template("upload.html")

# Video Stream Generator (For Face Recognition)
def generate_frames():
    cam = cv2.VideoCapture(0)
    while True:
        result, image = cam.read()
        key = cv2.waitKey(10)

        face, rect = train_data.detect_face(image)
        if type(rect) == np.ndarray:
            cv2.imwrite("test-data/test.jpg", image)
            image = predict(image)

        _, buffer = cv2.imencode('.jpg', image)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route: Video Feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
