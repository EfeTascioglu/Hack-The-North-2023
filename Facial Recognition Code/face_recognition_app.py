import face_recognition
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

def get_absolute_path(relative_path):
    return os.path.abspath(relative_path)

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

class SimpleFaceRecognizer:
    def __init__(self):
        self.encodings = []
        self.names = []

    def add_face(self, image_path, name):
        # Load the image
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

# Example usage:
recognizer = SimpleFaceRecognizer()
recognizer.add_face(get_absolute_path("images/efe_1.jpg"), "Efe Tascioglu")
recognizer.add_face(get_absolute_path("images/efe_2.jpg"), "Efe Tascioglu")
recognizer.add_face(get_absolute_path("images/efe_3.jpg"), "Efe Tascioglu")
recognizer.add_face(get_absolute_path("images/tyler_1.jpg"), "Tyler Tian")

recognized_faces = recognizer.recognize(get_absolute_path("images/tyler_2.jpg"))
for face in recognized_faces:
    print(f"Name: {face['name']}, Location: {face['location']}")

display_image_with_boxes(get_absolute_path("images/tyler_2.jpg"), recognized_faces)


recognized_faces = recognizer.recognize(get_absolute_path("images/efe_5.jpg"))
display_image_with_boxes(get_absolute_path("images/efe_5.jpg"), recognized_faces)