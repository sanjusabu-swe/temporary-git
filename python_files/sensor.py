import cv2
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Set up webcam
cap = cv2.VideoCapture(0)

# Create a black canvas to draw on
canvas = None

# Function to count raised fingers
def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

# Initialize Mediapipe Hands
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:

    prev_x, prev_y = 0, 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror image
        h, w, _ = frame.shape

        if canvas is None:
            canvas = np.zeros_like(frame)

        # Convert color for MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm = hand_landmarks.landmark

                # Get index finger tip coordinates
                x = int(lm[8].x * w)
                y = int(lm[8].y * h)

                # Count raised fingers
                raised = count_fingers(hand_landmarks)

                # If only index finger is up, draw
                if raised == 1:
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = x, y

                    # Draw line on canvas
                    cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 255), 5)
                    prev_x, prev_y = x, y

                # If more than 1 finger is up, reset previous position (lift pen)
                else:
                    prev_x, prev_y = 0, 0

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Combine canvas with webcam feed
        blended = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

        cv2.imshow("Hand Gesture Drawing", blended)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

cap.release()
cv2.destroyAllWindows()
