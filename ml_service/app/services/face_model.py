from insightface.app import FaceAnalysis

from app.core.config import (
    MODEL_NAME,
    MODEL_PROVIDER,
    DETECTION_SIZE
)

app = FaceAnalysis(
    name=MODEL_NAME,
    providers=MODEL_PROVIDER
)

app.prepare(
    ctx_id=0,
    det_size=DETECTION_SIZE
)