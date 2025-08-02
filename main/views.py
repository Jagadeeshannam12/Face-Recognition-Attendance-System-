from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError

from .forms import RegisterForm, LoginForm
from .models import Student, Attendance

import os, cv2, csv
import numpy as np

from face_recognition.detector import detect_faces
from face_recognition.utils import save_image
from face_recognition.recognizer import recognize_face
from face_recognition.live_recognizer import capture_and_mark_attendance
from django.core.files.base import ContentFile


# ✅ Register view with webcam + file upload support
def register_view(request):
    msg = ""
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                # Create User
                user = User.objects.create_user(
                    username=cd['username'],
                    email=cd['email'],
                    password=cd['password']
                )

                # Create Student
                student = Student.objects.create(
                    user=user,
                    registration_number=cd['registration_number'],
                    section=cd['section'],
                )

                # Get face image from uploaded file
                uploaded_img = request.FILES.get('face_image')
                if not uploaded_img:
                    msg = "❌ Please upload or capture a face image."
                    student.delete()
                    user.delete()
                    return render(request, 'register.html', {'form': form, 'msg': msg})

                # Convert to OpenCV format
                img_data = uploaded_img.read()
                np_arr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # Detect faces
                faces = detect_faces(img)
                if not faces:
                    msg = "❌ No face detected. Please try with a clear face image."
                    student.delete()
                    user.delete()
                    return render(request, 'register.html', {'form': form, 'msg': msg})

                # Save cropped face image to media/faces/
                face = faces[0]
                is_success, buffer = cv2.imencode(".jpg", face)
                if is_success:
                    content = ContentFile(buffer.tobytes())
                    filename = f"{student.registration_number}.jpg"
                    student.face_image.save(filename, content)
                    student.save()

                return redirect('login')

            except IntegrityError:
                msg = "⚠️ Username or registration number already exists."
                if 'user' in locals():
                    user.delete()
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'msg': msg})


# ✅ Login view
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = ""
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('student_dashboard' if hasattr(user, 'student') else 'teacher_dashboard')
        else:
            msg = "Invalid username or password"
    return render(request, 'login.html', {'form': form, 'msg': msg})


# ✅ Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


# ✅ Home view
def home_view(request):
    return render(request, 'home.html')


# ✅ Student Dashboard
@login_required
def student_dashboard(request):
    student = request.user.student
    records = Attendance.objects.filter(student=student)
    total = records.count()
    present = records.filter(is_present=True).count()
    absent = total - present
    percent = round((present / total) * 100, 2) if total else 0

    return render(request, 'dashboard_student.html', {
        'attendance_records': records,
        'present_days': present,
        'absent_days': absent,
        'total_days': total,
        'percent': percent
    })


# ✅ Teacher Dashboard
@login_required
def teacher_dashboard(request):
    students = Student.objects.all().order_by('registration_number')
    data = []

    for s in students:
        total = Attendance.objects.filter(student=s).count()
        present = Attendance.objects.filter(student=s, is_present=True).count()
        percent = round((present / total) * 100, 2) if total else 0

        data.append({
            'student': s,
            'present': present,
            'total': total,
            'percent': percent
        })

    return render(request, 'dashboard_teacher.html', {'attendance_data': data})


# ✅ Real-time face recognition with webcam
def mark_face_attendance(request):
    success, student = capture_and_mark_attendance()
    if success:
        return render(request, 'attendance_success.html', {'student': student})
    return render(request, 'attendance_failed.html')


# ✅ Upload face image from webcam/app for attendance marking
@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST' and request.FILES.get('face_image'):
        face_file = request.FILES['face_image']
        temp_path = f"media/temp/{face_file.name}"
        os.makedirs("media/temp", exist_ok=True)

        with open(temp_path, 'wb+') as dest:
            for chunk in face_file.chunks():
                dest.write(chunk)

        img = cv2.imread(temp_path)
        faces = detect_faces(img)
        if not faces:
            return JsonResponse({'status': 'error', 'message': 'No face detected'})

        saved_face_path = save_image(faces[0], folder='media/temp/')
        matched_file = recognize_face(saved_face_path)

        if matched_file:
            reg_no = os.path.splitext(matched_file)[0]
            student = Student.objects.filter(registration_number=reg_no).first()
            if student:
                Attendance.objects.get_or_create(
                    student=student,
                    date=timezone.localdate(),
                    defaults={'is_present': True}
                )
                return JsonResponse({'status': 'success', 'message': f'Attendance marked for {student.user.username}'})

        return JsonResponse({'status': 'error', 'message': 'Face not recognized'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# ✅ CSV Export for teachers
@login_required
def download_csv(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Registration No.', 'Section', 'Date', 'Present', 'Percentage'])

    students = Student.objects.all()

    for student in students:
        total_days = Attendance.objects.filter(student=student).count()
        present_days = Attendance.objects.filter(student=student, is_present=True).count()
        percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0

        records = Attendance.objects.filter(student=student).order_by('date')
        for record in records:
            writer.writerow([
                student.user.username,
                student.registration_number,
                student.section,
                record.date.strftime('%Y-%m-%d'),
                'Present' if record.is_present else 'Absent',
                percentage
            ])

    return response
