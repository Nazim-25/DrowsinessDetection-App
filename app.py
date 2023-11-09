
from flask import Flask, render_template, Response
import cv2
import numpy as np
import dlib
from imutils import face_utils
import time
from pygame import mixer

# Initializing the Flask application
app = Flask(__name__)

# Initializing the audio playback (mixer) module of Pygame
mixer.init()

# Loading audio files
NoDriverSound = mixer.Sound('NoDriverSound.mp3')
SleepSound = mixer.Sound('SleepSound.mp3')
TiredSound = mixer.Sound('TiredSound.mp3')

# Initializing the Dlib face detector
detector = dlib.get_frontal_face_detector()

# Loading the Dlib face landmark predictor model
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# Function to compute the distance between two points
def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

# Function to detect eye blinking
def blinked(a, b, c, d, e, f):

    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)
    # Check if the eyes are closed or open based on EAR
    if ratio > 0.22:
        return 'open'
    else:
        return 'closed'


# Function to calculate the mouth aspect ratio
def MouthAspectRatio(mouth):
    # Calculate distances between mouth landmark points
    A = compute(mouth[2], mouth[10])  # 51, 59
    B = compute(mouth[4], mouth[8])  # 53, 57
    C = compute(mouth[0], mouth[6])  # 49, 55
    # Calculate the mouth aspect ratio
    mar = (A + B) / (2.0 * C)
    return mar

# Definition of start and end indices for mouth landmarks
(LandMarkStart_mouth, LandMarkEnd_mouth) = (49, 68)

# Asynchronous function for fatigue detection
async def tired():
    startTime = time.time()
    ResetTimeStart = startTime
    TiredSound.play()  #
    a = 0

    while time.time() - startTime < 9:
        if time.time() - ResetTimeStart > 3:
            TiredSound.play()

    TiredSound.stop()
    return


# Main function for driver fatigue detection
def detech():
    SleepSound_flag = 0
    NoDriverSound_flag = 0
    yawning_frame_co = 0
    awake_frame_co = 0
    no_yawn_frame_co = 0
    sleep_frame_co = 0
    color = (0, 0, 0)
    status = ""
    no_driver_frame_co = 0
    frame_color = (0, 255, 0)
    #url = "http://192.168.1.33:8080/video"
    cap = cv2.VideoCapture(0)

    time.sleep(1)
    start = time.time()
    NoDriver_time = time.time()
    NoDriverSound_start = time.time()

    # Main loop for face, yawning, and eye blinking detection
    while True:
        _, frame = cap.read()  # Read an image from the video capture
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)  # Convert to YUV color space (To increase detection accuracy in the dark)
        channels = cv2.split(frame)  # Split color channels (To increase detection accuracy in the dark)
        cv2.equalizeHist(channels[0], channels[0])  # Equalize the histogram of the Y channel (To increase detection accuracy in the dark)
        frame = cv2.merge(channels)  # Merge color channels (To increase detection accuracy in the dark)
        frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)  # Convert to BGR color space (To increase detection accuracy in the dark)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        face_frame = frame.copy()
        faces = detector(gray, 0)

        if faces:
            NoDriverSound_flag = 0
            NoDriverSound.stop()
            no_driver_frame_co = 0
            NoDriver_time = time.time()

            face = faces[0]  # Select the first detected face
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            cv2.rectangle(frame, (x1, y1), (x2, y2), frame_color, 2)  # Draw a rectangle around the face

            landmarks = predictor(gray, face)  # Detect facial landmarks
            landmarks = face_utils.shape_to_np(landmarks)  # Convert to NumPy array

            left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])
            mouth = landmarks[LandMarkStart_mouth:LandMarkEnd_mouth] # Mouth region
            mouthMAR = MouthAspectRatio(mouth)
            mar = mouthMAR

            if mar > 0.80:
                sleep_frame_co = 0
                awake_frame_co = 0
                yawning_frame_co += 1
                status = "Yawning"
                color = (255, 0, 0)
                frame_color = (255, 0, 0)
                sleep_sound_flag = 0
                SleepSound.stop()
            elif left_blink == 'closed' or right_blink == 'closed':
                if yawning_frame_co > 20:
                    no_yawn_frame_co += 1
                sleep_frame_co += 1
                yawning_frame_co = 0
                awake_frame_co = 0
                if sleep_frame_co > 5:
                    status = "Asleep"
                    color = (0, 0, 255)
                    frame_color = (0, 0, 255)
                    if SleepSound_flag == 0:
                        SleepSound.play()
                    SleepSound_flag = 1
            else:
                if yawning_frame_co > 20:
                    no_yawn_frame_co += 1
                yawning_frame_co = 0
                sleep_frame_co = 0
                awake_frame_co += 1
                status = "Awake"
                color = (0, 255, 0)
                frame_color = (0, 255, 0)
                if awake_frame_co > 5:
                    SleepSound_flag = 0
                    SleepSound.stop()

            cv2.putText(frame, status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)  # Display the status

            if time.time() - start < 60 and no_yawn_frame_co >= 3:
                no_yawn_frame_co = 0
                TiredSound.play()
            elif time.time() - start > 60:
                start = time.time()

            #for n in range(0, 68):
            #   (x, y) = landmarks[n]
            #   cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)  # Draw facial landmarks

        else:
            no_driver_frame_co += 1
            SleepSound_flag = 0
            SleepSound.stop()
            if no_driver_frame_co > 10:
                status = "No Driver"
                color = (0, 0, 0)
            if time.time() - NoDriver_time > 5:
                if NoDriverSound_flag == 0:
                    NoDriverSound.play()
                    NoDriverSound_start = time.time()
                else:
                    if time.time() - NoDriverSound_start > 3:
                        NoDriverSound.play()
                        NoDriverSound_start = time.time()
                NoDriverSound_flag = 1

        cv2.putText(frame, status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)  # Display the status

        ret, buffer = cv2.imencode('.jpg', frame)  # Encode the image in JPEG format
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Return the encoded image





# Route for the video stream
@app.route("/video_feed")
def video_feed():
    print("Opening the camera")
    return Response(detech(), mimetype='multipart/x-mixed-replace;boundary=frame')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detection")
def detection():
    return render_template("detection.html")


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
