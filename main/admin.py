from django.contrib import admin
from .models import Student, Attendance
from django.utils.html import format_html

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_number', 'section', 'face_preview')
    search_fields = ('user__username', 'registration_number', 'section')
    readonly_fields = ('face_preview',)

    def face_preview(self, obj):
        if obj.face_image and hasattr(obj.face_image, 'url'):
            return format_html('<img src="{}" width="60" style="border:1px solid #ccc" />', obj.face_image.url)
        return "-"
    face_preview.short_description = 'Face Image'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    list_filter = ('date', 'is_present')
    search_fields = ('student__user__username', 'student__registration_number')
