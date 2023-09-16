
# TODO: This file is still experimental!

import face_recognition
import numpy as np

class SimpleFaceRecognizer:
    def __init__(self):
        self.encodings = []
        self.names = []

    def add_face(self, image_path, name):
        image = face_recognition.load_image_file(image_path)
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
recognizer.add_face("path_to_image_of_person_1.jpg", "Person 1 Name")
recognizer.add_face("path_to_image_of_person_2.jpg", "Person 2 Name")

recognized_faces = recognizer.recognize("path_to_unknown_image.jpg")
for face in recognized_faces:
    print(f"Name: {face['name']}, Location: {face['location']}")