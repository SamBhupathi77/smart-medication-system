# 💊 Smart Medication Management System

A full-stack healthcare workflow application that helps users manage medications, schedule reminders, track medication adherence, and automatically create Google Calendar reminder events.

---

## 🚀 Features

### Authentication

* User Registration
* User Login
* Session Management

### Medication Management

* Add Medication
* View Medication
* Edit Medication
* Delete Medication

### Schedule Management

* Create Medication Schedules
* Edit Schedules
* Delete Schedules
* Daily Reminder Tracking

### Medication Tracking

* Mark Medication as Taken
* Medication Logging

### Analytics Dashboard

* Total Medications
* Total Schedules
* Medications Taken Today
* Adherence Percentage

### Google Calendar Integration

* OAuth Authentication
* Automatic Calendar Event Creation
* Daily Recurring Reminder Events
* Mobile Notification Support

---

## 🏗️ System Architecture

```text
User
  │
  ▼
Streamlit Frontend
  │
  ▼
FastAPI Backend
  │
  ├── Authentication
  ├── Medication APIs
  ├── Schedule APIs
  ├── Analytics APIs
  │
  ▼
SQLite Database
  │
  ▼
Google Calendar API
```

---

## 📸 Screenshots

### Login Page

![Login](screenshots/login.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

---

## 🛠️ Technology Stack

### Frontend

* Streamlit

### Backend

* FastAPI

### Database

* SQLite

### ORM

* SQLAlchemy

### Scheduling

* APScheduler

### External Integration

* Google Calendar API
* OAuth 2.0

---

## 📂 Database Design

### Users

* id
* name
* email
* password

### Medications

* id
* user_id
* name
* dosage

### Schedules

* id
* medication_id
* reminder_time

### Medication Logs

* id
* schedule_id
* taken_date
* taken

---

## ⚙️ Installation
Fastapi,
Streamlit,
Python,
Sqlite,
Sqlalchemy,
Google-calendar-api,
Healthcare,
Rest-api,
Full-stack.
### Clone Repository

```bash
git clone https://github.com/SamBhupathi77/smart-medication-system.git

cd smart-medication-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn backend.main:app --reload
```

### Run Frontend

```bash
streamlit run frontend/app.py
```

---

## 🔄 Workflow

1. User Registers/Login
2. User Adds Medication
3. User Creates Schedule
4. Schedule Stored in Database
5. Google Calendar Event Created Automatically
6. Reminder Appears on User Calendar
7. User Marks Medication as Taken
8. Medication Log Updated
9. Analytics Dashboard Updated

---

## 🎯 Future Enhancements

* JWT Authentication
* Email Notifications
* WhatsApp Notifications
* PostgreSQL Migration
* Docker Deployment
* Multi-User Google Calendar OAuth

---

## 👨‍💻 Author

Sam Bhupathi

Final Year Engineering Student

Interested in:

* Machine Learning
* Deep Learning
* Large Language Models
* Full Stack Development
