import os

# ==============================
# BASE PATHS
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_DIR = os.path.join(BASE_DIR, "database")

EMBEDDINGS_PATH = os.path.join(DATABASE_DIR, "arcface.pkl")

STUDENTS_CSV_PATH = os.path.join(DATABASE_DIR, "students.csv")


# ==============================
# MODEL SETTINGS
# ==============================

MODEL_NAME = "buffalo_l"

MODEL_PROVIDER = ["CPUExecutionProvider"]

DETECTION_SIZE = (640, 640)


# ==============================
# RECOGNITION THRESHOLDS
# ==============================

STRONG_MATCH_THRESHOLD = 0.42

REJECT_THRESHOLD = 0.32