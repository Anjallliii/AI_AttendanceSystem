# AI-Powered Face Recognition Attendance Management System

An AI-powered attendance management system that automates classroom attendance marking using facial recognition. The system combines a Django-based backend, a FastAPI-based machine learning service, and ArcFace facial embeddings to identify students from classroom images and generate attendance records automatically.

## Features

* Automated attendance marking from classroom images
* ArcFace-based facial recognition using InsightFace
* Student enrollment with multiple face images
* Facial embedding generation and storage
* Cosine similarity-based face matching
* Multi-image classroom attendance processing
* Teacher verification and attendance finalization workflow
* JWT Authentication
* Role-Based Access Control (Admin, Teacher, Student)
* Subject-wise attendance tracking
* Student attendance history and analytics
* RESTful API architecture
* Separate ML and Backend services for scalability

---

## System Architecture

```text
Frontend (React)
        |
        v
Django Backend
(Authentication, Attendance Management, APIs)
        |
        v
FastAPI ML Service
(Face Detection, ArcFace Embeddings, Recognition)
        |
        v
Database
(Student Data, Embeddings, Attendance Records)
```

---

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework
* JWT Authentication

### Machine Learning Service

* FastAPI
* InsightFace
* ArcFace
* OpenCV
* NumPy

### Database

* SQLite (Development)

### Face Recognition Pipeline

* Face Detection
* ArcFace Embedding Generation
* Embedding Storage
* Cosine Similarity Matching
* Attendance Generation

---

## Attendance Workflow

### Student Enrollment

1. Admin creates student profile.
2. Multiple student images are uploaded.
3. ArcFace generates facial embeddings.
4. Embeddings are stored in the database.

### Attendance Processing

1. Teacher uploads multiple classroom images.
2. Faces are detected and extracted.
3. ArcFace generates embeddings for detected faces.
4. Cosine similarity is used to compare classroom embeddings with stored student embeddings.
5. Attendance is generated automatically.
6. Teacher verifies the results.
7. Attendance is finalized and stored.

---

## User Roles

### Admin

* Manage students
* Manage teachers
* Manage subjects
* Assign teachers to subjects and sections
* View attendance reports

### Teacher

* Upload classroom images
* Verify attendance predictions
* Finalize attendance records
* View attendance registers

### Student

* View assigned subjects
* Track attendance history
* Monitor attendance percentage

---

## Project Structure

```text
AI-Face-Recognition-Attendance-System/

├── attendance_backend/
│   ├── attendance/
│   ├── config/
│   └── manage.py
│
├── ml_service/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── database/
│   │   └── utils/
│   └── main.py
│
├── README.md
└── .gitignore
```

---

## Key Learning Outcomes

* Backend API Development with Django REST Framework
* JWT Authentication and Authorization
* Role-Based Access Control (RBAC)
* Multi-Service Architecture (Django + FastAPI)
* Computer Vision and Face Recognition
* ArcFace Embedding Generation
* Cosine Similarity-Based Matching
* Database Design and Modeling
* AI Service Integration into Production Workflows

---

## Future Improvements

* PostgreSQL Integration
* React Frontend Dashboard
* Attendance Risk Prediction
* Real-Time Attendance Processing
* Liveness Detection for Anti-Spoofing
* Advanced Attendance Analytics
* Cloud Deployment

---


