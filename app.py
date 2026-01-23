import streamlit as st
import cv2
import os
import json
import smtplib
import torch
from ultralytics import YOLO
from email.message import EmailMessage
from PIL import Image
from datetime import datetime

# ================= SAFE TORCH LOAD FIX =================
from ultralytics.nn.tasks import DetectionModel
torch.serialization.add_safe_globals([DetectionModel])

# ================= CONSTANTS =================
ANIMAL_CLASSES = [
    "dog", "cat", "cow", "horse", "sheep", "deer",
    "elephant", "bear", "zebra", "giraffe"
]
WEAPON_CLASSES = ["knife", "gun"]

MODEL_PATH = "yolov8n.pt"
UPLOAD_DIR = "uploads"
ALERT_DIR = "alerts"
USER_DB = "users.json"

EMAIL_USER = "chaluvashetty23@gmail.com"
EMAIL_PASS = "ytqwpuwzyxfwcism"   # Gmail app password
ALERT_EMAIL = "chaluvarajn231@gmail.com"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ALERT_DIR, exist_ok=True)

if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

# ================= LOAD MODEL =================
model = YOLO(MODEL_PATH)

# ================= UI STYLE =================
st.markdown("""
<style>
body { background-color: #0f172a; color: white; }
.block { background:#1e293b; padding:20px; border-radius:15px; }
</style>
""", unsafe_allow_html=True)

# ================= LOGIN / SIGNUP =================
def login_page():
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        users = json.load(open(USER_DB))
        if u in users and users[u] == p:
            st.session_state.logged = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

def signup_page():
    st.title("📝 Sign Up")
    u = st.text_input("New Username")
    p = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        users = json.load(open(USER_DB))
        users[u] = p
        json.dump(users, open(USER_DB, "w"))
        st.success("Account created")

if "logged" not in st.session_state:
    choice = st.radio("Choose", ["Login", "Sign Up"])
    if choice == "Login":
        login_page()
    else:
        signup_page()
    st.stop()

# ================= EMAIL ALERT =================
def send_alert(img_path, counts):
    msg = EmailMessage()
    msg["Subject"] = "🚨 POACHING ALERT"
    msg["From"] = EMAIL_USER
    msg["To"] = ALERT_EMAIL

    msg.set_content(f"""
Poaching Detected!

Animals: {counts['animal']}
Poachers: {counts['poacher']}
Weapons: {counts['weapon']}
Time: {datetime.now()}
""")

    with open(img_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="jpeg", filename="alert.jpg")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL_USER, EMAIL_PASS)
        s.send_message(msg)

# ================= NAVIGATION =================
page = st.sidebar.radio("Menu", ["Dashboard", "Image Detection", "Video Detection"])

# ================= DASHBOARD =================
if page == "Dashboard":
    st.title("🛡 Intelligent Poaching Detection System")
    c1, c2, c3 = st.columns(3)
    c1.metric("🐾 Animals", "Monitoring")
    c2.metric("🚶 Poachers", "Monitoring")
    c3.metric("🔫 Weapons", "Monitoring")
    st.success("System Online")

# ================= IMAGE DETECTION =================
elif page == "Image Detection":
    st.title("🖼 Image Detection")
    file = st.file_uploader("Upload Image", ["jpg", "png", "jpeg"])

    if file:
        image = Image.open(file)
        res = model(image, conf=0.25)
        annotated = res[0].plot()

        counts = {"animal": 0, "poacher": 0, "weapon": 0}

        if res[0].boxes is not None:
            for cls in res[0].boxes.cls:
                name = model.names[int(cls)]
                if name == "person":
                    counts["poacher"] += 1
                elif name in ANIMAL_CLASSES:
                    counts["animal"] += 1
                elif name in WEAPON_CLASSES:
                    counts["weapon"] += 1

        save_path = f"{ALERT_DIR}/alert.jpg"
        cv2.imwrite(save_path, annotated)

        st.image(annotated, caption="Detection Result")
        st.json(counts)

        if counts["poacher"] > 0:
            send_alert(save_path, counts)
            st.error("🚨 Alert Email Sent")

# ================= VIDEO DETECTION =================
elif page == "Video Detection":
    st.title("🎥 Video Detection")
    video = st.file_uploader("Upload Video", ["mp4", "avi", "mov"])

    if video:
        path = os.path.join(UPLOAD_DIR, video.name)
        with open(path, "wb") as f:
            f.write(video.read())

        cap = cv2.VideoCapture(path)
        frame_box = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            res = model(frame, conf=0.25)
            frame_box.image(res[0].plot(), channels="BGR")

        cap.release()
        st.success("Video Processing Done")