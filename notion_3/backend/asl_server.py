from flask import Flask, Response, jsonify, request, send_from_directory
from flask_cors import CORS
from keras.models import load_model
import numpy as np
import cv2
import mediapipe as mp
import os
import json
import base64

app = Flask(__name__)
CORS(app)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load model
model = load_model('smnist.h5')

# Letter predictions mapping
letterpred = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

@app.route('/')
def serve_index():
    return send_from_directory('.', 'asl.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get frame data from request
        frame_data = request.json['frame']
        frame_data = frame_data.split(',')[1]
        
        # Decode base64 image
        frame_bytes = base64.b64decode(frame_data)
        frame_arr = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_arr, cv2.IMREAD_COLOR)
        
        # Process frame with MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract hand region
            h, w, _ = frame.shape
            x_coords = [landmark.x * w for landmark in hand_landmarks.landmark]
            y_coords = [landmark.y * h for landmark in hand_landmarks.landmark]
            
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))
            
            # Add padding
            padding = 20
            x_min = max(0, x_min - padding)
            x_max = min(w, x_max + padding)
            y_min = max(0, y_min - padding)
            y_max = min(h, y_max + padding)
            
            # Process hand region
            hand_region = frame[y_min:y_max, x_min:x_max]
            if hand_region.size > 0:
                hand_region = cv2.resize(hand_region, (28, 28))
                hand_region = cv2.cvtColor(hand_region, cv2.COLOR_BGR2GRAY)
                hand_region = hand_region.reshape(1, 28, 28, 1)
                hand_region = hand_region / 255.0
                
                # Make prediction
                prediction = model.predict(hand_region)
                predicted_index = np.argmax(prediction[0])
                confidence = float(prediction[0][predicted_index])
                
                return jsonify({
                    'letter': letterpred[predicted_index],
                    'confidence': confidence
                })
        
        return jsonify({'letter': None, 'confidence': 0})
    
    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)