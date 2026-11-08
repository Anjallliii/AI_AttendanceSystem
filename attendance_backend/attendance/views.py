from unittest import result

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.contrib.auth import authenticate
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework_simplejwt.tokens import (
    RefreshToken
)
from .models import Student, AttendanceRecord
from .serializers import StudentSerializer, AttendanceUploadSerializer, StudentSubjectSerializer, TeacherAssignmentSerializer
from .models import TeacherAssignment, AttendanceEvent, AttendanceImage,AttendanceRecognitionResult
import json
from django.contrib.auth.models import User
from .serializers import (
    AttendanceRecognitionResultSerializer,
    AttendanceRecognitionUpdateSerializer,
    StudentAttendanceHistorySerializer,
    AdminStudentReportSubjectSerializer,
    LoginSerializer,
)
from .models import (
    Student,
    StudentPhoto,
    StudentEmbedding,
    Section,
    Teacher,
)
from .serializers import (
    StudentSerializer,
    AttendanceUploadSerializer,
    StudentCreateSerializer,
    TeacherCreateSerializer
)


class StudentListView(APIView):

    def get(self, request):

        students = Student.objects.all()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = StudentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
class AttendanceUploadView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = AttendanceUploadSerializer(
            data=request.data
        )

        if serializer.is_valid():

            teacher_assignment = (
                TeacherAssignment.objects.get(
                    id=serializer.validated_data[
                        "teacher_assignment"
                    ]
                )
            )

            attendance_event = (
                AttendanceEvent.objects.create(
                    teacher_assignment=teacher_assignment,
                    attendance_date=serializer.validated_data[
                        "attendance_date"
                    ]
                )
            )

            # Save classroom images
            for image in serializer.validated_data[
                "classroom_images"
            ]:

                AttendanceImage.objects.create(
                    attendance_event=attendance_event,
                    image=image
                )

            # =====================================
            # FETCH ATTENDANCE IMAGES
            # =====================================

            attendance_images = (
                AttendanceImage.objects.filter(
                    attendance_event=attendance_event
                )
            )

            # =====================================
            # FETCH STUDENTS OF SECTION
            # =====================================

            students = Student.objects.filter(
                section=teacher_assignment.section
            )

            # =====================================
            # BUILD STUDENTS PAYLOAD
            # =====================================

            students_payload = []

            for student in students:

                embeddings = (
                    StudentEmbedding.objects.filter(
                        photo__student=student
                    )
                )

                embedding_list = []

                for embedding in embeddings:

                    embedding_list.append(
                        embedding.embedding
                    )

                students_payload.append(
                    {
                        "student_id": student.id,
                        "embeddings": embedding_list
                    }
                )

            payload = {
                "students": students_payload
            }

            # =====================================
            # PREPARE IMAGE FILES
            # =====================================

            files = []

            for image in attendance_images:

                files.append(
                    (
                        "images",
                        (
                            image.image.name,
                            image.image.open("rb"),
                            "image/jpeg"
                        )
                    )
                )

            # =====================================
            # CALL FASTAPI
            # =====================================

            response = requests.post(
                "http://127.0.0.1:8000/recognize",
                files=files,
                data={
                    "students_json":
                    json.dumps(payload)
                },
                timeout=60
            )

            # =====================================
            # GET RECOGNITION RESULT
            # =====================================

            recognized_students = (
                response.json()[
                    "recognized_students"
                ]
            )
            
            # =====================================
            # CREATE RECOGNITION RESULTS
            # =====================================

            recognized_map = {}

            for item in recognized_students:

                recognized_map[
                    item["student_id"]
                ] = item["confidence"]


            for student in students:

                if student.id in recognized_map:

                    AttendanceRecognitionResult.objects.create(
                        attendance_event=attendance_event,
                        student=student,
                        confidence=recognized_map[
                            student.id
                        ],
                        is_present_predicted=True
                    )

                else:

                    AttendanceRecognitionResult.objects.create(
                        attendance_event=attendance_event,
                        student=student,
                        confidence=0,
                        is_present_predicted=False
                    )

            # TEMPORARY RETURN
            # WE WILL SAVE TO DB LATER

            return Response(
                {
                    "message":
                    "Recognition completed",

                    "event_id":
                    attendance_event.id,

                    "recognized_count":
                    len(recognized_students)
                },
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )
class StudentCreateView(APIView):

    def post(self, request):

        serializer = StudentCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            section = Section.objects.get(
                id=serializer.validated_data[
                    "section_id"
                ]
            )

            email = serializer.validated_data[
                "email"
            ]

            roll_number = serializer.validated_data[
                "roll_number"
            ]

            user = User.objects.create_user(
                username=email,
                email=email,
                password=roll_number
            )

            student = Student.objects.create(
                user=user,

                name=serializer.validated_data[
                    "name"
                ],

                email=email,

                roll_number=roll_number,

                section=section
            )

            student_photos = []
            for photo in serializer.validated_data[
                "photos"
            ]:

                student_photo = StudentPhoto.objects.create(
                    student=student,
                    image=photo
                )
                
                student_photos.append(
                    student_photo
                )
                
            files = []

            for photo in student_photos:

                files.append(
                    (
                        "images",
                        (
                            photo.image.name,
                            photo.image.open("rb"),
                            "image/jpeg"
                        )
                    )
                )
            response = requests.post(
                "http://127.0.0.1:8000/generate-embeddings",
                files=files,
                timeout=30
            )
            
            embeddings = response.json()[
                "embeddings"
            ]

            for photo, embedding in zip(
                student_photos,
                embeddings
            ):

                StudentEmbedding.objects.create(
                    photo=photo,
                    embedding=embedding
                )
                
                
            return Response(
                {
                    "message":
                    "Student created successfully",

                    "student_id":
                    student.id
                },
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )
        
