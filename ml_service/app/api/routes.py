from fastapi import APIRouter, UploadFile, File,Form
import json
from app.services.recognizer import recognize_faces
from typing import List

from app.services.embedding_generator import (
    generate_embeddings
)
from app.schemas.recognizer import (
    RecognitionRequest
)
router = APIRouter()


@router.post("/recognize")
async def recognize_students(

    images: List[UploadFile] = File(...),

    students_json: str = Form(...)
):
    image_bytes_list = []
    
    students_data = json.loads(
        students_json
    )

    request_data = (
        RecognitionRequest(
            **students_data
        )
    )

    for image in images:
        content = await image.read()
        image_bytes_list.append(content)

    recognized_students = recognize_faces(
        image_bytes_list,
        request_data.students
    )

    response = []

    for student_id, confidence in (recognized_students.items()):
        response.append(
            {
                "student_id": student_id,
                "confidence": round(confidence, 4)
            }
        )

    return {
        "recognized_students": response,
        "count": len(response)
    }
    
    
@router.post("/generate-embeddings")
async def generate_student_embeddings(
    images: List[UploadFile] = File(...)
):

    image_bytes_list = []

    for image in images:

        content = await image.read()

        image_bytes_list.append(
            content
        )

    embeddings = generate_embeddings(
        image_bytes_list
    )

    return {
        "embeddings": embeddings,
        "count": len(embeddings)
    }