import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response, jsonify, request

app = Flask(__name__)

# Initialize MediaPipe Pose and Selfie Segmentation
mp_pose = mp.solutions.pose
mp_selfie_segmentation = mp.solutions.selfie_segmentation
pose = mp_pose.Pose()
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Initialize variables
curl_count = 0
stage = None
calories_burned = 0
target_count = 0
is_target_set = False

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

# Initialize video capture
cap = cv2.VideoCapture(0)

def generate_frames():
    global curl_count, stage, calories_burned, target_count, is_target_set
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Convert to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the image for pose detection
            pose_results = pose.process(image)
            
            # Process the image for segmentation
            seg_results = segmentation.process(image)
            
            # Create a mask for segmentation
            mask = (seg_results.segmentation_mask > 0.1).astype(np.uint8) * 255
            
            if pose_results.pose_landmarks:
                landmarks = pose_results.pose_landmarks.landmark
                
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
            
            # Apply the segmentation mask
            segmented_image = cv2.bitwise_and(frame, frame, mask=mask)
            
            # Display curl count, calories burned, and target status
            cv2.putText(segmented_image, f'Curls: {curl_count}', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(segmented_image, f'Calories: {calories_burned:.1f}', (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if is_target_set:
                status = "Target reached!" if curl_count >= target_count else f"Target: {curl_count}/{target_count}"
                cv2.putText(segmented_image, status, (10, 110), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', segmented_image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset', methods=['POST'])
def reset():
    global curl_count, calories_burned, is_target_set
    curl_count = 0
    calories_burned = 0
    is_target_set = False
    return jsonify({"status": "reset successful"})

@app.route('/set_target', methods=['POST'])
def set_target():
    global target_count, is_target_set
    target_count = int(request.form['target'])
    is_target_set = True
    return jsonify({"status": "target set successfully"})

if __name__ == '__main__':
    app.run(debug=True)
