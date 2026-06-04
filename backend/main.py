from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date
from backend.calender_service import (
    create_calendar_event
)

from datetime import datetime
from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from backend.database import (
    engine,
    get_db
)

from backend.models import (
    Base,
    MedicationLog,
    User,
    Medication,
    Schedule
)

from backend.schemas import (
    UserCreate,
    UserLogin,
    MedicationCreate,
    ScheduleCreate
)

from backend.reminder_service import (
    check_reminders
)


# =====================================
# CREATE DATABASE TABLES
# =====================================

Base.metadata.create_all(bind=engine)


# =====================================
# FASTAPI APP
# =====================================

app = FastAPI()


# =====================================
# BACKGROUND SCHEDULER
# =====================================

scheduler = BackgroundScheduler()

scheduler.add_job(
    check_reminders,
    "interval",
    minutes=1
)

scheduler.start()


# =====================================
# HOME ROUTE
# =====================================

@app.get("/")
def home():

    return {
        "message":
        "Smart Medication System Running"
    }


# =====================================
# REGISTER API
# =====================================

@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:

        return {
            "success": False,
            "message":
            "Email already registered"
        }

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "success": True,
        "message":
        "User registered successfully",
        "user_id": new_user.id
    }


# =====================================
# LOGIN API
# =====================================

@app.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not db_user:

        return {
            "success": False,
            "message": "User not found"
        }

    if db_user.password != user.password:

        return {
            "success": False,
            "message":
            "Incorrect password"
        }

    return {
        "success": True,
        "message": "Login successful",
        "user_id": db_user.id,
        "name": db_user.name
    }


# =====================================
# ADD MEDICATION
# =====================================

@app.post("/medications")
def add_medication(
    medication: MedicationCreate,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id ==
            medication.user_id
        )
        .first()
    )

    if not user:

        return {
            "success": False,
            "message": "User not found"
        }

    new_medication = Medication(
        user_id=medication.user_id,
        name=medication.name,
        dosage=medication.dosage
    )

    db.add(new_medication)

    db.commit()

    db.refresh(new_medication)

    return {
        "success": True,
        "message": "Medication added",
        "medication_id":
        new_medication.id
    }


# =====================================
# GET MEDICATIONS
# =====================================

@app.get("/users/{user_id}/medications")
def get_medications(
    user_id: int,
    db: Session = Depends(get_db)
):

    medications = (
        db.query(Medication)
        .filter(
            Medication.user_id == user_id
        )
        .all()
    )

    return medications


# =====================================
# UPDATE MEDICATION
# =====================================

# =====================================
# UPDATE MEDICATION
# =====================================

@app.put("/medications/{medication_id}")
def update_medication(
    medication_id: int,
    medication: MedicationCreate,
    db: Session = Depends(get_db)
):

    db_medication = (
        db.query(Medication)
        .filter(
            Medication.id == medication_id
        )
        .first()
    )

    if not db_medication:

        return {
            "success": False,
            "message":
            "Medication not found"
        }

    db_medication.name = medication.name

    db_medication.dosage = medication.dosage

    db.commit()

    db.refresh(db_medication)

    return {
        "success": True,
        "message":
        "Medication updated successfully"
    }


# =====================================
# ADD SCHEDULE
# =====================================

@app.post("/schedules")
def add_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db)
):

    medication = (
        db.query(Medication)
        .filter(
            Medication.id ==
            schedule.medication_id
        )
        .first()
    )

    if not medication:

        return {
            "success": False,
            "message":
            "Medication not found"
        }

    reminder_time = datetime.strptime(
        schedule.reminder_time,
        "%H:%M"
    ).time()

    new_schedule = Schedule(
        medication_id=
        schedule.medication_id,

        reminder_time=
        reminder_time
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    calendar_link = create_calendar_event(medication.name, schedule.reminder_time)

    return {
        "success": True,
        "message": "Schedule added",
        "calendar_link": calendar_link,
    }


# =====================================
# GET MEDICATION SCHEDULES
# =====================================

@app.get(
    "/medications/{medication_id}/schedules"
)
def get_schedules(
    medication_id: int,
    db: Session = Depends(get_db)
):

    schedules = (
        db.query(Schedule)
        .filter(
            Schedule.medication_id
            == medication_id
        )
        .all()
    )

    return schedules


# =====================================
# GET USER SCHEDULES
# =====================================

@app.get("/users/{user_id}/schedules")
def get_user_schedules(
    user_id: int,
    db: Session = Depends(get_db)
):

    medications = (
        db.query(Medication)
        .filter(
            Medication.user_id == user_id
        )
        .all()
    )

    schedules_data = []

    for med in medications:

        schedules = (
            db.query(Schedule)
            .filter(
                Schedule.medication_id
                == med.id
            )
            .all()
        )

        for sched in schedules:

            schedules_data.append({

                "schedule_id":
                sched.id,

                "medication_name":
                med.name,

                "dosage":
                med.dosage,

                "reminder_time":
                str(sched.reminder_time)
            })

    return schedules_data


# =====================================
# UPDATE SCHEDULE
# =====================================


@app.put("/schedules/{schedule_id}")
def update_schedule(
    schedule_id: int,
    schedule: ScheduleCreate,
    db: Session = Depends(get_db)
):

    db_schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id
        )
        .first()
    )

    if not db_schedule:

        return {
            "success": False,
            "message":
            "Schedule not found"
        }

    reminder_time = datetime.strptime(
        schedule.reminder_time,
        "%H:%M"
    ).time()

    db_schedule.reminder_time = (
        reminder_time
    )

    db.commit()

    db.refresh(db_schedule)

    return {
        "success": True,
        "message":
        "Schedule updated successfully"
    }
