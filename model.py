import cv2
import imutils
import threading
from playsound import playsound
import smtplib
from email.message import EmailMessage
import os
import time
from datetime import datetime

# Initialize Video Capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Set up initial frame for motion detection
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0
last_snapshot_time = time.time()  # Initialize the last snapshot time

def send_email(face_paths):
    """
    Sends an alert email with face images attached when multiple faces are detected.

    Parameters:
    face_paths (list of str): A list of file paths to face image snapshots.
    """
    try:
        lateness_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time of motion detection
        
        msg = EmailMessage()
        msg['Subject'] = "Alert: Multiple People Detected!"
        msg['From'] = 'sender_email'  # Change to your email
        msg['To'] = 'receiver_email'  # Change to recipient's email

        # Email content with lateness time
        msg.set_content(f"Motion detected at {lateness_time}! See the attached images.")
        
        # Attach each face image
        for face_path in face_paths:
            with open(face_path, 'rb') as img:
                msg.add_attachment(img.read(), maintype='image', subtype='jpeg', filename=os.path.basename(face_path))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('sender_email', 'app_password_sender_email')  # Your email credentials
            server.send_message(msg)

        # Delete images after sending
        for face_path in face_paths:
            os.remove(face_path)

    except Exception as e:
        print(f"Error sending email: {e}")

def beep_alarm():
    """
    Plays an alarm sound for 3 seconds to alert of a detected face in motion. 
    The alarm stops if the alarm_mode is deactivated during the sound.
    """
    global alarm
    end_time = time.time() + 3  # Beep for 3 seconds
    while time.time() < end_time:
        if not alarm_mode:
            break
        print("ALARM")
        playsound("audiomass-output.mp3")  # Beep sound

    alarm = False

while True:
    """
    Main loop for video feed and motion detection. Reads frames from the camera, 
    detects motion and faces when alarm mode is active, and triggers an email alert 
    with images if faces are detected in a frame showing motion.

    Controls:
    - Press 't' to toggle alarm mode (on/off).
    - Press 'q' to quit the program.
    """
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        # Convert frame to grayscale and apply Gaussian blur
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (21, 21), 0)

        # Calculate difference from the starting frame
        diff = cv2.absdiff(start_frame, frame_bw)
        threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw  # Update starting frame

        # Check for significant changes indicating motion
        if threshold.sum() > 300:
            alarm_counter += 1
            
            # Detect faces in the current frame
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            if len(faces) > 0:
                current_time = time.time()
                # Take snapshots every 5 seconds
                if current_time - last_snapshot_time >= 5:
                    last_snapshot_time = current_time  # Update snapshot time
                    face_paths = []
                    
                    # Isolate each detected face, save it, and append the file path to the list
                    for i, (x, y, w, h) in enumerate(faces):
                        face_img = frame[y:y+h, x:x+w]
                        snapshot_path = f"snapshot_{i}_{int(time.time())}.jpg"
                        cv2.imwrite(snapshot_path, face_img)
                        face_paths.append(snapshot_path)
                    
                    # Send email with snapshots in a separate thread
                    threading.Thread(target=send_email, args=(face_paths,)).start()
            
        else:
            alarm_counter = max(0, alarm_counter - 1)  # Reset counter if no motion detected

        cv2.imshow("Threshold", threshold)  # Display threshold image for motion detection
    else:
        cv2.imshow("Frame", frame)  # Display the main camera feed if alarm mode is off

    # Activate alarm if motion is sustained
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    # Key bindings to toggle alarm mode and quit
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode 
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
