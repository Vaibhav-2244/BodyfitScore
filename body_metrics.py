import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

def extract_landmarks(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if not results.pose_landmarks:
        return None

    return results.pose_landmarks.landmark

def clothing_visibility_check(landmarks):
    critical = [
        mp_pose.PoseLandmark.LEFT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_HIP,
        mp_pose.PoseLandmark.RIGHT_HIP,
        mp_pose.PoseLandmark.LEFT_KNEE,
        mp_pose.PoseLandmark.RIGHT_KNEE
    ]

    visible = sum(1 for p in critical if landmarks[p].visibility > 0.6)
    return visible >= 5

def extract_measurements(lm):
    def dist(a, b):
        return abs(lm[a].x - lm[b].x)

    return {
        "chest": dist(mp_pose.PoseLandmark.LEFT_SHOULDER,
                      mp_pose.PoseLandmark.RIGHT_SHOULDER),

        "waist": dist(mp_pose.PoseLandmark.LEFT_HIP,
                      mp_pose.PoseLandmark.RIGHT_HIP) * 0.9,

        "hips": dist(mp_pose.PoseLandmark.LEFT_HIP,
                     mp_pose.PoseLandmark.RIGHT_HIP),

        "thighs": dist(mp_pose.PoseLandmark.LEFT_KNEE,
                       mp_pose.PoseLandmark.RIGHT_KNEE),

        "arms": dist(mp_pose.PoseLandmark.LEFT_ELBOW,
                     mp_pose.PoseLandmark.RIGHT_ELBOW)
    }
