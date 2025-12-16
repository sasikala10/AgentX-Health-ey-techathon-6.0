import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import requests
from io import BytesIO

# --- Page configuration ---
st.set_page_config(page_title="AgentX Health – EY Techathon", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("AgentX Health")
page = st.sidebar.radio("Go to", ["Home", "Provider Dashboard", "Validation Simulation", "Analytics", "Audit Logs"])

# --- Sample Doctor Data with Image URLs ---
doctor_data = [
    {"name": "Dr. A Kumar", "specialty": "Cardiology", "phone":"9876543210","address":"Chennai","image":"https://img.freepik.com/premium-photo/portrait-handsome-young-doctor-standing-against-white-background-created-with-generative-ai_762026-44070.jpg"},
    {"name": "Dr. S Mehta", "specialty": "Dermatology", "phone":"9876543211","address":"Bengaluru","image":"https://th.bing.com/th/id/R.256ff89b8455578cb07f46a207a4d6ae?rik=wamzqu6ozFnjjw&riu=http%3a%2f%2fwww.publicdomainpictures.net%2fpictures%2f210000%2fvelka%2fdoctor-1490804643Rfi.jpg&ehk=xVsfwkQ4RsL0lPNklpn0uYssY%2fJJqHho%2bhw1KPmGMXU%3d&risl=&pid=ImgRaw&r=0"},
    {"name": "Dr. R Iyer", "specialty": "Neurology", "phone":"9876543212","address":"Hyderabad","image":"https://as2.ftcdn.net/v2/jpg/06/46/17/19/1000_F_646171981_LhX2Z9Us0c7pSIcfvzgRkZeQIzsuuLNa.jpg"},
    {"name": "Dr. L Sharma", "specialty": "Orthopedics", "phone":"9876543213","address":"Mumbai","image":"https://thumbs.dreamstime.com/z/portrait-medical-doctor-clipboard-stethoscope-isolated-white-151729203.jpg"},
    {"name": "Dr. N Rithika", "specialty": "Pediatrics", "phone":"9876543214","address":"Delhi","image":"https://img.freepik.com/premium-photo/portrait-young-beautiful-smiling-indian-female-doctor-standing-isolated-background_1025753-91569.jpg?w=360"},
    {"name": "Dr. P  Preetha Singh", "specialty": "Oncology", "phone":"9876543215","address":"Kolkata","image":"https://img.freepik.com/premium-photo/indian-doctor-wearing-white-coat-with-stethoscope_85574-3676.jpg"},
    {"name": "Dr. K Rao", "specialty": "ENT", "phone":"9876543216","address":"Pune","image":"https://media.istockphoto.com/id/177373093/photo/indian-male-doctor.jpg?s=612x612&w=0&k=20&c=5FkfKdCYERkAg65cQtdqeO_D0JMv6vrEdPw3mX1Lkfg="},
    {"name": "Dr. M Das", "specialty": "Gynecology", "phone":"9876543217","address":"Jaipur","image":"https://as1.ftcdn.net/v2/jpg/00/47/00/44/1000_F_47004476_SYtxJxdbrzsVkTGMB0RGhomIKlnzLsSe.jpg"}
]

# Convert to DataFrame in session_state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(doctor_data)
    st.session_state.df['Validation Status'] = np.random.choice(["Verified","Needs Review","Error"], len(doctor_data), p=[0.6,0.3,0.1])

# Audit logs
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- HOME PAGE ---
if page == "Home":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>AgentX Health</h1>", unsafe_allow_html=True)
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

    for i in range(0, len(df_filtered), 4):
        cols = st.columns(4)
        for j, idx in enumerate(range(i, min(i+4, len(df_filtered)))):
            with cols[j]:
                doc = df_filtered.iloc[idx]
                # Load image from URL
                try:
                    response = requests.get(doc['image'])
                    img = Image.open(BytesIO(response.content))
                    st.image(img, width=100)
                except:
                    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910762.png", width=100)
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
        # Balloons only if Verified
        if status == "Verified":
            st.balloons()
        # Add to df & logs
        new_doc = {
            "name": name,
            "specialty": specialty,
            "phone": phone,
            "address": address,
            "image": "https://cdn-icons-png.flaticon.com/512/2910/2910762.png",
            "Validation Status": status
        }
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
