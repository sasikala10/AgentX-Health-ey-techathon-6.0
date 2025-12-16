import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
from io import BytesIO
import requests

# --- Page configuration ---
st.set_page_config(page_title="AgentX Health – EY Techathon", layout="wide")

# --- Session state for navigation ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- Doctor Data Sample ---
doctor_data = [
    {"name": f"Dr. {i} Name", "specialty": np.random.choice(
        ["Cardiology","Dermatology","Neurology","Orthopedics","Pediatrics","Oncology","ENT","Gynecology","Urology","Psychiatry"]),
     "phone": f"98765432{i:02}", "address": f"City {i}",
     "image":"https://cdn-icons-png.flaticon.com/512/387/387561.png"} for i in range(1,11)
]

# Convert to DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(doctor_data)
    st.session_state.df['Validation Status'] = np.random.choice(
        ["Verified","Needs Review","Error"], len(doctor_data), p=[0.6,0.3,0.1])

# Audit logs
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- HOME PAGE ---
if st.session_state.page=="Home":

    st.markdown("""
    <style>
    .app-title {
        font-size: 70px; font-weight: 800; text-align: center; color: #1F4FD8; cursor: pointer;
    }
    .subtitle { display:none; text-align:center; font-size:26px; margin-top:10px; font-weight:500; }
    .card { padding:25px; border-radius:18px; text-align:center; font-size:18px; font-weight:500; 
            box-shadow:0 6px 18px rgba(0,0,0,0.12); transition: transform 0.3s ease; cursor:pointer; }
    .card:hover { transform: translateY(-8px); }
    .get-started { margin-top:40px; display:flex; justify-content:center; }
    </style>
    <script>
    function showSubtitle() {
        var x = document.getElementById("subtitle");
        if (x.style.display === "none") { x.style.display = "block"; }
    }
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="app-title" onclick="showSubtitle()">Agent<span style="font-size:90px;">X</span> Health</div>
    <div id="subtitle" class="subtitle">Automated Healthcare Provider Data Validation using Agentic AI</div>
    """, unsafe_allow_html=True)

    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=160)

    st.markdown("<br>", unsafe_allow_html=True)

    # Three boxes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card" style="background-color:#D4EFDF;">🛡️<br><br>
        <b>Accurate Doctor Data Validation</b><br><br>
        Verify healthcare provider credentials and information with AI-powered precision, ensuring data accuracy and compliance.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card" style="background-color:#FEF9E7;">⚙️<br><br>
        <b>Intelligent Automation</b><br><br>
        Faster updates and reduced errors through agentic AI workflows that automate complex validation processes effortlessly.
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card" style="background-color:#FADBD8;">❤️<br><br>
        <b>Improved Patient Trust</b><br><br>
        Build confidence and trust with verified, up-to-date provider information that patients can rely on.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    # Get Started
    st.markdown("<div class='get-started'>", unsafe_allow_html=True)
    if st.button("🚀 Get Started"):
        st.session_state.page="Provider Dashboard"
    st.markdown("</div>", unsafe_allow_html=True)

# --- PROVIDER DASHBOARD ---
elif st.session_state.page=="Provider Dashboard":
    st.markdown("<h1 style='text-align:center; color:#2E86C1; font-size:48px;'>Provider Directory Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px; color:#566573;'>Filter and explore provider validation status:</p>", unsafe_allow_html=True)

    # Filters
    specialties = st.session_state.df['specialty'].unique().tolist()
    status_list = ["Verified","Needs Review","Error"]

    col1, col2 = st.columns(2)
    with col1:
        specialty_filter = st.multiselect("Select Specialty", specialties)
    with col2:
        status_filter = st.multiselect("Select Status", status_list)

    # Filter dataframe
    df_filtered = st.session_state.df.copy()
    if specialty_filter:
        df_filtered = df_filtered[df_filtered['specialty'].isin(specialty_filter)]
    if status_filter:
        df_filtered = df_filtered[df_filtered['Validation Status'].isin(status_filter)]

    # Display doctors in grid
    for i in range(0, len(df_filtered), 4):
        cols = st.columns(4)
        for j, idx in enumerate(range(i, min(i+4,len(df_filtered)))):
            with cols[j]:
                doc = df_filtered.iloc[idx]
                try:
                    response = requests.get(doc['image'])
                    img = Image.open(BytesIO(response.content))
                    st.image(img, width=100)
                except:
                    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=100)
                st.markdown(f"**{doc['name']}**")
                st.markdown(f"{doc['specialty']}")
                st.markdown(f"{doc['phone']}")
                st.markdown(f"{doc['address']}")
                # Color-coded status
                status_color = "#28A745" if doc['Validation Status']=="Verified" else "#FFC107" if doc['Validation Status']=="Needs Review" else "#DC3545"
                st.markdown(f"<div style='background-color:{status_color}; padding:5px; text-align:center;'>{doc['Validation Status']}</div>", unsafe_allow_html=True)

# --- VALIDATION SIMULATION ---
elif st.session_state.page=="Validation Simulation":
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
        new_doc = {"name":name,"specialty":specialty,"phone":phone,"address":address,"image":"https://cdn-icons-png.flaticon.com/512/387/387561.png","Validation Status":status}
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_doc])], ignore_index=True)
        st.session_state.logs.append(new_doc)

# --- ANALYTICS ---
elif st.session_state.page=="Analytics":
    st.title("Validation Analytics")
    status_counts = st.session_state.df['Validation Status'].value_counts()
    st.bar_chart(status_counts)
    st.subheader("Doctors by Specialty")
    st.bar_chart(st.session_state.df['specialty'].value_counts())

# --- AUDIT LOGS ---
elif st.session_state.page=="Audit Logs":
    st.title("Audit Logs")
    if st.session_state.logs:
        st.dataframe(pd.DataFrame(st.session_state.logs))
    else:
        st.info("No logs yet. Run some validation simulations!")
