import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import cv2
import mediapipe as mp
from keras.models import load_model
import numpy as np
import pandas as pd

model = load_model('smnist.h5')

mphands = mp.solutions.hands
hands = mphands.Hands()
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Attempt to capture a frame to initialize dimensions
ret, frame = cap.read()
if not ret:
    print("Failed to capture an initial frame. Exiting...")
    cap.release()
    exit()

h, w, c = frame.shape

letterpred = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

def preprocess_frame(frame, hand_landmarks):
    x_max = 0
    y_max = 0
    x_min = w
    y_min = h
    for lm in hand_landmarks.landmark:
        x, y = int(lm.x * w), int(lm.y * h)
        if x > x_max:
            x_max = x
        if x < x_min:
            x_min = x
        if y > y_max:
            y_max = y
        if y < y_min:
            y_min = y
    y_min = max(0, y_min - 20)
    y_max = min(h, y_max + 20)
    x_min = max(0, x_min - 20)
    x_max = min(w, x_max + 20)
    
    analysis_frame = cv2.cvtColor(frame[y_min:y_max, x_min:x_max], cv2.COLOR_BGR2GRAY)
    analysis_frame = cv2.resize(analysis_frame, (28, 28))
    
    nlist = analysis_frame.flatten().tolist()
    datan = pd.DataFrame(nlist).T
    
    colname = [i for i in range(784)]
    datan.columns = colname
    
    pixeldata = datan.values / 255
    pixeldata = pixeldata.reshape(-1, 28, 28, 1)
    
    return pixeldata

def display_prediction(frame, letter, confidence):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"{letter} ({confidence:.2f}%)"
    cv2.putText(frame, text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        continue

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    hand_landmarks = result.multi_hand_landmarks

    if hand_landmarks:
        for handLMs in hand_landmarks:
            mp_drawing.draw_landmarks(frame, handLMs, mphands.HAND_CONNECTIONS)
            
            pixeldata = preprocess_frame(frame, handLMs)
            prediction = model.predict(pixeldata)
            predarray = np.array(prediction[0])
            letter_prediction_dict = {letterpred[i]: predarray[i] for i in range(len(letterpred))}
            
            predarrayordered = sorted(predarray, reverse=True)
            high1 = predarrayordered[0]
            
            for key, value in letter_prediction_dict.items():
                if value == high1:
                    predicted_letter = key
                    predicted_confidence = 100 * value
                    display_prediction(frame, predicted_letter, predicted_confidence)
                    print(f"Predicted Character: {predicted_letter}")
                    print(f"Confidence: {predicted_confidence:.2f}%")
                    break

    cv2.imshow("ASL Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
