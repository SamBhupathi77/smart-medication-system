from pydantic import BaseModel
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class MedicationCreate(BaseModel):
    user_id: int
    name: str
    dosage: str

class ScheduleCreate(BaseModel):
    medication_id: int
    reminder_time: str   