import face_recognition
import numpy as np
import os

def get_absolute_path(relative_path):
    return os.path.abspath(relative_path)

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
        
        for unknown_face_encoding in unknown_face_encodings:
            # Compare the face to known faces
            results = face_recognition.compare_faces(self.encodings, unknown_face_encoding)
            name = "Unknown"
            for i in range(len(results)):
                if results[i]:
                    name = self.names[i]
                    break
            return name

# Example usage:
recognizer = SimpleFaceRecognizer()
recognizer.add_face(get_absolute_path("images/efe_1.jpg"), "Efe Tascioglu")
recognizer.add_face(get_absolute_path("images/tyler_1.jpg"), "Tyler Tian")
print(recognizer.recognize(get_absolute_path("images/tyler_2.jpg")))
