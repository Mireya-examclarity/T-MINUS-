from flask import Flask, render_template, jsonify, request
from datetime import datetime, timezone, timedelta
import random

app = Flask(__name__)

# side quests - i added some funny ones

SIDE_QUESTS = [
    "Hydrate, astronaut(Water break). Your brain needs fuel.",
    "Get out of your chair and stretch for 60 seconds.",
    "Oh is that some dust in your workspace?. Come on astronaut, let's clear it.",
    "Take three slow breaths.",
    "Close three tabs you don't actually need.",
    "Want to take a 30 minute nap?.",
    "Give your eyes a 60-second break from the screen.",
    "Put your phone out of reach for 15 minutes(no cheating!).",
    "Complete one tiny task you've been avoiding(Did you wash your clothes that you tossed around?).",
    "Astronaut...take a shower (Take care of yourself)",
    "Find one thing you can prepare for tomorrow.Any work which became a victim of procrastination?",
    "Stand up, go outside(Can you feel the air?) and return with fresh energy.",]


# anomalies

ANOMALIES = [
    {"code": "ANOMALY-001", "title": " LOW FOCUS DETECTED", "message": "Your attention is drifting. Focus on one small objective."},
    {"code": "ANOMALY-002", "title": "UNKNOWN DISTRACTION", "message": "Remove one distraction pulling you off course."},
    {"code": "ANOMALY-003", "title": "MISSION  DELAY", "message": "Break the next objective into a smaller step."},
    {"code": "ANOMALY-004", "title": "LOW ENERGY SIGNAL", "message": "Drink water or take a short break."},
    {"code": "ANOMALY-005", "title": "UNEXPECTED TASK", "message": "Decide whether the surprise objective needs attention now.(IS PROJECTS IMPORTANT?)"},
    {"code": "ANOMALY-006", "title": "NAVIGATION  ERROR", "message": "Choose your next single step."},
    {"code": "ANOMALY-007", "title": "SYSTEMS  OVERLOADED", "message": "Pause. You don't have to solve everything at once."},
    {"code": "ANOMALY-008", "title": " UNPLANNED COMMUNICATION", "message": "Notifications can wait(Your exam will not bro 🥹 ). Return to your objective."},]


# launch time default is 1 hour from now

LAUNCH_TIME = datetime.now(timezone.utc) + timedelta(hours=1)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")

def status():
    return jsonify({ 
        "status": "online",
        "mission_control": "T-MINUS",
        "server_time": datetime.now(timezone.utc).isoformat()})
    

@app.route("/api/countdown", methods=["GET", "POST"])
def countdown():
    global LAUNCH_TIME

    if request.method == "POST":
        data = request.get_json()
        if not data:
            data = {}
        
        launch_value = data.get("launch_time")

        if not launch_value:
            return jsonify({"error": "Provide launch_time as an ISO date-time string."}), 400

        try:
            # fixing Z issue i found on stackoverflow
            raw = launch_value.strip().replace("Z", "+00:00")
            target = datetime.fromisoformat(raw)

            if target.tzinfo is None:
                target = target.replace(tzinfo=timezone.utc)

        except:
            return jsonify({"error": "Invalid launch  date or time."}), 400

        if target <= datetime.now(timezone.utc):
            return jsonify({"error": "Launch time must be in the  future."}), 400

        LAUNCH_TIME = target

    now = datetime.now(timezone.utc)
    remaining = int((LAUNCH_TIME - now).total_seconds())
    if remaining < 0:
        remaining = 0

    return jsonify({
     "days": remaining // 86400,
    "hours": (remaining % 86400) // 3600,
    "minutes": (remaining % 3600) // 60,
    "seconds": remaining % 60,
    "launched": remaining == 0,
    "launch_time": LAUNCH_TIME.isoformat() })
   

@app.route("/api/side-quest")
def side_quest():
    quest = random.choice(SIDE_QUESTS)
    return jsonify({"quest": quest})

@app.route("/api/anomaly")
def anomaly():
    picked = random.choice(ANOMALIES)
    return jsonify(picked)

@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "API endpoint not found"}), 404
    return "Page not found", 404

if __name__ == "__main__":
    app.run(debug=True) 
    
