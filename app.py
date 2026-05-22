import streamlit as st

st.set_page_config(
    page_title="Cyber Fraud Detection System",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #00ff9d;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
}
.card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #00ff9d;
    box-shadow: 0 0 15px rgba(0,255,157,0.2);
}
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #00ff9d;
    background-color: #0f172a;
    color: white;
    font-weight: bold;
    padding: 10px;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #00ff9d;
    color: black;
    border: 1px solid #00ff9d;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.markdown('<div class="main-title">🛡️ Cyber Fraud Detection Monitoring System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered fraud detection, monitoring, analytics and threat intelligence platform</div>', unsafe_allow_html=True)

st.write("")

if not st.session_state.logged_in:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Access granted.")
            st.rerun()
        else:
            st.error("Access denied. Invalid credentials.")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.sidebar.success("Logged in as Admin")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("""
    <div class="card">
        <h2>🏠 Security Operations Overview</h2>
        <p>
        This AI-powered cyber fraud detection monitoring system identifies suspicious 
        financial transactions using Machine Learning and provides fraud analytics, 
        prediction history, CSV analysis, risk scoring, and security insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔍 Fraud Prediction</h3>
            <p>Analyze single or bulk transactions using ML.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Fraud Prediction", key="prediction"):
            st.switch_page("pages/prediction.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📊 Threat Dashboard</h3>
            <p>View fraud trends, risk scores and transaction analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Dashboard", key="dashboard"):
            st.switch_page("pages/dashboard.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <h3>🕘 Audit History</h3>
            <p>Track stored prediction logs and download reports.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open History", key="history"):
            st.switch_page("pages/history.py")
        st.markdown("</div>", unsafe_allow_html=True)
    st.info("Use the left sidebar to open Prediction, Dashboard, and History pages.")