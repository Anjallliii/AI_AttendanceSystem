import cv2
import numpy as np

from app.services.face_model import app
from app.core.config import (
    STRONG_MATCH_THRESHOLD,
    REJECT_THRESHOLD
)





# ==============================
# SIMILARITY FUNCTION
# ==============================

def cosine_similarity(a, b):
    return np.dot(a, b)

# ==============================
# RECOGNITION FUNCTION
# ==============================

def recognize_faces(
    image_list,
    students
):

    recognized_students = {}

    for image_bytes in image_list:

        # Convert bytes to image
        nparr = np.frombuffer(image_bytes, np.uint8)

        img = cv2.imdecode(
            nparr,
            cv2.IMREAD_COLOR
        )

        if img is None:
            continue

        faces = app.get(img)

        for face in faces:

            emb = face.embedding

            emb = emb / np.linalg.norm(emb)

            best_student_id = None

            best_score = -1


            for student in students:

                student_best_score = -1

                for stored_embedding in student.embeddings:

                    stored_embedding = np.array(
                        stored_embedding
                    )

                    score = cosine_similarity(
                        stored_embedding,
                        emb
                    )

                    if score > student_best_score:

                        student_best_score = score

                if student_best_score > best_score:

                    best_score = student_best_score

                    best_student_id = (
                        student.student_id
                    )


            if best_score < REJECT_THRESHOLD:

                continue


            if best_score >= STRONG_MATCH_THRESHOLD:

                if (
                    best_student_id
                    not in recognized_students
                    or
                    best_score >
                    recognized_students[
                        best_student_id
                    ]
                ):

                    recognized_students[
                        best_student_id
                    ] = float(best_score)

    return recognized_students