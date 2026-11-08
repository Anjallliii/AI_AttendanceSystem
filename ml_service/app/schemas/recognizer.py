#schemas are like FastAPI's Serializers, the define and also validate data 
from pydantic import BaseModel
from typing import List


#one student and his embeddings
class StudentData(BaseModel):

    student_id: int

    embeddings: List[List[float]]
    
    
#entire section of students 
class RecognitionRequest(BaseModel):

    students: List[StudentData]