class AttendanceEventDetailView(APIView):
    permission_classes = [
            IsAuthenticated
        ]

    def get(self, request, event_id):
        

        attendance_event = (
            AttendanceEvent.objects.get(
                id=event_id
            )
        )
        
        teacher = request.user.teacher

        if (
            attendance_event.teacher_assignment.teacher
            !=
            teacher
        ):

            return Response(
                {
                    "error":
                    "Forbidden"
                },
                status=403
            )

        results = (
            AttendanceRecognitionResult.objects.filter(
                attendance_event=attendance_event
            ).select_related(
                "student"
            )
        )

        serializer = (
            AttendanceRecognitionResultSerializer(
                results,
                many=True
            )
        )

        return Response(
            {
                "event_id":
                attendance_event.id,

                "is_finalized":
                attendance_event.is_finalized,

                "students":
                serializer.data
            }
        )
        
class AttendanceRecognitionUpdateView(
    APIView
):
    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request,
        result_id
    ):

        result = (
            AttendanceRecognitionResult.objects.get(
                id=result_id
            )
        )
        
        teacher = request.user.teacher

        if (
            result.attendance_event
            .teacher_assignment
            .teacher
            !=
            teacher
        ):

            return Response(
                {
                    "error":
                    "Forbidden"
                },
                status=403
            )

        serializer = (
            AttendanceRecognitionUpdateSerializer(
                data=request.data
            )
        )

        if serializer.is_valid():

            result.is_present_predicted = (
                serializer.validated_data[
                    "is_present_predicted"
                ]
            )

            result.save()

            return Response(
                {
                    "message":
                    "Attendance updated"
                }
            )

        return Response(
            serializer.errors,
            status=400
        )
        
        
