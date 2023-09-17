import face_recognition
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

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

def closest_face(eye_coords, face_locations):
    """
    Find the closest face to the eye coordinates.

    Parameters:
    - eye_coords (tuple): Tuple of (x, y) coordinates of the eye.
    - face_locations (list): List of tuples of (top, right, bottom, left) coordinates of the faces.

    Returns:
    - closest_face: Index of Closest Face.
    """
    closest_face = None
    closest_face_distance = None
    for face_num, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location
        face_center = (left + right) / 2, (top + bottom) / 2
        face_distance = np.linalg.norm(np.array(eye_coords) - np.array(face_center))
        if closest_face_distance is None or face_distance < closest_face_distance:
            closest_face = face_num
            closest_face_distance = face_distance
    return closest_face

class SimpleFaceRecognizer:
    def __init__(self):
        self.encodings = []
        self.names_and_data = []
        # Load the Haar cascades xml file for fast face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    
    def add_face(self, image_path, eye_coords, name_and_data):
        image = face_recognition.load_image_file(image_path)
        # Find the face encoding for the image
        face_encodings = face_recognition.face_encodings(image)
        face_locations = face_recognition.face_locations(image)

        if len(face_locations) == 0:
            print("No faces detected in image")
            return False

        closest_face_index = closest_face(eye_coords, face_locations)
        closest_face_encoding = face_encodings[closest_face_index]
        
        self.encodings.append(closest_face_encoding)
        self.names_and_data.append(name_and_data)
        
        return True

    def recognize(self, unknown_image_path, eye_coords):
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)
        unknown_face_locations = face_recognition.face_locations(unknown_image)
        if len(unknown_face_locations) == 0:
            print("No Images Detected")
            return False, "No Faces Found"
        
        closest_face_index = closest_face(eye_coords, unknown_face_locations)
        closest_face_encoding = unknown_face_encodings[closest_face_index]
        matches = face_recognition.compare_faces(self.encodings, closest_face_encoding)
        name_and_data = "Unknown"
        if True in matches:
            match_index = matches.index(True)
            name_and_data = self.names_and_data[match_index]
        return True, name_and_data
    
