# 🎓 Face Attendance System

![Face Recognition](https://cdn-icons-png.flaticon.com/512/4727/4727425.png) ![Real-Time](https://cdn-icons-png.flaticon.com/512/3135/3135715.png) ![Secure](https://cdn-icons-png.flaticon.com/512/3062/3062634.png)

Automated attendance using facial recognition — secure, fast, and accurate.

## 🚀 Features

- 🤖 **Facial Recognition:** AI-powered face detection for contactless attendance.
- ⏱️ **Real-Time Tracking:** Instant access to attendance records for teachers and students.
- 🔒 **Secure & Private:** Data handled securely, accessible only to authorized users.
- 📦 **CSV Export:** Teachers can export attendance data.
- 📷 **Webcam/App Upload:** Mark attendance via webcam or image upload.

## 🖼️ Screenshots

### 🏠 Home Page
![Home Page](images/home%20page.png.png)

### 🔑 Login Page
![Login Page](images/login%20page.png.png)

### 👨‍🎓 Student Login
![Student Login](images/student%20login%20.png.png)

### 📝 Student Registration
![Student Registration](images/student%20registration.png.png)

### 👩‍🏫 Teacher Login
![Teacher Login](images/teacher%20login.png.png)

## 🗂️ Project Structure

```
attendance_project/
  ├── main/
  │   ├── models.py
  │   ├── views.py
  │   ├── templates/
  │   └── ...
  ├── face_recognition/
  │   ├── detector.py
  │   ├── recognizer.py
  │   └── ...
  ├── media/
  ├── weights/
  │   └── yolov8n.pt
  ├── manage.py
  └── requirements.txt
```

## ⚙️ Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/face-attendance-system.git
   cd face-attendance-system
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Run the server:**
   ```sh
   python manage.py runserver
   ```

## 🖼️ Usage

- Register as a student or teacher.
- Mark attendance via webcam or upload face image.
- Teachers can view dashboards and export CSV reports.

## 🛠️ Tech Stack

- Django
- OpenCV
- Deepface
- YOLOv8
- Pandas

## 📄 License

This project is licensed under the MIT License.


