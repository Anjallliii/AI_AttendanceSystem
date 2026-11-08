from rest_framework import serializers
from .models import AttendanceRecognitionResult, Student, Teacher, TeacherAssignment


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student

        fields = "__all__"
        


class AttendanceUploadSerializer(
    serializers.Serializer
):

    teacher_assignment = serializers.IntegerField()

    attendance_date = serializers.DateField()

    classroom_images = serializers.ListField(
        child=serializers.ImageField()
    )
    
class StudentCreateSerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=100
    )

    email = serializers.EmailField()

    roll_number = serializers.CharField(
        max_length=30
    )

    section_id = serializers.IntegerField()

    photos = serializers.ListField(
        child=serializers.ImageField()
    )
    
class AttendanceRecognitionResultSerializer(
    serializers.ModelSerializer
):

    student_name = serializers.CharField(
        source="student.name",
        read_only=True
    )

    class Meta:

        model = AttendanceRecognitionResult

        fields = [
            "id",
            "student",
            "student_name",
            "confidence",
            "is_present_predicted"
        ]
        
class AttendanceRecognitionUpdateSerializer(
    serializers.Serializer
):

    is_present_predicted = (
        serializers.BooleanField()
    )
    
    
class StudentSubjectSerializer(
    serializers.Serializer
):

    subject_id = serializers.IntegerField()

    subject_name = serializers.CharField()

    subject_code = serializers.CharField()

    attendance_percentage = (
        serializers.FloatField()
    )
    
class StudentAttendanceHistorySerializer(
    serializers.Serializer
):

    date = serializers.DateField()

    status = serializers.CharField()

    finalized = serializers.BooleanField()
    
class TeacherAssignmentSerializer(
    serializers.ModelSerializer
):

    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True
    )

    subject_code = serializers.CharField(
        source="subject.code",
        read_only=True
    )

    section_name = serializers.CharField(
        source="section.name",
        read_only=True
    )

    semester = serializers.IntegerField(
        source="section.semester",
        read_only=True
    )

    class Meta:

        model = TeacherAssignment

        fields = [
            "id",
            "subject_name",
            "subject_code",
            "section_name",
            "semester"
        ]
        
class AdminStudentReportSubjectSerializer(
    serializers.Serializer
):

    subject_id = serializers.IntegerField()

    subject_name = serializers.CharField()

    subject_code = serializers.CharField()

    attendance_percentage = (
        serializers.FloatField()
    )
    
class TeacherCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Teacher

        fields = [
            "teacher_id",
            "name",
            "email"
        ]
        


class LoginSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()

    password = serializers.CharField()