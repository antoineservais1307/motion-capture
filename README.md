
# 📹 Motion Detection and Alert System 🔔

This project is a motion detection and alert system that uses a webcam to detect motion and faces in real-time. When both motion and faces are detected, an alarm sounds, and an email with snapshots of detected faces is sent. Built with OpenCV, it leverages threading for smooth multitasking.

## ✨ Features

- **🎥 Motion Detection**: Detects movement between consecutive frames using frame differencing and thresholding.
- **😊 Face Detection**: Recognizes faces in frames with motion, using a pre-trained Haar Cascade model.
- **📧 Email Alert**: Sends an email with snapshots when faces are detected in motion-triggered frames.
- **🚨 Sound Alarm**: Plays a 3-second alarm sound when motion with faces is detected, using multithreading to avoid blocking.
-**🕒 Snapshot Interval**: Takes face snapshots at least 5 seconds apart to avoid spamming with alerts.
  
## 📦 Requirements

- **🐍 Python 3.x**
- **🎥 Webcam:** Required to capture video feed.
- **🔐 Email Credentials :** Needed to send email alerts (configured in the code).

## 📲 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/antoineservais1307/motion-capture.git
   cd motion-capture
    ``` 
2. Install required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

3. Update email credentials in the `send_email` function:

    - `sender_email`: Replace with the sender's email address.
    - `receiver_email`: Replace with the recipient's email address.
    - `app_password_sender_email`: Replace with your app password (use app-specific passwords for Gmail if 2FA is enabled).

4. Place an audio file named `audiomass-output.mp3` in the project directory for the alarm sound, or update the filename in the `playsound function.`

## 🚀 Usage
1. Run the script:
    ```
    python model.py
    ```
2. Controls:
    - Press ‘t’ to toggle alarm mode on/off 🟢.
    - Press ‘q’ to quit the program ❌.

3. The camera feed will open 🎬, and the program will start detecting motion and faces in real-time.

## 📧 Email Configuration Note
To avoid security issues, use an app-specific password if you’re configuring Gmail or any email service with 2FA enabled. Keep your email credentials secure and do not share them in public repositories.

## 🖥️ How It Works
The code uses frame differencing and thresholding to identify motion. When motion is detected in alarm mode, the system looks for faces within the moving area, taking snapshots and sending them via email when they are detected.

## 📂 Snapshot Management
To avoid clutter, snapshots are automatically deleted after the email is sent. This keeps the system efficient by not overloading storage.

---
Now you can see whoever is coming somewhere 
![](https://media1.tenor.com/m/c8BVgXNBoRsAAAAd/josh-neal-camera.gif)
