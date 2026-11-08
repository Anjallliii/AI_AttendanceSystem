import cv2
import numpy as np

from app.services.face_model import app


def generate_embeddings(image_list):

    embeddings = []

    for image_bytes in image_list:

        nparr = np.frombuffer(
            image_bytes,
            np.uint8
        )

        img = cv2.imdecode(
            nparr,
            cv2.IMREAD_COLOR
        )

        if img is None:
            continue

        faces = app.get(img)

        if len(faces) == 0:
            continue

        face = max(
            faces,
            key=lambda x:
            x.bbox[2] - x.bbox[0]
        )

        embedding = face.embedding

        embedding = (
            embedding /
            np.linalg.norm(
                embedding
            )
        )

        embeddings.append(
            embedding.tolist()
        )

    return embeddings