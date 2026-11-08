from django.urls import path

from .views import (
    AdminStudentReportView,
    AttendanceRecognitionUpdateView,
    FinalizeAttendanceView,
    LoginView,
    StudentAttendanceHistoryView,
    StudentCreateView,
    StudentListView,
    AttendanceUploadView,
    AttendanceEventDetailView,
    StudentSubjectsView,
    TeacherAssignmentsView,
    TeacherAttendanceRegisterView,
    TeacherCreateView
)

urlpatterns = [

    path(
        "students/",
        StudentListView.as_view(),
        name="student-list"
    ),

    path(
        "attendance/upload/",
        AttendanceUploadView.as_view(),
        name="attendance-upload"
    ),
    
    path(
        "students/create/",
        StudentCreateView.as_view(),
        name="student-create"
    ),
    
    path(
        "attendance/event/<int:event_id>/",
        AttendanceEventDetailView.as_view()
    ),
    
    path(
        "attendance/result/<int:result_id>/",
        AttendanceRecognitionUpdateView.as_view()
    ),
    
    path(
        "attendance/finalize/<int:event_id>/",
        FinalizeAttendanceView.as_view()
    ),
    
    path(
    "my-subjects/",
        StudentSubjectsView.as_view()
    ),
    
    path(
        "my-subjects/<int:subject_id>/attendance/",
        StudentAttendanceHistoryView.as_view()
    ),
    
    path(
        "my-assignments/",
        TeacherAssignmentsView.as_view()
    ),
    
    path(
        "teacher-assignment/<int:assignment_id>/register/",
        TeacherAttendanceRegisterView.as_view()
    ),
    
    path(
        "admin/student/<int:student_id>/report/",
        AdminStudentReportView.as_view()
    ),
    
    path(
        "teachers/create/",
        TeacherCreateView.as_view()
    ),
    
    path(
        "login/",
        LoginView.as_view()
    ),
]