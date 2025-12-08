import mediapipe as mp
import cv2
import numpy as np
from math import dist

mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_mesh

def load_image(path):
    img = cv2.imread(path)
    return img

def extract_pose_landmarks(image_path):
    image = load_image(image_path)
    with mp_pose.Pose(static_image_mode=True) as pose:
        res = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not res.pose_landmarks:
            return None, image
        landmarks = res.pose_landmarks.landmark
        h, w = image.shape[:2]
        pts = {i.name: (landmark.x * w, landmark.y * h) for i, landmark in zip(mp_pose.PoseLandmark, landmarks)}
        return pts, image

def compute_simple_body_measurements(landmarks, user_height_cm=None):
    # landmarks: dict with keys like LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_HIP, RIGHT_HIP, NOSE, LEFT_ANKLE, RIGHT_ANKLE
    # Simple scale: measure pixel distance between nose and average ankle -> map to user height if given
    nose = landmarks.get("NOSE")
    left_ankle = landmarks.get("LEFT_ANKLE")
    right_ankle = landmarks.get("RIGHT_ANKLE")
    if not nose or not left_ankle or not right_ankle:
        return {"error":"required landmarks not found"}
    ankle_y = (left_ankle[1] + right_ankle[1])/2
    pixel_height = ankle_y - nose[1]
    if pixel_height <= 0:
        scale = None
    else:
        scale = (user_height_cm / pixel_height) if user_height_cm else None

    # Use shoulder width as base measurement:
    left_shoulder = landmarks.get("LEFT_SHOULDER")
    right_shoulder = landmarks.get("RIGHT_SHOULDER")
    left_hip = landmarks.get("LEFT_HIP")
    right_hip = landmarks.get("RIGHT_HIP")
    def px_to_cm(px):
        return px * scale if scale else None

    out = {}
    if left_shoulder and right_shoulder:
        shoulder_px = dist(left_shoulder, right_shoulder)
        out["shoulder_cm"] = round(px_to_cm(shoulder_px) or (shoulder_px), 2)
        # approximate chest circumference: multiply width by factor (empirical)
        out["chest_cm_est"] = round((px_to_cm(shoulder_px) or shoulder_px) * 2.5, 1)
    if left_hip and right_hip:
        hip_px = dist(left_hip, right_hip)
        out["hip_cm_est"] = round((px_to_cm(hip_px) or hip_px) * 2.7, 1)
    # waist: area between left and right at mid-hip/torso; approximate as average of shoulder & hip widths
    if left_shoulder and right_shoulder and left_hip and right_hip:
        avg_px = (dist(left_shoulder, right_shoulder) + dist(left_hip, right_hip))/2
        out["waist_cm_est"] = round((px_to_cm(avg_px) or avg_px) * 2.6, 1)
    return out

def process_image_for_body(path, user_height_cm=None):
    landmarks, image = extract_pose_landmarks(path)
    if landmarks is None:
        return {"error": "No pose found"}
    measurements = compute_simple_body_measurements(landmarks, user_height_cm)
    return {"measurements": measurements}
