from face_recognition_code.face_recognition_api import *

import base64
from flask import Flask, request, jsonify
app = Flask(__name__)

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
    if recognized_faces["success"]:
        return jsonify({"success": True, "recognized_faces": recognized_faces})


if __name__ == "__main__":
    # Example usage:
    recognizer = SimpleFaceRecognizer()
    # Set up the database in RAM
    recognizer.add_face(get_absolute_path("images/efe_1.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/efe_2.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/efe_3.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/tyler_1.jpg"), "Tyler Tian")
    app.run(host='0.0.0.0')