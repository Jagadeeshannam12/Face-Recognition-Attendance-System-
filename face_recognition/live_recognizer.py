import cv2
import os
from django.utils import timezone
from face_recognition.detector import detect_faces
from face_recognition.utils import save_image
from face_recognition.recognizer import recognize_face
from main.models import Student, Attendance


def capture_and_mark_attendance():
    cap = cv2.VideoCapture(0)
    matched_student = None

    print("[INFO] Starting webcam... Press 'q' to exit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to read from webcam.")
                break

            faces = detect_faces(frame)

            for face in faces:
                temp_path = save_image(face, folder='media/temp/')
                matched_filename = recognize_face(temp_path)

                if matched_filename:
                    reg_no = os.path.splitext(matched_filename)[0]
                    student = Student.objects.filter(registration_number=reg_no).first()

                    if student:
                        today = timezone.localdate()
                        _, created = Attendance.objects.get_or_create(
                            student=student,
                            date=today,
                            defaults={'is_present': True}
                        )

                        matched_student = student

                        # Draw name and rectangle
                        h, w = frame.shape[:2]
                        label = f"{student.user.username} | {student.registration_number} | {student.section}"

                        # Background box for text
                        cv2.rectangle(frame, (10, h - 60), (w - 10, h - 20), (0, 255, 0), -1)
                        cv2.putText(
                            frame, label,
                            (20, h - 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 0),  # black text
                            2
                        )

                        # Green frame outline
                        cv2.rectangle(frame, (20, 20), (w - 20, h - 80), (0, 255, 0), 3)

                        # OPTIONAL: Save annotated frame
                        # cv2.imwrite(f"media/marked/{reg_no}_{today}.jpg", frame)

                        break  # Only process one match

            # Show video
            cv2.imshow("✅ Face Attendance - Press Q to Exit", frame)

            # Break if matched or user presses 'q'
            if matched_student or cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    if matched_student:
        print(f"[✅] Attendance marked for {matched_student.user.username}")
        return True, matched_student
    else:
        print("[❌] No match found.")
        return False, None