@app.post("/logs/{schedule_id}/take")
def mark_medication_taken(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    today = date.today()

    existing_log = (
        db.query(MedicationLog)
        .filter(
            MedicationLog.schedule_id
            == schedule_id,

            MedicationLog.date == today
        )
        .first()
    )

    if existing_log:

        existing_log.taken = True

    else:

        new_log = MedicationLog(
            schedule_id=schedule_id,
            date=today,
            taken=True
        )

        db.add(new_log)

    db.commit()

    return {
        "success": True,
        "message":
        "Medication marked as taken"
    }
# =====================================
# DELETE MEDICATION
# =====================================

@app.delete("/medications/{medication_id}")
def delete_medication(
    medication_id: int,
    db: Session = Depends(get_db)
):

    medication = (
        db.query(Medication)
        .filter(
            Medication.id == medication_id
        )
        .first()
    )

    if not medication:

        return {
            "success": False,
            "message":
            "Medication not found"
        }

    schedules = (
        db.query(Schedule)
        .filter(
            Schedule.medication_id
            == medication_id
        )
        .all()
    )

    for sched in schedules:

        db.delete(sched)

    db.delete(medication)

    db.commit()

    return {
        "success": True,
        "message":
        "Medication deleted"
    }

# =====================================
# DELETE SCHEDULE
# =====================================

@app.delete("/schedules/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id
        )
        .first()
    )

    if not schedule:

        return {
            "success": False,
            "message":
            "Schedule not found"
        }

    db.delete(schedule)

    db.commit()

    return {
        "success": True,
        "message":
        "Schedule deleted"
    }

@app.delete("/medications/{medication_id}")
def delete_medication(
    medication_id: int,
    db: Session = Depends(get_db)
):

    medication = (
        db.query(Medication)
        .filter(
            Medication.id == medication_id
        )
        .first()
    )

    if not medication:

        return {
            "success": False,
            "message":
            "Medication not found"
        }

    schedules = (
        db.query(Schedule)
        .filter(
            Schedule.medication_id
            == medication_id
        )
        .all()
    )

    for sched in schedules:

        db.delete(sched)

    db.delete(medication)

    db.commit()

    return {
        "success": True,
        "message":
        "Medication deleted"
    }

@app.delete("/schedules/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id
        )
        .first()
    )

    if not schedule:

        return {
            "success": False,
            "message":
            "Schedule not found"
        }

    db.delete(schedule)

    db.commit()

    return {
        "success": True,
        "message":
        "Schedule deleted"
    }
@app.get("/logs/{schedule_id}/today")
def get_today_status(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    today = date.today()

    log = (
        db.query(MedicationLog)
        .filter(
            MedicationLog.schedule_id == schedule_id,
            MedicationLog.date == today
        )
        .first()
    )

    return {
        "taken": bool(log and log.taken)
    }
@app.get("/analytics/{user_id}")
def get_analytics(
    user_id: int,
    db: Session = Depends(get_db)
):

    medications = (
        db.query(Medication)
        .filter(
            Medication.user_id == user_id
        )
        .all()
    )

    medication_count = len(
        medications
    )

    schedules = []

    for med in medications:

        med_schedules = (
            db.query(Schedule)
            .filter(
                Schedule.medication_id
                == med.id
            )
            .all()
        )

        schedules.extend(
            med_schedules
        )

    schedule_count = len(
        schedules
    )

    today = date.today()

    taken_today = (
        db.query(MedicationLog)
        .filter(
            MedicationLog.date
            == today,

            MedicationLog.taken
            == True
        )
        .count()
    )

    adherence = 0

    if schedule_count > 0:

        adherence = round(
            (
                taken_today
                / schedule_count
            )
            * 100,
            2
        )

    return {

        "medications":
        medication_count,

        "schedules":
        schedule_count,

        "taken_today":
        taken_today,

        "adherence":
        adherence
    }