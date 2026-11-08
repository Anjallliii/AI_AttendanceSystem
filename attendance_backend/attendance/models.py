from django.db import models
from django.contrib.auth.models import User

class Section(models.Model):

    name = models.CharField(max_length=20)

    semester = models.IntegerField()

    passout_year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "name",
            "passout_year"
        )

    def __str__(self):
        return (
            f"{self.name} | "
            f"Sem {self.semester} | "
            f"{self.passout_year}"
        )
    
class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
    unique=True
    )

    roll_number = models.CharField(
        max_length=30,
        unique=True
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.roll_number} - {self.name}"
    
    
class StudentPhoto(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="student_photos/"
    )

    is_processed = models.BooleanField(
        default=False
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.roll_number}"
            f" - Photo {self.id}"
        )
        
        
class StudentEmbedding(models.Model):

    photo = models.ForeignKey(
        StudentPhoto,
        on_delete=models.CASCADE
    )

    embedding = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.photo.student.roll_number}"
            f" - Embedding {self.id}"
        )
        
        
class Subject(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    
class Teacher(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    teacher_id = models.CharField(
        max_length=30,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    
class TeacherAssignment(models.Model):

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "teacher",
            "subject",
            "section"
        )

    def __str__(self):
        return (
            f"{self.teacher.name} - "
            f"{self.subject.name} - "
            f"{self.section.name}"
        )
        
        
class AttendanceEvent(models.Model):

    teacher_assignment = models.ForeignKey(
        TeacherAssignment,
        on_delete=models.PROTECT
    )

    attendance_date = models.DateField()

    classroom_image = models.ImageField(
        upload_to="attendance_images/"
    )
    
    is_finalized = models.BooleanField(
        default=False
    )

    is_verified = models.BooleanField(
        default=False
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "teacher_assignment",
            "attendance_date"
        )

    def __str__(self):
        return (
            f"{self.teacher_assignment.subject.name}"
            f" - {self.attendance_date}"
        )
        
class AttendanceRecord(models.Model):

    attendance_event = models.ForeignKey(
        AttendanceEvent,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT
    )

    is_present = models.BooleanField(
        default=False
    )

    marked_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "attendance_event",
            "student"
        )

    def __str__(self):
        status = "Present" if self.is_present else "Absent"

        return (
            f"{self.student.name}"
            f" - {status}"
        )
        

class AttendanceImage(models.Model):

    attendance_event = models.ForeignKey(
        AttendanceEvent,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="attendance_images/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    
class AttendanceRecognitionResult(
    models.Model
):

    attendance_event = models.ForeignKey(
        AttendanceEvent,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    confidence = models.FloatField()

    is_present_predicted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )