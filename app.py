import streamlit as st
from cryptography.fernet import Fernet, InvalidToken
import hashlib, base64, secrets, string, time, json
from datetime import datetime

# ---------- PAGE ----------
st.set_page_config(page_title="🔐 Pro Encryption Tool", layout="centered")

# ---------- 🎨 FULL PROFESSIONAL UI ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0f1c, #1e293b);
    color: #e2e8f0;
}

/* Titles */
h1, h2, h3 {
    color: #f8fafc !important;
}

/* Text */
p, label, span {
    color: #cbd5e1 !important;
}

/* Input */
.stTextInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 8px;
    border: 1px solid #334155;
}

/* FILE UPLOADER FIX (🔥 IMPORTANT) */
section[data-testid="stFileUploader"] {
    background-color: #1e293b !important;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #334155;
}

section[data-testid="stFileUploader"] label {
    color: #e2e8f0 !important;
}

section[data-testid="stFileUploader"] div {
    color: #cbd5e1 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 10px;
    padding: 10px;
    border: 10px;
    font-weight: bold;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
}

/* Cards */
.card {
    background-color:#1e293b;
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
    color:pink;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #3b82f6;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🔐 File Encryption Tool")
st.markdown("### Secure • Fast • Professional 🚀")

# ---------- FUNCTIONS ----------
def generate_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def file_hash(data):
    return hashlib.sha256(data).hexdigest()

def generate_password():
    chars = string.ascii_letters + string.digits + "@#$%"
    return ''.join(secrets.choice(chars) for _ in range(12))

def password_score(password):
    score = 0
    if len(password) >= 8: score += 25
    if any(c.isdigit() for c in password): score += 25
    if any(c.isupper() for c in password): score += 25
    if any(c in "@#$%" for c in password): score += 25
    return score

# ---------- SESSION ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "stats" not in st.session_state:
    st.session_state.stats = {"encrypt":0, "decrypt":0}

# ---------- PASSWORD ----------
show_pass = st.checkbox("👁 Show Password")
password = st.text_input("🔑 Enter Password", type="default" if show_pass else "password")

if st.button("⚡ Generate Strong Password"):
    st.success(generate_password())

if password:
    score = password_score(password)
    st.progress(score)
    st.write(f"Password Strength: {score}/100")

# ---------- FILE UPLOAD ----------
uploaded_files = st.file_uploader("📂 Upload Files", accept_multiple_files=True)

# ---------- MAIN ----------
if uploaded_files and password:

    key = generate_key(password)
    cipher = Fernet(key)

    for file in uploaded_files:
        data = file.read()

        st.subheader(f"📄 {file.name}")

        if len(data) == 0:
            st.error("⚠ File is empty!")
            continue

        # File info
        st.write("📏 Size:", len(data), "bytes")
        st.write("📂 Type:", file.name.split('.')[-1])
        st.write("🔐 Hash:", file_hash(data))

        col1, col2 = st.columns(2)

        # ENCRYPT
        with col1:
            if st.button("🔒 Encrypt", key="enc_"+file.name):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.002)
                    progress.progress(i+1)

                encrypted = cipher.encrypt(data)

                st.success("Encrypted Successfully!")

                st.session_state.stats["encrypt"] += 1
                st.session_state.history.append({
                    "action":"encrypt",
                    "file":file.name,
                    "time":str(datetime.now())
                })

                st.download_button(
                    "⬇ Download Encrypted",
                    encrypted,
                    file_name=file.name + ".enc",
                    key="down_enc_"+file.name
                )

        # DECRYPT
        with col2:
            if st.button("🔓 Decrypt", key="dec_"+file.name):
                try:
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.002)
                        progress.progress(i+1)

                    decrypted = cipher.decrypt(data)

                    st.success("Decrypted Successfully!")

                    st.session_state.stats["decrypt"] += 1
                    st.session_state.history.append({
                        "action":"decrypt",
                        "file":file.name,
                        "time":str(datetime.now())
                    })

                    st.download_button(
                        "⬇ Download Decrypted",
                        decrypted,
                        file_name="decrypted_"+file.name,
                        key="down_dec_"+file.name
                    )

                except InvalidToken:
                    st.error("❌ Wrong Password or Invalid File!")

# ---------- DASHBOARD ----------
st.markdown("## 📊 Analytics Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
    🔒 <h2>{st.session_state.stats['encrypt']}</h2>
    Encrypted Files
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
    🔓 <h2>{st.session_state.stats['decrypt']}</h2>
    Decrypted Files
    </div>
    """, unsafe_allow_html=True)

# ---------- HISTORY ----------
st.markdown("## 📜 Activity History")

if st.session_state.history:
    for item in st.session_state.history[::-1]:
        st.markdown(f"""
        <div class="card">
        🔹 <b>{item['action'].upper()}</b> | 📄 {item['file']} <br>
        🕒 {item['time']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No activity yet")

# ---------- CLEAR HISTORY ----------
if st.button("🗑 Clear History"):
    st.session_state.history = []
    st.success("History Cleared!")

# ---------- REPORT ----------
report = json.dumps(st.session_state.history, indent=2)
st.download_button("📥 Download Report", report, file_name="report.json")