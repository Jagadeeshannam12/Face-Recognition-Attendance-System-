from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('mark-face/', views.mark_face_attendance, name='mark_face_attendance'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('export-csv/', views.download_csv, name='export_csv'),  # ✅ NEW CSV export route
    path('', views.home_view, name='home'),
]
