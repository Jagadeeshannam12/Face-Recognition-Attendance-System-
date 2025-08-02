import cv2
from ultralytics import YOLO
import os

# Load model once
MODEL_PATH = 'weights/yolov8n.pt'

# Check if weights file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"YOLO weights not found at: {MODEL_PATH}")

model = YOLO(MODEL_PATH)

def detect_faces(frame):
    """
    Detect faces in a given frame using YOLOv8.
    
    Args:
        frame (ndarray): Image/frame as a NumPy array (BGR).
    
    Returns:
        List of cropped face images (as NumPy arrays).
    """
    results = model.predict(source=frame, save=False, stream=True, verbose=False)
    faces = []

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            h, w = frame.shape[:2]

            # Safety check to avoid out-of-bounds slicing
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            face = frame[y1:y2, x1:x2]
            if face.size > 0:
                faces.append(face)

    return faces
