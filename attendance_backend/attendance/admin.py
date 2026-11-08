from django.contrib import admin
from .models import AttendanceImage, AttendanceRecognitionResult, Section, Student, StudentEmbedding, StudentPhoto, TeacherAssignment ,Subject, Teacher, AttendanceEvent, AttendanceRecord

admin.site.register(Section)
admin.site.register(Student)
admin.site.register(StudentPhoto)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(TeacherAssignment)
admin.site.register(AttendanceEvent)
admin.site.register(AttendanceRecord)
admin.site.register(
    AttendanceImage
)
admin.site.register(StudentEmbedding)
admin.site.register(AttendanceRecognitionResult)