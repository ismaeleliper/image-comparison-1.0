import os
import json
import uuid
import base64
import cv2
import face_recognition

from PIL import Image
from io import BytesIO

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

app = Flask(__name__)
os.makedirs(os.path.join(app.instance_path, 'images'), exist_ok=True)
CORS(app)


@app.route("/check-comparison", methods=["POST"])
def check():
    response = {}
    try:
        images_path = os.path.join(app.instance_path, 'images')
        image_1 = request.files["image_1"] if request.files["image_1"] else None
        image_2 = request.files["image_2"] if request.files["image_2"] else None

        images = (image_1, image_2)

        for i in images:
            i.save(os.path.join(images_path, i.filename))
            i.close()

        img = cv2.imread(f"instance/images/{images[0].filename}")
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]

        img2 = cv2.imread(f"instance/images/{images[1].filename}")
        rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

        result = face_recognition.compare_faces([img_encoding], img_encoding2)[0]
        if result:
            return jsonify({"success": True, "icon": "success", "message": "SAME PERSON"}), 200
        else:
            return jsonify({"success": False, "icon": "danger", "message": "NOT SAME PERSON"}), 200
    except Exception as e:
        response["error"] = str(e)
        return jsonify(response), 400


if __name__ == '__main__':
    app.run()
