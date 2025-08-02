from deepface import DeepFace
import os

def recognize_face(input_face_path, registered_faces_dir='media/faces/'):
    """
    Compares the input face against all registered faces in the given directory
    using DeepFace and returns the matched filename (e.g., "21BCS123.jpg").
    """
    if not os.path.exists(input_face_path):
        print(f"[ERROR] Input face image not found: {input_face_path}")
        return None

    registered_files = [
        f for f in os.listdir(registered_faces_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    for file in registered_files:
        known_face_path = os.path.join(registered_faces_dir, file)
        try:
            result = DeepFace.verify(
                img1_path=input_face_path,
                img2_path=known_face_path,
                model_name='VGG-Face',       # You can switch to 'Facenet' or others
                detector_backend='opencv',   # Optional: speed up by avoiding mtcnn
                enforce_detection=False
            )
            if result.get("verified"):
                print(f"[MATCH] Found match with: {file}")
                return file

        except Exception as e:
            print(f"[ERROR] Failed comparing with {file}: {e}")

    print("[INFO] No match found.")
    return None
