import face_recognition
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import base64

from flask import Flask, request, jsonify
app = Flask(__name__)

def get_absolute_path(relative_path):
    # Get the directory containing the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, relative_path)

def display_image_with_boxes(image_path, recognized_faces):
    """
    Display image with bounding boxes and names.

    Parameters:
    - image_path (str): Path to the image.
    - recognized_faces (list): List of dictionaries with 'name' and 'location' keys.
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    for face in recognized_faces:
        top, right, bottom, left = face["location"]
        name = face["name"]
        
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)  # Draw rectangle around face
        cv2.putText(image, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Put name above the rectangle

    plt.imshow(image)
    plt.axis('off')  # Turn off axis numbers
    plt.show()

def b64_to_path(b64: str) -> str:
    img_data = base64.b64decode(b64)
    with open("./image_in.jpg", "wb") as f:
        f.write(img_data)
    return "./image_in.jpg"

# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function.
@app.route('/api/add_face', methods=['POST'])
def api_add_face():
    json = request.json
    image_path = json["image_path"]
    name = json["name"]
    recognizer.add_face(get_absolute_path(image_path), name)
    return jsonify({"success": True})

# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function.
@app.route('/api/recognize_face', methods=['POST'])
def api_recognize_face():
    json = request.json
    image_path = b64_to_path(json["image"])
    recognized_faces = recognizer.recognize(image_path)
    display_image_with_boxes(get_absolute_path(image_path), recognized_faces)
    return jsonify({"success": True, "recognized_faces": recognized_faces})


class SimpleFaceRecognizer:
    def __init__(self):
        self.encodings = []
        self.names = []
        # Load the Haar cascades xml file for fast face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    
    def add_face(self, image_path, name):
        image = face_recognition.load_image_file(image_path)
        # Find the face encoding for the image
        face_encoding = face_recognition.face_encodings(image)[0]
        self.encodings.append(face_encoding)
        self.names.append(name)

    def recognize(self, unknown_image_path):
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)
        unknown_face_locations = face_recognition.face_locations(unknown_image)
        
        recognized_faces = []

        for unknown_face_encoding, face_location in zip(unknown_face_encodings, unknown_face_locations):
            matches = face_recognition.compare_faces(self.encodings, unknown_face_encoding)
            name = "Unknown"
            if True in matches:
                match_index = matches.index(True)
                name = self.names[match_index]
            recognized_faces.append({
                "name": name,
                "location": face_location  # This will be in the format (top, right, bottom, left)
            })

        return recognized_faces
if __name__ == "__main__":
    # Example usage:
    recognizer = SimpleFaceRecognizer()
    app.run(host='0.0.0.0')
    
