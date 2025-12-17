import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
from io import BytesIO
import requests

# --- Page configuration ---
st.set_page_config(page_title="AgentX Health – EY Techathon", layout="wide")

# --- Session state ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- Sample Doctor Data ---
doctor_data = [
    {"name": f"Dr. {i} Name",
     "specialty": np.random.choice([
         "Cardiology","Dermatology","Neurology","Orthopedics","Pediatrics",
         "Oncology","ENT","Gynecology","Urology","Psychiatry"]),
     "phone": f"98765432{i:02}",
     "address": f"City {i}",
     "image": "https://cdn-icons-png.flaticon.com/512/387/387561.png"}
    for i in range(1, 11)
]

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(doctor_data)
    st.session_state.df['Validation Status'] = np.random.choice(
        ["Verified", "Needs Review", "Error"], len(doctor_data),
        p=[0.6, 0.3, 0.1]
    )

# --- GLOBAL CSS ---
st.markdown("""
<style>
@keyframes snakeMove {
    0% { transform: translateX(0); }
    25% { transform: translateX(-6px); }
    50% { transform: translateX(6px); }
    75% { transform: translateX(-4px); }
    100% { transform: translateX(0); }
}
.snake { animation: snakeMove 0.6s ease-in-out; }

.app-title {
    font-size: 70px;
    font-weight: 800;
    text-align: center;
    color: #1F4FD8;
    cursor: pointer;
}

.subtitle {
    display:none;
    text-align:center;
    font-size:26px;
    margin-top:10px;
}

.card {
    padding:25px;
    border-radius:18px;
    text-align:center;
    font-size:18px;
    box-shadow:0 6px 18px rgba(0,0,0,0.12);
    transition: transform 0.3s ease;
    cursor:pointer;
}
.card:hover { transform: translateY(-8px); }

.doctor-img {
    transition: transform 0.3s ease;
}
.doctor-img:hover {
    transform: scale(1.08) rotate(1deg);
}

.stButton>button {
    background-color:#1F4FD8;
    color:white;
    font-size:22px;
    padding:12px 40px;
    border-radius:30px;
    border:none;
    transition: transform 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-5px);
}
</style>

<script>
function showSubtitle(el) {
    el.classList.add('snake');
    document.getElementById("subtitle").style.display = "block";
}
</script>
""", unsafe_allow_html=True)

# ================= HOME PAGE =================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="app-title" onclick="showSubtitle(this)">
    Agent<span style="font-size:90px;">X</span> Health
    </div>
    <div id="subtitle" class="subtitle">
    Automated Healthcare Provider Data Validation using Agentic AI
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center;margin-top:15px;'>"
        "<img src='https://cdn-icons-png.flaticon.com/512/387/387561.png' "
        "width='160' class='doctor-img'/></div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card" style="background:#D4EFDF;">
    🛡️<br>
    <b>Accurate Doctor Data Validation</b><br><br>
    ✔ AI-powered credential verification<br>
    ✔ Cross-platform data consistency<br>
    ✔ Compliance-ready provider records<br><br>
    Verify healthcare provider credentials with AI-powered precision,
    ensuring accuracy and regulatory compliance.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card" style="background:#FEF9E7;">
    ⚙️<br>
    <b>Intelligent Automation</b><br><br>
    ✔ Agentic AI workflows<br>
    ✔ Reduced manual effort<br>
    ✔ Faster validation cycles<br><br>
    Automate complex validation processes to deliver faster updates
    with fewer human errors.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card" style="background:#FADBD8;">
    ❤️<br>
    <b>Improved Patient Trust</b><br><br>
    ✔ Verified provider profiles<br>
    ✔ Accurate contact details<br>
    ✔ Reliable healthcare access<br><br>
    Build confidence and trust with verified, up-to-date provider
    information patients can rely on.
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Get Started"):
        st.session_state.page = "Provider Dashboard"

# ================= PROVIDER DASHBOARD =================
elif st.session_state.page == "Provider Dashboard":

    st.markdown("""
    <h1 onclick="this.classList.add('snake')"
    style="text-align:center;
    font-size:48px;
    color:#2E86C1;
    cursor:pointer;
    text-shadow:0 0 12px rgba(46,134,193,0.8);">
    Provider Directory Dashboard
    </h1>
    """, unsafe_allow_html=True)

    specialties = st.session_state.df['specialty'].unique().tolist()
    statuses = ["Verified","Needs Review","Error"]

    col1, col2 = st.columns(2)
    with col1:
        specialty_filter = st.multiselect("Select Specialty", specialties)
    with col2:
        status_filter = st.multiselect("Select Status", statuses)

    df = st.session_state.df.copy()
    if specialty_filter:
        df = df[df['specialty'].isin(specialty_filter)]
    if status_filter:
        df = df[df['Validation Status'].isin(status_filter)]

    for i in range(0, len(df), 4):
        cols = st.columns(4)
        for j, idx in enumerate(range(i, min(i+4, len(df)))):
            with cols[j]:
                doc = df.iloc[idx]
                st.markdown(
                    f"<img src='{doc['image']}' width='100' class='doctor-img'/>",
                    unsafe_allow_html=True
                )
                st.markdown(f"**{doc['name']}**")
                st.markdown(doc['specialty'])
                st.markdown(doc['phone'])
                st.markdown(doc['address'])

                color = "#28A745" if doc['Validation Status']=="Verified" else \
                        "#FFC107" if doc['Validation Status']=="Needs Review" else "#DC3545"

                st.markdown(f"""
                <div style="
                background:{color};
                padding:6px;
                text-align:center;
                border-radius:8px;
                font-weight:bold;
                transition: transform 0.3s ease;"
                onmouseover="this.style.transform='translateX(5px)'"
                onmouseout="this.style.transform='translateX(0)'">
                {doc['Validation Status']}
                </div>
                """, unsafe_allow_html=True)
