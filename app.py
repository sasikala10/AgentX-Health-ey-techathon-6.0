import streamlit as st
import pandas as pd
import numpy as np
import time

# Page configuration
st.set_page_config(page_title="AgentX Health – EY Techathon 6.0", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("AgentX Health")
page = st.sidebar.radio("Go to", ["Home", "Provider Dashboard", "Validation Simulation", "Analytics", "Audit Logs"])

# --- Sample Provider Data ---
data = {
    "Doctor Name": [
        "Dr. A Kumar", "Dr. S Mehta", "Dr. R Iyer", "Dr. L Sharma",
        "Dr. N Verma", "Dr. P Singh", "Dr. K Rao", "Dr. M Das"
    ],
    "Specialty": [
        "Cardiology", "Dermatology", "Neurology", "Orthopedics",
        "Pediatrics", "Oncology", "ENT", "Gynecology"
    ],
    "Phone": [
        "9876543210","9876543211","9876543212","9876543213",
        "9876543214","9876543215","9876543216","9876543217"
    ],
    "Address": [
        "Chennai", "Bengaluru", "Hyderabad", "Mumbai",
        "Delhi", "Kolkata", "Pune", "Jaipur"
    ],
    "Validation Status": [
        "Verified", "Needs Review", "Verified", "Error",
        "Verified", "Needs Review", "Verified", "Error"
    ]
}

df = pd.DataFrame(data)

# --- Audit Logs ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- HOME PAGE ---
if page == "Home":
    st.title("AgentX Health – EY Techathon 6.0")
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910762.png", width=150)
    st.markdown("""
    ### Automated Healthcare Provider Data Validation using Agentic AI

    **Purpose:** Ensure accurate, up-to-date doctor information across healthcare directories.  
    **Features:** Multi-page dashboard, color-coded validation status, AI simulation, analytics, audit logs.  
    **Outcome:** Faster updates, reduced errors, improved patient trust.

    **EY Techathon 6.0 Submission**
    """)
    st.success("Click on the sidebar to navigate through the prototype pages!")

# --- PROVIDER DASHBOARD ---
elif page == "Provider Dashboard":
    st.title("Provider Directory Dashboard")
    st.markdown("Filter and explore provider validation status:")

    # Filters
    specialty_filter = st.multiselect("Select Specialty", df['Specialty'].unique())
    status_filter = st.multiselect("Select Status", df['Validation Status'].unique())
    
    filtered_df = df.copy()
    if specialty_filter:
        filtered_df = filtered_df[filtered_df['Specialty'].isin(specialty_filter)]
    if status_filter:
        filtered_df = filtered_df[filtered_df['Validation Status'].isin(status_filter)]

    # Color-coded table
    def color_status(val):
        if val=="Verified":
            return 'background-color: #d4edda; color: black'
        elif val=="Needs Review":
            return 'background-color: #fff3cd; color: black'
        else:
            return 'background-color: #f8d7da; color: black'

    st.dataframe(filtered_df.style.applymap(color_status, subset=['Validation Status']), height=400)

# --- VALIDATION SIMULATION ---
elif page == "Validation Simulation":
    st.title("Simulate New Provider Validation")
    st.markdown("Enter new provider details and see Agentic AI validation in action!")

    with st.form(key="validation_form"):
        name = st.text_input("Doctor Name")
        specialty = st.selectbox("Specialty", ["Cardiology","Dermatology","Neurology","Orthopedics","Pediatrics","Oncology","ENT","Gynecology"])
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")
        submit_button = st.form_submit_button("Validate")

    if submit_button:
        st.info("Agentic AI validating...")
        time.sleep(1.5)
        # Randomly assign status
        status = np.random.choice(["Verified","Needs Review","Error"], p=[0.6,0.3,0.1])
        st.success(f"{name} ({specialty}) validated: {status}")
        st.balloons() if status=="Verified" else None
        # Append to logs
        st.session_state.logs.append({"Doctor": name, "Specialty": specialty, "Status": status})
        # Also add to main df for dashboard display
        df.loc[len(df)] = [name, specialty, phone, address, status]

# --- ANALYTICS / INSIGHTS ---
elif page == "Analytics":
    st.title("Validation Analytics Dashboard")
    st.markdown("Summary of provider validation status")
    # Status counts
    status_counts = df['Validation Status'].value_counts()
    st.subheader("Validation Status Distribution")
    st.bar_chart(status_counts)

    st.subheader("Doctors by Specialty")
    specialty_counts = df['Specialty'].value_counts()
    st.bar_chart(specialty_counts)

    st.subheader("Pie Chart - Validation Status")
    st.pyplot(df['Validation Status'].value_counts().plot.pie(autopct='%1.1f%%', figsize=(4,4)).figure)

# --- AUDIT LOGS ---
elif page == "Audit Logs":
    st.title("Compliance / Audit Logs")
    if st.session_state.logs:
        logs_df = pd.DataFrame(st.session_state.logs)
        st.dataframe(logs_df)
    else:
        st.info("No logs yet. Simulate some validations!")
