from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import Date

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)

    dosage = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


   # Line 34: The class definition starts at the far left margin
class Schedule(Base):
    # Line 35 and onwards: Everything inside MUST be indented by 4 spaces!
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"))
    reminder_time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicationLog(Base):

    __tablename__ = "medication_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    schedule_id = Column(
        Integer,
        ForeignKey("schedules.id")
    )

    date = Column(Date)

    taken = Column(
        Boolean,
        default=False
    )