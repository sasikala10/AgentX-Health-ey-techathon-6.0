import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image

# --- Page configuration ---
st.set_page_config(page_title="AgentX Health – EY Techathon", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("AgentX Health")
page = st.sidebar.radio("Go to", ["Home", "Provider Dashboard", "Validation Simulation", "Analytics", "Audit Logs"])

# --- Sample Doctor Data with Images ---
doctor_data = [
    {"name": "Dr. A Kumar", "specialty": "Cardiology", "phone":"9876543210","address":"Chennai","image":"dr_a_kumar.png"},
    {"name": "Dr. S Mehta", "specialty": "Dermatology", "phone":"9876543211","address":"Bengaluru","image":"dr_s_mehta.png"},
    {"name": "Dr. R Iyer", "specialty": "Neurology", "phone":"9876543212","address":"Hyderabad","image":"dr_r_iyer.png"},
    {"name": "Dr. L Sharma", "specialty": "Orthopedics", "phone":"9876543213","address":"Mumbai","image":"dr_l_sharma.png"},
    {"name": "Dr. N Verma", "specialty": "Pediatrics", "phone":"9876543214","address":"Delhi","image":"dr_n_verma.png"},
    {"name": "Dr. P Singh", "specialty": "Oncology", "phone":"9876543215","address":"Kolkata","image":"dr_p_singh.png"},
    {"name": "Dr. K Rao", "specialty": "ENT", "phone":"9876543216","address":"Pune","image":"dr_k_rao.png"},
    {"name": "Dr. M Das", "specialty": "Gynecology", "phone":"9876543217","address":"Jaipur","image":"dr_m_das.png"}
]

# Convert to DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(doctor_data)
    st.session_state.df['Validation Status'] = np.random.choice(["Verified","Needs Review","Error"], len(doctor_data), p=[0.6,0.3,0.1])

# --- Audit Logs ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- HOME PAGE ---
if page == "Home":
    st.markdown("""
    <h1 style='text-align: center; color: #2E86C1; font-size:60px;'>
    AgentX Health
    </h1>
    """, unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910762.png", width=150)
    st.markdown("""
    ### Automated Healthcare Provider Data Validation using Agentic AI
    **Purpose:** Ensure accurate, up-to-date doctor information across healthcare directories.  
    **Features:** Multi-page dashboard, color-coded validation status, AI simulation, analytics, audit logs.  
    **Outcome:** Faster updates, reduced errors, improved patient trust.  
    """)

# --- PROVIDER DASHBOARD ---
elif page == "Provider Dashboard":
    st.title("Provider Directory Dashboard")
    st.markdown("Filter and explore provider validation status:")
    
    specialty_filter = st.multiselect("Select Specialty", st.session_state.df['specialty'].unique())
    status_filter = st.multiselect("Select Status", st.session_state.df['Validation Status'].unique())
    
    df_filtered = st.session_state.df.copy()
    if specialty_filter:
        df_filtered = df_filtered[df_filtered['specialty'].isin(specialty_filter)]
    if status_filter:
        df_filtered = df_filtered[df_filtered['Validation Status'].isin(status_filter)]
    
    # Display doctors in grid with images
    for i in range(0, len(df_filtered), 4):
        cols = st.columns(4)
        for j, idx in enumerate(range(i, min(i+4, len(df_filtered)))):
            with cols[j]:
                doc = df_filtered.iloc[idx]
                img = Image.open(doc['image'])
                st.image(img, width=100)
                st.markdown(f"**{doc['name']}**")
                st.markdown(f"{doc['specialty']}")
                # Color-coded status
                status = doc['Validation Status']
                color = "#d4edda" if status=="Verified" else "#fff3cd" if status=="Needs Review" else "#f8d7da"
                st.markdown(f"<div style='background-color:{color}; padding:5px; text-align:center;'>{status}</div>", unsafe_allow_html=True)

# --- VALIDATION SIMULATION ---
elif page == "Validation Simulation":
    st.title("Simulate New Provider Validation")
    with st.form(key="validation_form"):
        name = st.text_input("Doctor Name")
        specialty = st.selectbox("Specialty", st.session_state.df['specialty'].unique())
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")
        submit_button = st.form_submit_button("Validate")
    
    if submit_button:
        st.info("Agentic AI validating...")
        time.sleep(1.5)
        status = np.random.choice(["Verified","Needs Review","Error"], p=[0.6,0.3,0.1])
        st.success(f"{name} ({specialty}) validated: {status}")
        if status=="Verified": st.balloons()
        # Add to df & logs
        new_doc = {"name":name, "specialty":specialty, "phone":phone, "address":address, "image":"https://cdn-icons-png.flaticon.com/512/2910/2910762.png", "Validation Status":status}
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_doc])], ignore_index=True)
        st.session_state.logs.append(new_doc)

# --- ANALYTICS ---
elif page == "Analytics":
    st.title("Validation Analytics")
    status_counts = st.session_state.df['Validation Status'].value_counts()
    st.bar_chart(status_counts)
    st.subheader("Doctors by Specialty")
    st.bar_chart(st.session_state.df['specialty'].value_counts())

# --- AUDIT LOGS ---
elif page == "Audit Logs":
    st.title("Audit Logs")
    if st.session_state.logs:
        st.dataframe(pd.DataFrame(st.session_state.logs))
    else:
        st.info("No logs yet. Run some validation simulations!")
