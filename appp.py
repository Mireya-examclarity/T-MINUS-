import streamlit as st
import random
import time
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="T-MINUS | Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "missions": [],
    "mission_time": 2 * 60 * 60,
    "timer_running": False,
    "timer_started_at": None,
    "side_quest": "Mission systems ready. Generate a side quest.",
    "anomaly": "Mission systems nominal. No anomalies detected.",
    "mission_name": "PROJECT T-MINUS",
    "astronaut": "COMMANDER",
    "mission_launched": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# DATA
# =========================================================

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


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        radial-gradient(
            circle at 50% -10%,
            rgba(37, 99, 235, 0.30),
            transparent 40%
        ),
        radial-gradient(
            circle at 90% 50%,
            rgba(6, 182, 212, 0.10),
            transparent 35%
        ),
        #020617;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: white !important;
    }

    .hero {
        text-align: center;
        padding: 25px 0 35px 0;
    }

    .eyebrow {
        color: #22d3ee;
        font-size: 12px;
        letter-spacing: 4px;
        font-weight: bold;
    }

    .hero-title {
        font-size: 70px;
        font-weight: 900;
        letter-spacing: -4px;
        background: linear-gradient(
            90deg,
            #ffffff,
            #60a5fa,
            #22d3ee
        );
        -webkit-background-clip: text;
        color: transparent;
        margin: 5px 0;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 16px;
    }

    .card {
        background: rgba(15, 23, 42, 0.80);
        border: 1px solid rgba(96, 165, 250, 0.18);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.25);
    }

    .countdown {
        text-align: center;
        font-family: "Courier New", monospace;
        font-size: 75px;
        font-weight: bold;
        letter-spacing: 5px;
        color: white;
        text-shadow: 0 0 25px rgba(34, 211, 238, 0.40);
    }

    .countdown-label {
        text-align: center;
        color: #22d3ee;
        font-size: 11px;
        letter-spacing: 3px;
        font-weight: bold;
    }

    .online {
        color: #22c55e;
        font-weight: bold;
        font-size: 12px;
        letter-spacing: 2px;
    }

    .stat {
        background: rgba(15, 23, 42, 0.80);
        border: 1px solid rgba(96, 165, 250, 0.15);
        border-radius: 14px;
        padding: 20px;
        min-height: 95px;
    }

    .stat-label {
        color: #94a3b8;
        font-size: 10px;
        letter-spacing: 2px;
    }

    .stat-value {
        color: white;
        font-size: 30px;
        font-weight: bold;
    }

    .mission {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .mission-complete {
        opacity: 0.45;
        text-decoration: line-through;
    }

    .feature {
        min-height: 180px;
    }

    .feature-icon {
        font-size: 35px;
    }

    .feature-text {
        color: #94a3b8;
        line-height: 1.6;
    }

    .launch-ready {
        color: #22c55e;
        font-weight: bold;
        text-align: center;
        letter-spacing: 2px;
    }

    .footer {
        text-align: center;
        color: #475569;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 25px;
        margin-top: 50px;
        font-size: 11px;
        letter-spacing: 2px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# TIMER ENGINE
# =========================================================

if st.session_state.timer_running:

    elapsed = int(
        time.time() - st.session_state.timer_started_at
    )

    remaining = max(
        0,
        st.session_state.mission_time - elapsed
    )

    if remaining == 0:

        st.session_state.mission_time = 0
        st.session_state.timer_running = False
        st.session_state.mission_launched = True

    else:

        # Refresh the page every second while running.
        time.sleep(1)
        st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🚀 T-MINUS")

    st.markdown(
        """
        ### MISSION CONTROL

        Transform everyday tasks into
        space missions.

        ---
        """
    )

    st.markdown(
        '<p class="online">● SYSTEM ONLINE</p>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### 🛰️ Mission Parameters")

    st.session_state.mission_name = st.text_input(
        "Mission name",
        value=st.session_state.mission_name,
    )

    st.session_state.astronaut = st.text_input(
        "Mission operator",
        value=st.session_state.astronaut,
    )

    st.markdown("---")

    st.markdown("### 📡 System")

    st.write("🟢 Python: ONLINE")
    st.write("🟢 Streamlit: ONLINE")
    st.write("🟢 Mission Control: ONLINE")

    st.markdown("---")

    if st.button(
        "🔄 RESET ALL MISSION DATA",
        use_container_width=True,
    ):

        st.session_state.missions = []
        st.session_state.mission_time = 2 * 60 * 60
        st.session_state.timer_running = False
        st.session_state.timer_started_at = None
        st.session_state.mission_launched = False

        st.session_state.side_quest = (
            "Mission systems ready. Generate a side quest."
        )

        st.session_state.anomaly = (
            "Mission systems nominal. No anomalies detected."
        )

        st.rerun()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="eyebrow">
            NASA-INSPIRED PRODUCTIVITY SYSTEM
        </div>

        <div class="hero-title">
            T-MINUS
        </div>

        <div class="hero-subtitle">
            MISSION CONTROL FOR EVERYDAY PROBLEM-SOLVING
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MISSION HEADER
# =========================================================

st.markdown(
    f"""
    <div class="card">

        <div class="countdown-label">
            NEXT LAUNCH •
            {st.session_state.mission_name}
            • OPERATOR:
            {st.session_state.astronaut}
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# COUNTDOWN
# =========================================================

if st.session_state.timer_running:

    elapsed = int(
        time.time() - st.session_state.timer_started_at
    )

    display_seconds = max(
        0,
        st.session_state.mission_time - elapsed
    )

else:

    display_seconds = st.session_state.mission_time


hours = display_seconds // 3600

minutes = (display_seconds % 3600) // 60

seconds = display_seconds % 60


time_display = (
    f"{hours:02d}:"
    f"{minutes:02d}:"
    f"{seconds:02d}"
)


st.markdown(
    f"""
    <div class="countdown">
        {time_display}
    </div>

    <div class="countdown-label">
        T-MINUS MISSION CLOCK
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# TIMER CONTROLS
# =========================================================

timer_col1, timer_col2, timer_col3 = st.columns(3)


with timer_col1:

    if st.button(
        "▶ START MISSION",
        use_container_width=True,
    ):

        if st.session_state.mission_time > 0:

            st.session_state.timer_running = True

            st.session_state.timer_started_at = time.time()

            st.session_state.mission_launched = False

            st.rerun()


with timer_col2:

    if st.button(
        "❚❚ PAUSE",
        use_container_width=True,
    ):

        if st.session_state.timer_running:

            elapsed = int(
                time.time()
                - st.session_state.timer_started_at
            )

            st.session_state.mission_time = max(
                0,
                st.session_state.mission_time - elapsed
            )

        st.session_state.timer_running = False
        st.session_state.timer_started_at = None

        st.rerun()


with timer_col3:

    if st.button(
        "↻ RESET TIMER",
        use_container_width=True,
    ):

        st.session_state.mission_time = 2 * 60 * 60
        st.session_state.timer_running = False
        st.session_state.timer_started_at = None
        st.session_state.mission_launched = False

        st.rerun()


# =========================================================
# LAUNCH MESSAGE
# =========================================================

if st.session_state.mission_launched:

    st.error(
        "🚀 LAUNCH TIME REACHED — MISSION CLOCK COMPLETE!"
    )

else:

    if st.session_state.timer_running:

        st.markdown(
            '<p class="launch-ready">🟢 MISSION IN PROGRESS</p>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            '<p class="launch-ready">🟡 MISSION STANDBY</p>',
            unsafe_allow_html=True,
        )


# =========================================================
# MISSION STATISTICS
# =========================================================

missions = st.session_state.missions

total = len(missions)

completed = sum(
    1
    for mission in missions
    if mission["completed"]
)

active = total - completed


if total > 0:

    progress = int(
        (completed / total) * 100
    )

else:

    progress = 0


# =========================================================
# MISSION STATUS
# =========================================================

st.markdown("## 📊 Mission Status")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="stat">

            <div class="stat-label">
                OBJECTIVES
            </div>

            <div class="stat-value">
                {total}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        f"""
        <div class="stat">

            <div class="stat-label">
                ACTIVE
            </div>

            <div class="stat-value">
                {active}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:

    st.markdown(
        f"""
        <div class="stat">

            <div class="stat-label">
                COMPLETED
            </div>

            <div class="stat-value">
                {completed}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col4:

    st.markdown(
        f"""
        <div class="stat">

            <div class="stat-label">
                PROGRESS
            </div>

            <div class="stat-value">
                {progress}%
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PROGRESS BAR
# =========================================================

st.markdown("### MISSION PROGRESS")

st.progress(progress / 100)

st.caption(
    f"{completed} of {total} objectives complete"
)


# =========================================================
# OBJECTIVE CREATION
# =========================================================

st.markdown("## 🎯 Mission Objectives")


with st.form("objective_form", clear_on_submit=True):

    objective = st.text_input(
        "NEW OBJECTIVE",
        placeholder="Example: Complete NASA presentation",
    )

    submitted = st.form_submit_button(
        "🚀 ADD OBJECTIVE",
        use_container_width=True,
    )


if submitted:

    if objective.strip():

        st.session_state.missions.append(
            {
                "id": len(st.session_state.missions) + 1,
                "title": objective.strip(),
                "completed": False,
                "created": datetime.now().strftime("%H:%M"),
            }
        )

        st.success(
            "🚀 Objective successfully added to mission control!"
        )

        st.rerun()

    else:

        st.warning(
            "Please enter an objective."
        )


# =========================================================
# OBJECTIVE DISPLAY
# =========================================================

if not missions:

    st.info(
        "🛰️ No objectives detected. "
        "Add your first mission objective above."
    )

else:

    for mission in missions:

        col1, col2, col3 = st.columns(
            [0.10, 0.68, 0.22]
        )


        # -------------------------------------------------
        # NUMBER
        # -------------------------------------------------

        with col1:

            if mission["completed"]:

                st.markdown("### ✓")

            else:

                st.markdown(
                    f"### {mission['id']}"
                )


        # -------------------------------------------------
        # DETAILS
        # -------------------------------------------------

        with col2:

            if mission["completed"]:

                st.markdown(
                    f"""
                    <div class="mission mission-complete">

                        <strong>
                            {mission["title"]}
                        </strong>

                        <br>

                        <small>
                            COMPLETED •
                            {mission["created"]}
                        </small>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    f"""
                    <div class="mission">

                        <strong>
                            {mission["title"]}
                        </strong>

                        <br>

                        <small>
                            ACTIVE •
                            CREATED {mission["created"]}
                        </small>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


        # -------------------------------------------------
        # ACTION
        # -------------------------------------------------

        with col3:

            if not mission["completed"]:

                if st.button(
                    "✓ COMPLETE",
                    key=f"complete_{mission['id']}",
                    use_container_width=True,
                ):

                    mission["completed"] = True

                    st.balloons()

                    st.rerun()

            else:

                if st.button(
                    "🗑 DELETE",
                    key=f"delete_{mission['id']}",
                    use_container_width=True,
                ):

                    st.session_state.missions.remove(
                        mission
                    )

                    st.rerun()


# =========================================================
# MISSION EVENTS
# =========================================================

st.markdown("---")

st.markdown("## 🛰️ Mission Events")


event_col1, event_col2 = st.columns(2)


# =========================================================
# SIDE QUEST
# =========================================================

with event_col1:

    st.markdown(
        """
        <div class="card feature">

            <div class="feature-icon">
                🎲
            </div>

            <h2>
                SIDE QUEST
            </h2>

            <p class="feature-text">
                Optional challenges designed to
                make productivity more engaging.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🎲 GENERATE SIDE QUEST",
        use_container_width=True,
    ):

        st.session_state.side_quest = random.choice(
            SIDE_QUESTS
        )

        st.rerun()

    st.success(
        st.session_state.side_quest
    )


# =========================================================
# ANOMALY
# =========================================================

with event_col2:

    st.markdown(
        """
        <div class="card feature">

            <div class="feature-icon">
                🚨
            </div>

            <h2>
                MISSION ANOMALY
            </h2>

            <p class="feature-text">
                Unexpected problems become
                mission anomalies.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "⚠️ RUN SYSTEM CHECK",
        use_container_width=True,
    ):

        st.session_state.anomaly = random.choice(
            ANOMALIES
        )

        st.rerun()

    st.warning(
        st.session_state.anomaly
    )


# =========================================================
# MISSION SUMMARY
# =========================================================

st.markdown("---")

st.markdown(
    f"""
    <div class="card">

        <div style="
            text-align:center;
            padding:30px;
        ">

            <div style="
                color:#3b82f6;
                font-size:50px;
            ">
                🚀
            </div>

            <h2>
                Mission Briefing
            </h2>

            <p style="
                color:#94a3b8;
                max-width:700px;
                margin:auto;
                line-height:1.7;
            ">

                <strong>{st.session_state.mission_name}</strong>
                is being operated by
                <strong>{st.session_state.astronaut}</strong>.

                T-MINUS transforms everyday
                problem-solving into a space mission —
                making progress visible, goals actionable,
                and productivity more engaging.

            </p>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        T-MINUS • MISSION CONTROL

        <br><br>

        BUILT WITH PYTHON + STREAMLIT

    </div>
    """,
    unsafe_allow_html=True,
)


   

        

   

    

        



