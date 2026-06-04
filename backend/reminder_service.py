from datetime import datetime
from backend.database import SessionLocal
from backend.models import Schedule, Medication

def check_reminders():
    db = SessionLocal()
    try:
        # Get current time string in 24-hour format "HH:MM"
        current_time = datetime.now().strftime("%H:%M")
        
        schedules = db.query(Schedule).all()
        
        for schedule in schedules:
            db_time_str = ""
            
            # Handle if SQLite returned a datetime object or a string
            if hasattr(schedule.reminder_time, "strftime"):
                db_time_str = schedule.reminder_time.strftime("%H:%M")
            else:
                # If it's a string like "03:57:00", strip it to "03:57"
                db_time_str = str(schedule.reminder_time)[:5]
            
            # Debugging logs to verify your comparison
            print(f"[Match Check] System Time: {current_time} | DB Schedule: {db_time_str}")
            
            if db_time_str == current_time:
                medication = db.query(Medication).filter(Medication.id == schedule.medication_id).first()
                if medication:
                    print("\n🚨 ========================")
                    print("         REMINDER         ")
                    print(f" Take {medication.name} ({medication.dosage})")
                    print(f" Scheduled Time: {db_time_str}")
                    print(" ========================\n")
                    
    except Exception as e:
        print(f"❌ Scheduler Error: {e}")
    finally:
        db.close()