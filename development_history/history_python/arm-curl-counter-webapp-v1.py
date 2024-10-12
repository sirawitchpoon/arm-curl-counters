import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response
from opencv_webcam_flask_streamer import WebcamStreamer

app = Flask(__name__)
streamer = WebcamStreamer()

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize variables
curl_count = 0
stage = None
calories_burned = 0

# Function to calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle

def process_frame(frame):
    global curl_count, stage, calories_burned
    
    # Convert to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image
    results = pose.process(image)
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        # Get coordinates
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        
        # Calculate angle
        angle = calculate_angle(shoulder, elbow, wrist)
        
        # Curl counter logic
        if angle > 160:
            stage = "down"
        if angle < 30 and stage == 'down':
            stage = "up"
            curl_count += 1
            calories_burned += 0.1  # Assuming 0.1 calorie burned per curl
    
    # Display curl count and calories burned
    cv2.putText(frame, f'Curls: {curl_count}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'Calories: {calories_burned:.1f}', (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return frame

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(streamer.stream(process_frame),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
