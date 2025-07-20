import cv2
import pyttsx3
import time

# ----------- Text-to-Speech Setup ------------
engine = pyttsx3.init()
engine.setProperty('rate', 145)
engine.setProperty('volume', 1.0)

# Choose voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

# ----------- Welcome Speech Lines ------------
speech_lines = [
    "Good day everyone, and a warm welcome to Mar Elias College!",
    "We're really excited to have you with us today.",
    "Here, we don't just teach — we inspire innovation and creativity.",
    "Feel free to explore, learn, and grow with us.",
    "This demo uses real-time face detection powered by OpenCV.",
    "Let's begin the experience. Smile for the camera!"
]

# ----------- Load Haar Cascade for Face Detection ------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ----------- Start Webcam ------------
cap = cv2.VideoCapture(0)

# Delay before speech starts (camera warm-up)
time.sleep(2)

current_line = 0
last_line_time = time.time()

# Speak first line
engine.say(speech_lines[current_line])
engine.runAndWait()
current_line += 1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Show static labels
    cv2.putText(frame, "Mar Elias College", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.putText(frame, "Face Detection Active", (10, 65), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 255), 2)

    # Show current speech line on screen
    if current_line <= len(speech_lines):
        cv2.putText(frame, speech_lines[current_line - 1], (10, 430), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        # Move to next line every ~3 seconds
        if time.time() - last_line_time > 3:
            if current_line < len(speech_lines):
                engine.say(speech_lines[current_line])
                engine.runAndWait()
                last_line_time = time.time()
                current_line += 1

    # Display the frame
    cv2.imshow('Face Detection - Mar Elias College', frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------- Clean Up ------------
cap.release()
cv2.destroyAllWindows()