class FinalizeAttendanceView(
    APIView
):
    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        event_id
    ):

        attendance_event = (
            AttendanceEvent.objects.get(
                id=event_id
            )
        )
        
        teacher = request.user.teacher

        if (
            attendance_event.teacher_assignment.teacher
            !=
            teacher
        ):

            return Response(
                {
                    "error":
                    "Forbidden"
                },
                status=403
            )

        if attendance_event.is_finalized:

            return Response(
                {
                    "error":
                    "Attendance already finalized"
                },
                status=400
            )

        results = (
            AttendanceRecognitionResult.objects.filter(
                attendance_event=attendance_event
            )
        )

        for result in results:

            AttendanceRecord.objects.create(
                attendance_event=attendance_event,
                student=result.student,
                is_present=result.is_present_predicted
            )

        attendance_event.is_finalized = True

        attendance_event.save()

        return Response(
            {
                "message":
                "Attendance finalized"
            }
        )
        
class StudentSubjectsView(
    APIView
):
    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
    ):

        student = request.user.student

        assignments = (
            TeacherAssignment.objects.filter(
                section=student.section
            ).select_related(
                "subject"
            )
        )

        subjects = []

        for assignment in assignments:

            total_classes = (
                AttendanceEvent.objects.filter(
                    teacher_assignment=assignment,
                    is_finalized=True
                ).count()
            )

            present_classes = (
                AttendanceRecord.objects.filter(
                    student=student,
                    attendance_event__teacher_assignment=
                    assignment,
                    is_present=True
                ).count()
            )

            percentage = 0

            if total_classes > 0:

                percentage = round(
                    (
                        present_classes
                        /
                        total_classes
                    ) * 100,
                    2
                )

            subjects.append(
                {
                    "subject_id":
                    assignment.subject.id,

                    "subject_name":
                    assignment.subject.name,

                    "subject_code":
                    assignment.subject.code,

                    "attendance_percentage":
                    percentage
                }
            )

        serializer = (
            StudentSubjectSerializer(
                subjects,
                many=True
            )
        )

        return Response(
            {
                "student":
                student.name,

                "section":
                student.section.name,

                "semester":
                student.section.semester,

                "subjects":
                serializer.data
            }
        )
        
class StudentAttendanceHistoryView(
    APIView
):
    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        subject_id
    ):

        student = request.user.student
        

        is_enrolled = TeacherAssignment.objects.filter(
            section=student.section,
            subject_id=subject_id
        ).exists()

        if not is_enrolled:

            return Response(
                {
                    "error": "Forbidden"
                },
                status=403
            )

        records = (
            AttendanceRecord.objects.filter(
                student=student,
                attendance_event__teacher_assignment__subject_id=
                subject_id
            )
            .select_related(
                "attendance_event"
            )
            .order_by(
                "-attendance_event__attendance_date"
            )
        )

        attendance_history = []

        for record in records:

            attendance_history.append(
                {
                    "date":
                    record.attendance_event.attendance_date,

                    "status":
                    (
                        "Present"
                        if record.is_present
                        else "Absent"
                    ),

                    "finalized":
                    record.attendance_event.is_finalized
                }
            )

        serializer = (
            StudentAttendanceHistorySerializer(
                attendance_history,
                many=True
            )
        )

        return Response(
            {
                "student":
                student.name,

                "subject_id":
                subject_id,

                "attendance_history":
                serializer.data
            }
        )
        
class TeacherAssignmentsView(
    APIView
):
    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):
        teacher = request.user.teacher
        assignments = (
            TeacherAssignment.objects.filter(
                teacher=teacher
            )
            .select_related(
                "subject",
                "section"
            )
        )

        serializer = (
            TeacherAssignmentSerializer(
                assignments,
                many=True
            )
        )

        return Response(
            serializer.data
        )
        
