import os
import cv2
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from body_metrics import (
    extract_landmarks,
    extract_measurements,
    clothing_visibility_check
)
from body_analysis import calculate_score, generate_message

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    gender = request.form.get("gender")

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    image = cv2.imread(filepath)
    if image is None:
        return jsonify({"error": "Invalid image"}), 400

    landmarks = extract_landmarks(image)
    if not landmarks:
        return jsonify({"error": "Body not detected properly"}), 400

    if not clothing_visibility_check(landmarks):
        return jsonify({
            "error": "We couldn’t analyze this image accurately because body shape details aren’t clearly visible. Please try uploading a clear full-body photo in fitted clothing—such as sportswear, sports-bra, leggings, or shorts—for better results.",
            "image_url": f"/static/uploads/{filename}"
        })

    measurements = extract_measurements(landmarks)
    score = calculate_score(measurements, gender)
    message = generate_message(measurements, gender, score)

    return jsonify({
        "bodyfitscore": score,
        "message": message,
        "image_url": f"/static/uploads/{filename}"
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
