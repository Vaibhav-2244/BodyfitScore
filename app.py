import os
import cv2
from mediapipe.python.solutions import pose as mp_pose
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# =======================
# CONFIG (Render-friendly)
# =======================
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =======================
# MediaPipe setup
# =======================
pose = mp_pose.Pose(static_image_mode=True)

# -----------------------------
# Utility: extract body features
# -----------------------------
def extract_body_features(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if not results.pose_landmarks:
        return None

    lm = results.pose_landmarks.landmark

    def dist(a, b):
        return abs(lm[a].x - lm[b].x)

    features = {
        "shoulder_width": dist(mp_pose.PoseLandmark.LEFT_SHOULDER,
                                mp_pose.PoseLandmark.RIGHT_SHOULDER),
        "waist_width": dist(mp_pose.PoseLandmark.LEFT_HIP,
                             mp_pose.PoseLandmark.RIGHT_HIP) * 0.9,
        "hip_width": dist(mp_pose.PoseLandmark.LEFT_HIP,
                           mp_pose.PoseLandmark.RIGHT_HIP),
        "chest_width": dist(mp_pose.PoseLandmark.LEFT_SHOULDER,
                             mp_pose.PoseLandmark.RIGHT_SHOULDER) * 0.95,
        "leg_width": dist(mp_pose.PoseLandmark.LEFT_KNEE,
                           mp_pose.PoseLandmark.RIGHT_KNEE)
    }

    return features

# -----------------------------
# Score logic
# -----------------------------
def calculate_score(features, height=None, weight=None, age=None):
    score = 55

    if features["shoulder_width"] > features["waist_width"]:
        score += 6
    else:
        score -= 4

    if features["hip_width"] > features["waist_width"]:
        score += 6

    if features["leg_width"] > features["waist_width"] * 0.8:
        score += 5

    if height and weight:
        bmi_like = weight / ((height / 100) ** 2)
        if 19 <= bmi_like <= 25:
            score += 6
        else:
            score -= 4

    if age and age > 35:
        score -= 2

    return max(30, min(90, int(score)))

# -----------------------------
# Text generator
# -----------------------------
def generate_text(score, features, gender):
    upper_good = features["shoulder_width"] > features["waist_width"]
    lower_good = features["hip_width"] > features["waist_width"]

    text = "Your body structure shows a clear training base. "

    # Upper body (ALWAYS)
    if upper_good:
        text += "Your upper body, including chest and shoulder width, provides a solid frame. "
    else:
        text += "Your upper body needs more focused chest and shoulder training to improve balance. "

    # Lower body (ALWAYS)
    if lower_good:
        text += "Your lower body, especially hips and thighs, shows good potential for strength and shape. "
    else:
        text += "Improving lower-body strength will help create better overall proportion. "

    # Core / waist
    if features["waist_width"] > features["shoulder_width"] * 0.9:
        text += "Strengthening the core and improving waist control will noticeably enhance definition. "
    else:
        text += "Your waist-to-frame balance supports a clean, athletic look. "

    # Closing
    if score < 50:
        text += "With consistency and structured training, visible progress will come faster than expected."
    elif score < 70:
        text += "You’re on the right path—smart training will take your physique to the next level."
    else:
        text += "Your progress already shows discipline—fine-tuning will elevate your results even more."

    return text

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    gender = request.form.get("gender")
    height = request.form.get("height", type=float)
    weight = request.form.get("weight", type=float)
    age = request.form.get("age", type=int)

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save image (same behavior as your old project)
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Read saved image
    image = cv2.imread(filepath)
    if image is None:
        return jsonify({"error": "Invalid image"}), 400

    features = extract_body_features(image)
    if not features:
        return jsonify({"error": "Body not detected properly"}), 400

    score = calculate_score(features, height, weight, age)
    text = generate_text(score, features, gender)

    return jsonify({
        "bodyfitscore": score,
        "message": text
    })

# =======================
# MAIN
# =======================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
