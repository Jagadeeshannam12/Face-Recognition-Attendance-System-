import os
import cv2
import uuid

def save_image(image, folder='media/faces/'):
    """
    Saves the given image (numpy array) to the specified folder using a unique filename.
    Returns the full file path where the image is saved.
    """
    # Ensure the directory exists and is not accidentally a file
    if os.path.exists(folder) and not os.path.isdir(folder):
        os.remove(folder)  # Remove if a file exists at that path
    os.makedirs(folder, exist_ok=True)

    # Generate a unique filename
    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(folder, filename)

    # Save image using OpenCV
    success = cv2.imwrite(path, image)
    if success:
        print(f"[INFO] Image saved: {path}")
    else:
        print(f"[ERROR] Failed to save image to: {path}")

    return path
