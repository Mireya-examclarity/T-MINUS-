# 🚀 T-MINUS | Mission Control

> NASA-inspired productivity system that turns your boring to-do list into a space mission.

### What is T-MINUS?

T-MINUS transforms everyday problem-solving into a space mission. Instead of tasks, you have **mission objectives**. Instead of a timer, you have a **T-MINUS launch clock**. Instead of distractions, you have **mission anomalies**.

It makes progress visible, goals actionable, and productivity actually engaging.

### ✨ Features
- **Mission Clock** - 2 hour countdown with START / PAUSE / RESET
- **Mission Objectives** - Add, complete, delete objectives with localStorage persistence
- **Live Mission Stats** - Objectives, Active, Completed, Progress % with animated bar
- **Side Quest Generator** - Random productivity challenges to stay sharp
- **Mission Anomaly Check** - Turns distractions into NASA-style anomalies
- **Confetti Launch** - Celebrates when you complete objectives or launch time hits

### 🛠️ Tech Stack
- **Flask** - Backend (No more Streamlit sleeping)
- **HTML/CSS/JS + Chart.js** - Frontend with glassmorphism + space theme
- **Gunicorn + Render + GitHub** - Always-on deployment

### What I Fixed

My first version was on **Streamlit**. It looked good locally but on deployment it kept sleeping. After 15 mins of inactivity the link would die and users saw "Waking up" screen. For a productivity timer that needs to run live, that's useless.

So I rebuilt the whole app in **Flask**. Flask + Render never sleeps if you add UptimeRobot.




pip install -r requirements.txt
python app.py
