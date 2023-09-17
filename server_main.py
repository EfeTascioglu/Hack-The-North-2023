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

def mainloop():
    # The FAILURE signal is associated with a red flash on the display.
    # SUCCESS signal is associated with a green flash.
    
    # Wait until either DETECT or RECALL signal. Maintain the previous state of the display until signal received.
    # If DETECT signal
    #     Raspi gives us raw image, and position of gaze on image.
    #     Look at image, assume that it's an alternating QR code input and face input. 
    #     The Pi will let us know if it's a QRDETECT or FACEDETECT signal.
    #     If QRDETECT:
    #         Decode QR code closest to gaze, if it exists. 
    #         Check if website is a HTN profile
    #         If website is a HTN profile:
    #             Return SUCCESS to raspi
    #         If website is not:
    #             Return FAILURE to raspi
    #         Run htnscraper.py on website, running maybe in a separate thread. 
    #         Store name and bio info in a database
    #     If FACEDETECT:
    #         Store the image of the face. 
    #         If the most recent QR code already has a database entry:
    #            Overwrite the database entry with the new face image.
    #         If the most recent QR code is new:
    #           Create a new database entry with the new face image.
    #         Return SUCCESS to raspi
    # If RECALL signal:
    #     Raspi gives us raw image, and position of gaze on image.
    #     Find the closest face to the gaze in the image, if it exists.
    #     If the face exists: 
    #         run Face Recognition on the face, and find the name. 
    #         If the name is UNKNOWN:
    #             Give text: UNKNOWN to raspi
    #             Return FAILURE to raspi
    #         If the name is known:
    #             Give text: $name to raspi
    #             Return SUCCESS to raspi


if __name__ == "__main__":
    # Example usage:
    recognizer = SimpleFaceRecognizer()
    # Set up the database in RAM
    recognizer.add_face(get_absolute_path("images/efe_1.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/efe_2.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/efe_3.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/tyler_1.jpg"), "Tyler Tian")
    app.run(host='0.0.0.0')