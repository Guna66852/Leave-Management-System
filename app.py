import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Leave Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Register Employee", "Apply Leave", "View Leaves", "Admin Panel"]
)

if menu == "Register Employee":

    st.header("Employee Registration")

    name = st.text_input("Name")
    email = st.text_input("Email")
    employee_id = st.number_input("Employee ID", step=1)

    if st.button("Register"):
        if not name or not email or not employee_id:
            st.error("Please fill all fields")
            st.stop()
            if start_date < date.today():
                st.error("Cannot apply leave in past")
                st.stop()
  
        response = requests.post(
            f"{API_URL}/employees",
            json={"name": name, "email": email, "employee_id": employee_id}
        )

        st.success("Employee Registered")


elif menu == "Apply Leave":

    st.header("Apply Leave")

    employee_id = st.number_input("Employee ID", step=1)
    leave_type = st.selectbox("Leave Type", ["Casual", "Sick"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    reason = st.text_input("Reason")
    if st.button("Apply"):
        if not employee_id or not leave_type or not start_date or not end_date or not reason:
            st.error("Please fill all fields")
            st.stop()
        data = {
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "reason": reason
        }

        requests.post(f"{API_URL}/leave/apply", json=data)

        st.success("Leave Applied")


elif menu == "View Leaves":

    st.header("Leave Requests")

    response = requests.get(f"{API_URL}/leave")

    leaves = response.json()

    for leave in leaves:

        st.write(leave)


elif menu == "Admin Panel":

    st.header("Admin Panel")

    response = requests.get(f"{API_URL}/leave")

    leaves = response.json()

    for leave in leaves:

        st.write(leave)

        if st.button(f"Approve {leave['id']}"):

            requests.put(f"{API_URL}/leave/{leave['id']}/approve")

        if st.button(f"Reject {leave['id']}"):

            requests.put(f"{API_URL}/leave/{leave['id']}/reject")