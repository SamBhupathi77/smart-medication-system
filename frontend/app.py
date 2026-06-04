import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Smart Medication System",
    page_icon="💊",
    layout="wide",
)

st.title("💊 Smart Medication System")
st.caption("Helping users take medicines on time.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn"):
            try:
                response = requests.post(
                    f"{BASE_URL}/login",
                    json={"email": login_email, "password": login_password},
                )
                result = response.json()

                if result.get("success"):
                    st.session_state.logged_in = True
                    st.session_state.user_id = result.get("user_id")
                    st.session_state.user_name = result.get("name")
                    st.rerun()
                else:
                    st.error(result.get("message", "Login failed"))
            except Exception as e:
                st.error(str(e))

    with tab2:
        st.subheader("Create Account")
        register_name = st.text_input("Name", key="register_name")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("Password", type="password", key="register_password")

        if st.button("Register", key="register_btn"):
            try:
                response = requests.post(
                    f"{BASE_URL}/register",
                    json={
                        "name": register_name,
                        "email": register_email,
                        "password": register_password,
                    },
                )
                result = response.json()

                if result.get("success"):
                    st.success(result.get("message", "Account created"))
                else:
                    st.error(result.get("message", "Registration failed"))
            except Exception as e:
                st.error(str(e))

else:
    st.sidebar.success(f"Welcome {st.session_state.user_name}")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "➕ Add Medication",
            "💊 View Medications",
            "📅 Add Schedule",
            "⏰ View Schedules",
        ],
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.rerun()

    if page == "🏠 Dashboard":
        st.success(f"Welcome back {st.session_state.user_name} 👋")

        try:
            analytics_response = requests.get(f"{BASE_URL}/analytics/{st.session_state.user_id}")
            analytics = analytics_response.json()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💊 Medications", analytics.get("medications", 0))
            col2.metric("⏰ Schedules", analytics.get("schedules", 0))
            col3.metric("✅ Taken Today", analytics.get("taken_today", 0))
            col4.metric("📈 Adherence %", analytics.get("adherence", 0))

            st.markdown("---")
            st.subheader("🔔 Today's Reminders")

            sched_response = requests.get(f"{BASE_URL}/users/{st.session_state.user_id}/schedules")
            schedules = sched_response.json()

            if schedules:
                for sched in schedules:
                    st.warning(f"💊 {sched['medication_name']}")
                    st.caption(f"⏰ {sched['reminder_time']}")

                    try:
                        status_response = requests.get(f"{BASE_URL}/logs/{sched['schedule_id']}/today")
                        status = status_response.json()

                        if status.get("taken"):
                            st.success("Already Taken ✅")
                        else:
                            if st.button("Mark as Taken", key=f"take_{sched['schedule_id']}"):
                                take_response = requests.post(f"{BASE_URL}/logs/{sched['schedule_id']}/take")
                                result = take_response.json()

                                if result.get("success"):
                                    st.success("Medication Taken ✅")
                                    st.rerun()
                                else:
                                    st.error(result.get("message", "Could not log medication"))
                    except Exception:
                        st.error("Could not load reminder status")
            else:
                st.info("No reminders today")

        except Exception:
            st.warning("Unable to load dashboard metrics")

    elif page == "➕ Add Medication":
        st.subheader("➕ Add Medication")
        medication_name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")

        if st.button("Add Medication"):
            response = requests.post(
                f"{BASE_URL}/medications",
                json={
                    "user_id": st.session_state.user_id,
                    "name": medication_name,
                    "dosage": dosage,
                },
            )
            result = response.json()

            if result.get("success"):
                st.success("Medication Added")
                st.rerun()
            else:
                st.error(result.get("message", "Could not add medication"))

    elif page == "💊 View Medications":
        st.subheader("💊 Your Medications")

        response = requests.get(f"{BASE_URL}/users/{st.session_state.user_id}/medications")
        medications = response.json()

        if medications:
            for med in medications:
                st.markdown("---")
                st.info(f"💊 {med['name']} | {med['dosage']}")

                col1, col2 = st.columns([3, 1])

                with col1:
                    with st.expander("✏️ Edit Medication"):
                        new_name = st.text_input("Medication Name", value=med["name"], key=f"name_{med['id']}")
                        new_dosage = st.text_input("Dosage", value=med["dosage"], key=f"dosage_{med['id']}")

                        if st.button("Save Changes", key=f"save_med_{med['id']}"):
                            response = requests.put(
                                f"{BASE_URL}/medications/{med['id']}",
                                json={
                                    "user_id": st.session_state.user_id,
                                    "name": new_name,
                                    "dosage": new_dosage,
                                },
                            )
                            result = response.json()

                            if result.get("success"):
                                st.success("Medication Updated")
                                st.rerun()
                            else:
                                st.error(result.get("message", "Update failed"))

                with col2:
                    if st.button("🗑 Delete", key=f"delete_{med['id']}"):
                        response = requests.delete(f"{BASE_URL}/medications/{med['id']}")
                        result = response.json()

                        if result.get("success"):
                            st.success("Medication Deleted")
                            st.rerun()
                        else:
                            st.error(result.get("message", "Delete failed"))
        else:
            st.info("No medications found")

    elif page == "📅 Add Schedule":
        st.subheader("📅 Add Schedule")

        response = requests.get(f"{BASE_URL}/users/{st.session_state.user_id}/medications")
        medications = response.json()

        if medications:
            medication_options = {f"{med['name']} ({med['dosage']})": med["id"] for med in medications}
            selected_medication = st.selectbox("Select Medication", list(medication_options.keys()))
            reminder_time = st.text_input("Reminder Time (HH:MM)")

            if st.button("Add Schedule"):
                response = requests.post(
                    f"{BASE_URL}/schedules",
                    json={
                        "medication_id": medication_options[selected_medication],
                        "reminder_time": reminder_time,
                    },
                )
                result = response.json()

                if result.get("success"):
                    st.success("Schedule Added")
                    st.rerun()
                else:
                    st.error(result.get("message", "Could not add schedule"))
        else:
            st.warning("Add medication first")

    elif page == "⏰ View Schedules":
        st.subheader("⏰ Your Schedules")

        response = requests.get(f"{BASE_URL}/users/{st.session_state.user_id}/schedules")
        schedules = response.json()

        if schedules:
            for sched in schedules:
                st.markdown("---")
                st.warning(f"💊 {sched['medication_name']}")
                st.caption(f"⏰ {sched['reminder_time']}")

                col1, col2 = st.columns([3, 1])

                with col1:
                    with st.expander("✏️ Edit Schedule"):
                        current_time = sched["reminder_time"][:5]
                        new_time = st.text_input("Reminder Time (HH:MM)", value=current_time, key=f"time_{sched['schedule_id']}")

                        if st.button("Save Schedule", key=f"save_sched_{sched['schedule_id']}"):
                            response = requests.put(
                                f"{BASE_URL}/schedules/{sched['schedule_id']}",
                                json={
                                    "medication_id": sched.get("medication_id", 1),
                                    "reminder_time": new_time,
                                },
                            )
                            result = response.json()

                            if result.get("success"):
                                st.success("Schedule Updated")
                                st.rerun()
                            else:
                                st.error(result.get("message", "Update failed"))

                with col2:
                    if st.button("🗑 Delete", key=f"delete_sched_{sched['schedule_id']}"):
                        response = requests.delete(f"{BASE_URL}/schedules/{sched['schedule_id']}")
                        result = response.json()

                        if result.get("success"):
                            st.success("Schedule Deleted")
                            st.rerun()
                        else:
                            st.error(result.get("message", "Delete failed"))
        else:
            st.info("No schedules found")
