# 🦏 Intelligent Poaching Detection and Response System

An AI-powered system designed to detect poaching activities using computer vision and automatically alert authorities through email notifications. The project leverages deep learning, real-time object detection, and a modern web interface to assist wildlife conservation efforts.

---

## 📌 Project Overview

Wildlife poaching is a major threat to biodiversity across the globe. This project aims to provide a **technology-driven solution** by detecting suspicious activities such as the presence of poachers, weapons, or animals using images and videos. Upon detection, the system sends automated alerts with visual evidence to administrators.

---

## 🎯 Objectives

- Detect poachers, weapons, and animals using deep learning.
- Provide real-time image/video analysis.
- Send automated email alerts with detected images.
- Maintain detection history for monitoring and reporting.
- Offer a secure, user-friendly admin interface.

---

## 🛠️ Technologies Used

- **Python**
- **YOLO (You Only Look Once)** – Object Detection
- **OpenCV** – Image & Video Processing
- **Streamlit** – Web Application UI
- **SMTP (Gmail)** – Email Alerts
- **JSON** – Admin & History Storage

---

## ⚙️ System Architecture

1. **Input Source**  
   - Images / Videos uploaded by the admin.

2. **Detection Engine**  
   - YOLO model detects objects such as *poacher*, *weapon*, and *animal*.

3. **Web Interface**  
   - Streamlit-based UI for uploads, results, and history.

4. **Alert System**  
   - Email notifications sent with detected images attached.

5. **Data Logging**  
   - Detection details stored in history logs for future reference.

---

## 🔐 Admin Features

- Secure login and registration for multiple admins.
- Upload images or videos for detection.
- View annotated detection results.
- Receive email alerts on threat detection.
- Access detection history in tabular format.
- Logout functionality for session security.

