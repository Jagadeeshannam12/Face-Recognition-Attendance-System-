from django.db import models
from django.contrib.auth.models import User
import os


def face_image_upload_path(instance, filename):
    """
    Save student face images inside MEDIA_ROOT/faces/
    Filename will be the student's registration_number.jpg
    """
    ext = filename.split('.')[-1]
    filename = f"{instance.registration_number}.{ext}"
    return os.path.join("faces", filename)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=10)
    face_image = models.ImageField(upload_to=face_image_upload_path, blank=True, null=True)

    def __str__(self):
        # ✅ fixed: Student has no "name" field, so use related user.username
        return f"{self.registration_number} - {self.user.username}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')  # one attendance record per day per student
        ordering = ['-date']  # latest first

    def __str__(self):
        return f"{self.student.registration_number} - {self.date} - {'Present' if self.is_present else 'Absent'}"
