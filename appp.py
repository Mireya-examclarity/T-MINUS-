
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timezone, timedelta
import random

app = Flask(__name__)

SIDE_QUESTS = [
    "Hydrate, astronaut. Your brain needs fuel.",
    "Get out of your chair and stretch for 60 seconds.",
    "Clear one tiny patch of your workspace.",
    "Take three slow breaths. Reset your systems.",
    "Close three tabs you don't actually need.",
    "Write down the next thing you need to do.",
    "Give your eyes a 60-second break from the screen.",
    "Put your phone out of reach for 15 minutes.",
    "Complete one tiny task you've been avoiding.",
    "Take a moment to tidy your mission control.",
    "Find one thing you can prepare for tomorrow.",
    "Stand up, move around, and return with fresh energy.",
]

ANOMALIES = [
    {
        "code": f"ANOMALY-{i:03}",
        "title": title,
        "message": message,
    }
    for i, (title, message) in enumerate([
        ("LOW FOCUS DETECTED",
         "Your attention is drifting. Focus on one small objective."),
        ("UNKNOWN DISTRACTION",
         "Remove one distraction pulling you off course."),
        ("MISSION DELAY",
         "Break the next objective into a smaller step."),
        ("LOW ENERGY SIGNAL",
         "Drink water or take a short break."),
        ("UNEXPECTED TASK",
         "Decide whether the surprise objective needs attention now."),
        ("NAVIGATION ERROR",
         "Choose your next single step."),
        ("SYSTEMS OVERLOADED",
         "Pause. You don't have to solve everything at once."),
        ("UNPLANNED COMMUNICATION",
         "Notifications can wait. Return to your objective."),
    ], start=1)
]

# Default launch is one hour after the server starts.
LAUNCH_TIME = datetime.now(timezone.utc) + timedelta(hours=1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "mission_control": "T-MINUS",
        "server_time": datetime.now(timezone.utc).isoformat(),
    })


@app.route("/api/countdown", methods=["GET", "POST"])
def countdown():
    global LAUNCH_TIME

    # Allow the frontend to set a new launch time.
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        launch_value = data.get("launch_time")

        if not isinstance(launch_value, str):
            return jsonify({
                "error": "Provide launch_time as an ISO date-time string."
            }), 400

        try:
            target = datetime.fromisoformat(
                launch_value.replace("Z", "+00:00")
            )

            # Treat timestamps without a timezone as UTC.
            if target.tzinfo is None:
                target = target.replace(tzinfo=timezone.utc)

            target = target.astimezone(timezone.utc)

        except ValueError:
            return jsonify({
                "error": "Invalid launch date or time."
            }), 400

        if target <= datetime.now(timezone.utc):
            return jsonify({
                "error": "Launch time must be in the future."
            }), 400

        LAUNCH_TIME = target

    now = datetime.now(timezone.utc)
    remaining = max(0, int((LAUNCH_TIME - now).total_seconds()))

    return jsonify({
        "days": remaining // 86400,
        "hours": (remaining % 86400) // 3600,
        "minutes": (remaining % 3600) // 60,
        "seconds": remaining % 60,
        "launched": remaining == 0,
        "launch_time": LAUNCH_TIME.isoformat(),
    })


@app.route("/api/side-quest")
def side_quest():
    return jsonify({
        "quest": random.choice(SIDE_QUESTS)
    })


@app.route("/api/anomaly")
def anomaly():
    return jsonify(random.choice(ANOMALIES))


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "API endpoint not found"}), 404

    return "Page not found", 404


if __name__ == "__main__":
    app.run(debug=True)