class TeacherAttendanceRegisterView(
    APIView
):
    
    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        assignment_id
    ):

        assignment = (
            TeacherAssignment.objects
            .select_related(
                "subject",
                "section"
            )
            .get(
                id=assignment_id
            )
        )
        
        teacher = request.user.teacher

        if assignment.teacher != teacher:

            return Response(
                {
                    "error":
                    "Forbidden"
                },
                status=403
            )

        events = (
            AttendanceEvent.objects.filter(
                teacher_assignment=assignment,
                is_finalized=True
            )
            .order_by(
                "attendance_date"
            )
        )

        dates = [
            event.attendance_date
            for event in events
        ]

        students = Student.objects.filter(
            section=assignment.section
        ).order_by(
            "roll_number"
        )

        register_students = []

        for student in students:

            attendance_list = []

            present_count = 0

            total_classes = len(events)

            for event in events:

                record = (
                    AttendanceRecord.objects.filter(
                        attendance_event=event,
                        student=student
                    )
                    .first()
                )

                if (
                    record
                    and
                    record.is_present
                ):

                    attendance_list.append(
                        "P"
                    )

                    present_count += 1

                else:

                    attendance_list.append(
                        "A"
                    )

            percentage = 0

            if total_classes > 0:

                percentage = round(
                    (
                        present_count
                        /
                        total_classes
                    ) * 100,
                    2
                )

            register_students.append(
                {
                    "student_id":
                    student.id,

                    "roll_number":
                    student.roll_number,

                    "student_name":
                    student.name,

                    "attendance":
                    attendance_list,

                    "percentage":
                    percentage
                }
            )

        return Response(
            {
                "assignment_id":
                assignment.id,

                "subject":
                assignment.subject.name,

                "subject_code":
                assignment.subject.code,

                "section":
                assignment.section.name,

                "semester":
                assignment.section.semester,

                "dates":
                dates,

                "students":
                register_students
            }
        )
        
class AdminStudentReportView(
    APIView
):

    def get(
        self,
        request,
        student_id
    ):

        student = Student.objects.get(
            id=student_id
        )

        assignments = (
            TeacherAssignment.objects.filter(
                section=student.section
            ).select_related(
                "subject"
            )
        )

        subjects = []

        for assignment in assignments:

            total_classes = (
                AttendanceEvent.objects.filter(
                    teacher_assignment=assignment,
                    is_finalized=True
                ).count()
            )

            present_classes = (
                AttendanceRecord.objects.filter(
                    student=student,
                    attendance_event__teacher_assignment=
                    assignment,
                    is_present=True
                ).count()
            )

            percentage = 0

            if total_classes > 0:

                percentage = round(
                    (
                        present_classes
                        /
                        total_classes
                    ) * 100,
                    2
                )

            subjects.append(
                {
                    "subject_id":
                    assignment.subject.id,

                    "subject_name":
                    assignment.subject.name,

                    "subject_code":
                    assignment.subject.code,

                    "attendance_percentage":
                    percentage
                }
            )

        serializer = (
            AdminStudentReportSubjectSerializer(
                subjects,
                many=True
            )
        )

        return Response(
            {
                "student_id":
                student.id,

                "student_name":
                student.name,

                "roll_number":
                student.roll_number,

                "section":
                student.section.name,

                "semester":
                student.section.semester,

                "subjects":
                serializer.data
            }
        )
        
class TeacherCreateView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = (
            TeacherCreateSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data[
            "email"
        ]

        teacher_id = serializer.validated_data[
            "teacher_id"
        ]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=teacher_id
        )

        teacher = Teacher.objects.create(
            user=user,
            teacher_id=teacher_id,
            name=serializer.validated_data[
                "name"
            ],
            email=email
        )

        return Response(
            {
                "teacher_id":
                teacher.id,

                "login_email":
                email,

                "default_password":
                teacher_id
            },
            status=201
        )
        
class LoginView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = LoginSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data[
            "email"
        ]

        password = serializer.validated_data[
            "password"
        ]

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:

            return Response(
                {
                    "error":
                    "Invalid credentials"
                },
                status=401
            )

        refresh = RefreshToken.for_user(
            user
        )

        if hasattr(
            user,
            "student"
        ):

            role = "STUDENT"

        elif hasattr(
            user,
            "teacher"
        ):

            role = "TEACHER"

        else:

            role = "ADMIN"

        return Response(
            {
                "access":
                str(refresh.access_token),

                "refresh":
                str(refresh),

                "role":
                role
            }
        )