from face_recognition_code.face_recognition_api import *
from htnscraper import *
from htnscraper2 import *
import QRCodeReader
from QRCodeReader2 import *

import base64
from flask import Flask, request, jsonify
from threading import Thread
app = Flask(__name__)

global next_name_and_data
next_name_and_data = None

def b64_to_path(b64: str) -> str:
    img_data = base64.b64decode(b64)
    with open("./image_in.png", "wb") as f:
        f.write(img_data)
    return "./image_in.png"

def get_absolute_path(relative_path):
    # Get the directory containing the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, relative_path)

# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function.
@app.route('/api/ADD_FACE', methods=['POST'])
def api_add_face():
    global next_name_and_data
    print("POST REQUEST - ADD_FACE")
    json = request.json # assume that there is correct formatting here for now. 
    image_path = b64_to_path(json["image"])
    eye_position = json["eye_pos"]
    if next_name_and_data is None:
        return jsonify({"success": False, "name_and_data": "Not Ready"})
    name_and_data = next_name_and_data # # Assume that the caller calls this after calling QR_DETECT.
    success = recognizer.add_face(get_absolute_path(image_path), eye_position, name_and_data)
    return jsonify({"success": success, "name_and_data": name_and_data})

# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function.
@app.route('/api/RECALL', methods=['POST'])
def api_recognize_face():
    print("POST REQUEST - RECALL")
    json = request.json
    image_path = b64_to_path(json["image"])
    eye_position = json["eye_pos"]
    success, name_and_data = recognizer.recognize(get_absolute_path(image_path), eye_position)
    print("Found Data:", name_and_data)
    return jsonify({"success": success, "name_and_data": name_and_data})

@app.route('/api/QR_DETECT', methods=['POST'])
def api_scan_qr():
    print("POST REQUEST -QR_DETECT")
    json = request.json
    image_path = b64_to_path(json["image"])
    qr_code = str(extract_qr_code_from_image(image_path))[4:]
    #image = cv2.imread(image_path)
    #detect = cv2.QRCodeDetector()
    #qr_code, qr_points, qr_status = detect.detectAndDecode(image)
    if qr_code is None:
        print("No QR Code Found")
        return jsonify({"success": False})
    print("QR Code:", str(qr_code))
    Thread(target=aync_scrape, args=(str(qr_code), )).start()
    return jsonify({"success": True})

def aync_scrape(qr_code):
    global next_name_and_data
    next_name_and_data = (scrape_htn_profile(qr_code))
    print("GOT THE SCRAPE:", next_name_and_data)

def pseudo_mainloop():
    # The FAILURE signal is associated with a red flash on the display.
    # SUCCESS signal is associated with a green flash.
    # The Raspi outgoing boolean signal can be associated with a message, which will be displayed.
    # The Raspi incoming signal is an image, an eye position, and either DETECT or RECALL. 
    
    # Wait until either DETECT or RECALL signal. Maintain the previous state of the display until signal received.
    # If DETECT signal
    #     Raspi gives us raw image, and position of gaze on image.
    #     Look at image, assume that it's an alternating QR code input and face input. 
    #     The Pi will let us know if it's a QRDETECT or FACEDETECT signal.
    #     If QRDETECT:
    #         Decode QR code closest to gaze, if it exists. 
    #         Check if website is a HTN profile
    #         If website is a HTN profile:
    #             Give text: TAKE IMAGE to raspi             
    #             Return SUCCESS to raspi
    #         If website is not:
    #             Give text: RETRY to raspi
    #             Return FAILURE to raspi
    #         Run htnscraper.py on website, running maybe in a separate thread. 
    #         Store name and bio info in a database
    #     If FACEDETECT:
    #         Store the image.
    #         Check if there is a face in the image. 
    #         If there is no face in the image:
    #             Give text: NO FACE to raspi
    #             Return FAILURE to raspi
    #         If there is a face in the image:
    #             If the most recent QR code already has a database entry:
    #                Give text: OVERWRITE to raspi
    #                Overwrite the database entry with the new face image.
    #             If the most recent QR code is new:
    #                Give text: NEW FACE to raspi
    #                Create a new database entry with the new face image.
    #             Return SUCCESS to raspi
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
    #     If the face does not exist:
    #         Give text: NO FACE to raspi
    #         Return FAILURE to raspi
    pass


if __name__ == "__main__":
    # Example usage:
    recognizer = SimpleFaceRecognizer()
    # Set up the database in RAM
    #recognizer.add_face(get_absolute_path("face_recognition_code/images/efe_1.jpg"), (100, 100), "Efe")
    #recognizer.add_face(get_absolute_path("face_recognition_code/images/efe_3.jpg"), (100, 100), "Efe")
    #recognizer.add_face(get_absolute_path("face_recognition_code/images/tyler_1.jpg"), (100, 100), "Tyler")
    #recognizer.add_face(get_absolute_path("face_recognition_code/images/tyler_2.jpg"), (100, 100), "Tyler")
    app.run(host='0.0.0.0')