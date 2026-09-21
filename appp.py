from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

SIDE_QUESTS = [
    "Drink some water. Mission systems need fuel.",
    "Stand up and stretch for 60 seconds.",
    "Clean one small area of your workspace.",
    "Take three deep breaths before your next objective.",
    "Close unnecessary browser tabs.",
    "Write down your next objective.",
    "Take a 5-minute systems check break.",
    "Put your phone away for the next 15 minutes.",
    "Complete one tiny task you've been avoiding.",
    "Rest your eyes for 60 seconds.",
]

ANOMALIES = [
    "⚠️ LOW FOCUS DETECTED",
    "⚠️ UNKNOWN DISTRACTION DETECTED",
    "⚠️ MISSION DELAY DETECTED",
    "⚠️ ENERGY LEVELS FLUCTUATING",
    "⚠️ UNEXPECTED TASK DETECTED",
    "⚠️ NAVIGATION ERROR",
    "⚠️ PRODUCTIVITY LEVELS DROPPING",
    "⚠️ COMMUNICATION INTERRUPTION",
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/side-quest')
def side_quest():
    return jsonify({"quest": random.choice(SIDE_QUESTS)})

@app.route('/api/anomaly')
def anomaly():
    return jsonify({"anomaly": random.choice(ANOMALIES)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)