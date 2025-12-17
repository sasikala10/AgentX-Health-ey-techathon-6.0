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
st.markdown("""
<style>
.nav-item {
    font-size: 28px;
    font-weight: 800;
    cursor: pointer;
    text-align: center;
    padding: 12px;
    transition: all 0.3s ease;
}

.nav-item:hover {
    transform: translateX(8px);
    text-shadow: 0 0 12px rgba(0,0,0,0.35);
}

.nav-validate { color:#17A589; }
.nav-analytics { color:#AF7AC5; }
.nav-audit { color:#D35400; }

/* remove button background */
.stButton>button {
    background: none;
    border: none;
    padding: 0;
}
</style>
""", unsafe_allow_html=True)


st.markdown("---")

# --- Sample Doctor Data ---
doctor_data = [
    {
        "name": "Dr. Arun Kumar",
        "specialty": "Cardiology",
        "phone": "9876543201",
        "address": "Chennai",
        "image": "https://img.freepik.com/premium-photo/young-confident-indian-male-doctor_601128-2498.jpg?w=2000"
    },
    {
        "name": "Dr. Sneha Mehta",
        "specialty": "Dermatology",
        "phone": "9876543202",
        "address": "Mumbai",
        "image": "https://img.freepik.com/premium-photo/woman-white-lab-coat-is-posing-photo_1262781-7688.jpg"
    },
    {
        "name": "Dr. Rajesh Iyer",
        "specialty": "Neurology",
        "phone": "9876543203",
        "address": "Bangalore",
        "image": "https://img.freepik.com/premium-photo/photo-smiling-doctor-with-strethoscope-isolated-one-color-background_953680-46518.jpg"
    },
    {
        "name": "Dr. Pooja Sharma",
        "specialty": "Orthopedics",
        "phone": "9876543204",
        "address": "Delhi",
        "image": "https://img.freepik.com/premium-photo/female-doctor_1158146-4.jpg"
    },
    {
        "name": "Dr. Anil Verma",
        "specialty": "Pediatrics",
        "phone": "9876543205",
        "address": "Hyderabad",
        "image": "https://static.vecteezy.com/system/resources/thumbnails/026/375/249/small_2x/ai-generative-portrait-of-confident-male-doctor-in-white-coat-and-stethoscope-standing-with-arms-crossed-and-looking-at-camera-photo.jpg"
    },
    {
        "name": "Dr. Kavya Reddy",
        "specialty": "Gynecology",
        "phone": "9876543206",
        "address": "Vijayawada",
        "image": "https://static.wixstatic.com/media/cadcfa_644de5333f304ab68bd14a6c832bb2f5~mv2.jpg/v1/fill/w_429,h_469,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/Untitled-2.jpg"
    },
    {
        "name": "Dr. Rohit Malhotra",
        "specialty": "Oncology",
        "phone": "9876543207",
        "address": "Gurgaon",
        "image": "https://img.freepik.com/premium-photo/image-young-man-doctor-dress-white-background_911078-16198.jpg"
    },
    {
        "name": "Dr. Neha Patel",
        "specialty": "ENT",
        "phone": "9876543208",
        "address": "Ahmedabad",
        "image": "https://www.herpulse.in/wp-content/uploads/2021/11/Aunty-Resize.png"
    },
    {
        "name": "Dr. Suresh Nair",
        "specialty": "Urology",
        "phone": "9876543209",
        "address": "Kochi",
        "image": "https://img.freepik.com/premium-photo/free-photo-handsome-indian-doctor-man-white-medical-gown-with-stethoscope_1221994-2548.jpg?w=1060"
    },
    {
        "name": "Dr. Priya Banerjee",
        "specialty": "Psychiatry",
        "phone": "9876543210",
        "address": "Kolkata",
        "image": "https://i.pinimg.com/736x/c5/a3/90/c5a3904b38eb241dd03dd30889599dc4.jpg"
    }
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
    🛡️  <br>
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
                    f"<img src='{doc['image']}' width='120' height='120' style='object-fit:cover; border-radius:50%;'/>",
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
    st.markdown("<br>", unsafe_allow_html=True)

   
   
    nav1, nav2, nav3 = st.columns(3)

    with nav1:
        if st.button("🧪 Validation Simulation"):
            st.session_state.page = "Validation Simulation"
        st.markdown("<div class='nav-item nav-validate'>Validation Simulation</div>", unsafe_allow_html=True)

    with nav2:
        if st.button("📊 Analytics"):
            st.session_state.page = "Analytics"
        st.markdown("<div class='nav-item nav-analytics'>Analytics</div>", unsafe_allow_html=True)

    with nav3:
        if st.button("🧾 Audit Logs"):
            st.session_state.page = "Audit Logs"
        st.markdown("<div class='nav-item nav-audit'>Audit Logs</div>", unsafe_allow_html=True)

    st.markdown("---")

elif st.session_state.page == "Validation Simulation":

    st.markdown("""
    <h1 class="snake"
    style="text-align:center;
    font-size:44px;
    color:#17A589;
    text-shadow:0 0 15px rgba(23,165,137,0.8);">
    Validation Simulation
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="background:#E8F8F5;">
    🤖 <b>Simulate New Provider Validation</b><br><br>
    Enter provider details to see how Agentic AI validates
    credentials, contact data, and consistency in real-time.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- VALIDATION FORM ----------
    with st.form("validation_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Doctor Name")
            specialty = st.selectbox(
                "Specialty",
                st.session_state.df['specialty'].unique()
            )

        with col2:
            phone = st.text_input("Phone Number")
            address = st.text_input("Address")

        submitted = st.form_submit_button("🧪 Run Validation")

    # ---------- VALIDATION LOGIC ----------
    if submitted:
        st.info("🔍 Agentic AI validating provider data...")
        progress = st.progress(0)

        for i in range(5):
            time.sleep(0.4)
            progress.progress((i + 1) * 20)

        # Simulate detailed AI feedback
        issues = []
        if not phone.isdigit() or len(phone) != 10:
            issues.append("Phone number format incorrect")
        if len(address) < 5:
            issues.append("Address seems too short")
        if name.lower() in st.session_state.df['name'].str.lower().tolist():
            issues.append("Duplicate entry detected")

        # Determine status
        if issues:
            status = np.random.choice(["Needs Review", "Error"], p=[0.7, 0.3])
        else:
            status = "Verified"

        # Simulate confidence score
        confidence = np.random.randint(75, 100) if status=="Verified" else np.random.randint(40, 74)

        # Show results
        if status == "Verified":
            st.success(f"✅ {name} validated successfully")
            st.balloons()
        elif status == "Needs Review":
            st.warning(f"⚠ {name} needs manual review")
        else:
            st.error(f"❌ Validation error detected for {name}")

        # Show detailed AI feedback
        if issues:
            st.markdown("<b>AI Detected Issues:</b>", unsafe_allow_html=True)
            for issue in issues:
                st.write(f"- {issue}")

        # Show confidence bar
        st.markdown(f"**Confidence Score:** {confidence}%")
        st.progress(confidence)

        # ---------- ADD TO DASHBOARD ----------
        new_doc = {
            "name": name,
            "specialty": specialty,
            "phone": phone,
            "address": address,
            "image": "https://cdn-icons-png.flaticon.com/512/2910/2910762.png",
            "Validation Status": status
        }
        st.session_state.df = pd.concat(
            [st.session_state.df, pd.DataFrame([new_doc])],
            ignore_index=True
        )

        # ---------- VALIDATION HISTORY ----------
        if 'validation_history' not in st.session_state:
            st.session_state.validation_history = []
        st.session_state.validation_history.append({
            "name": name,
            "specialty": specialty,
            "status": status,
            "issues": issues,
            "confidence": confidence
        })

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("📁 Provider added to Provider Directory Dashboard")

        # Show history
        st.markdown("### 🗂️ Validation History")
        history_df = pd.DataFrame(st.session_state.validation_history)
        st.dataframe(history_df, use_container_width=True)


    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Home"

elif st.session_state.page == "Analytics":

    st.markdown("""
    <h1 class="snake"
    style="text-align:center;
    font-size:44px;
    color:#AF7AC5;
    text-shadow:0 0 15px rgba(175,122,197,0.8);">
    Analytics Dashboard
    </h1>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card" style="background:#F4ECF7;">
        📈 <b>Validation Status Distribution</b>
        </div>
        """, unsafe_allow_html=True)

        status_counts = st.session_state.df['Validation Status'].value_counts()
        st.bar_chart(status_counts)

    with col2:
        st.markdown("""
        <div class="card" style="background:#EBDEF0;">
        🧠 <b>Specialty-wise Provider Count</b>
        </div>
        """, unsafe_allow_html=True)

        specialty_counts = st.session_state.df['specialty'].value_counts()
        st.line_chart(specialty_counts)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Provider Dashboard"
elif st.session_state.page == "Audit Logs":

    st.markdown("""
    <h1 class="snake"
    style="text-align:center;
    font-size:44px;
    color:#D35400;
    text-shadow:0 0 15px rgba(211,84,0,0.8);">
    Audit Logs
    </h1>
    """, unsafe_allow_html=True)

    logs = pd.DataFrame({
        "Timestamp": pd.date_range(end=pd.Timestamp.now(), periods=8),
        "Action": [
            "Doctor profile verified",
            "Phone number updated",
            "Address mismatch detected",
            "License revalidated",
            "Duplicate entry flagged",
            "Manual review requested",
            "Profile approved",
            "Audit export generated"
        ],
        "Status": np.random.choice(["Success", "Warning", "Error"], 8)
    })

    st.dataframe(logs, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Home"



