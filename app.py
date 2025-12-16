import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="AgentX Health – EY Techathon 6.0", layout="wide")

# Sidebar navigation
st.sidebar.title("AgentX Health")
page = st.sidebar.radio("Navigation", ["Home", "Provider Dashboard", "Validation Simulation", "Analytics", "Audit Logs"])

# Sample data
data = {
    "Doctor Name": ["Dr. A Kumar", "Dr. S Mehta", "Dr. R Iyer", "Dr. L Sharma"],
    "Specialty": ["Cardiology", "Dermatology", "Neurology", "Orthopedics"],
    "Phone": ["9876543210", "9876543210", "9876543210", "9876543210"],
    "Address": ["Chennai", "Bengaluru", "Hyderabad", "Mumbai"],
    "Validation Status": ["Verified", "Needs Review", "Verified", "Error"]
}
df = pd.DataFrame(data)

# --- Home Page ---
if page == "Home":
    st.title("AgentX Health – EY Techathon 6.0")
    st.markdown("### Automated Provider Data Validation using Agentic AI")
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910762.png", width=150)
    st.markdown("""
    **Purpose:** Ensure accurate and up-to-date doctor information across all healthcare directories.  
    **Features:** Multi-page dashboard, AI validation simulation, analytics, compliance logs.  
    **Outcome:** Faster updates, reduced errors, improved patient trust.
    """)

# --- Provider Dashboard ---
elif page == "Provider Dashboard":
    st.title("Provider Directory Dashboard")
    st.markdown("Filter and explore provider validation status:")
    specialty_filter = st.multiselect("Select Specialty", df['Specialty'].unique())
    status_filter = st.multiselect("Select Status", df['Validation Status'].unique())
    
    filtered_df = df.copy()
    if specialty_filter:
        filtered_df = filtered_df[filtered_df['Specialty'].isin(specialty_filter)]
    if status_filter:
        filtered_df = filtered_df[filtered_df['Validation Status'].isin(status_filter)]
    
    # Color-coded display
    def color_status(val):
        if val=="Verified":
            color="background-color: #d4edda"
        elif val=="Needs Review":
            color="background-color: #fff3cd"
        else:
            color="background-color: #f8d7da"
        return color

    st.dataframe(filtered_df.style.applymap(color_status, subset=['Validation Status']), height=400)

# --- Validation Simulation ---
elif page == "Validation Simulation":
    st.title("Simulate New Provider Validation")
    with st.form(key="validation_form"):
        name = st.text_input("Doctor Name")
        specialty = st.selectbox("Specialty", ["Cardiology", "Dermatology", "Neurology", "Orthopedics"])
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")
        submit_button = st.form_submit_button("Validate")
    
    if submit_button:
        st.info("Agentic AI validating...")
        time.sleep(1.5)
        status = np.random.choice(["Verified","Needs Review"])
        st.success(f"{name} ({specialty}) validated: {status}")
        st.balloons()

# --- Analytics / Insights ---
elif page == "Analytics":
    st.title("Validation Analytics")
    st.markdown("Summary of provider validation status")
    status_counts = df['Validation Status'].value_counts()
    st.bar_chart(status_counts)
    st.pie_chart(status_counts)

# --- Audit Logs ---
elif page == "Audit Logs":
    st.title("Compliance / Audit Logs")
    logs = {
        "Event": ["Added Dr. A Kumar", "Validated Dr. S Mehta", "Error Dr. L Sharma"],
        "Timestamp": ["2025-12-16 10:00", "2025-12-16 10:05", "2025-12-16 10:08"],
        "Status": ["Verified", "Verified", "Error"]
    }
    st.dataframe(pd.DataFrame(logs))
