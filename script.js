
// T-MINUS | Mission Control
document.addEventListener("DOMContentLoaded", () => {
    const $ = (selector) => document.querySelector(selector);

    // Safe browser storage helpers
    function loadData(key, fallback) {
        try {
            const saved = localStorage.getItem(key);
            return saved === null ? fallback : JSON.parse(saved);
        } catch {
            return fallback;
        }
    }

    function saveData(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch {
            // The site still works if browser storage is unavailable.
        }
    }

    // 1. MISSION OBJECTIVES
    let tasks = loadData("tminus-tasks", []);
    if (!Array.isArray(tasks)) tasks = [];

    const taskForm = $("#task-form");
    const taskInput = $("#task-input");
    const taskList = $("#task-list");
    const taskProgress = $("#task-progress");

    function renderTasks() {
        taskList.replaceChildren();

        tasks.forEach((task, index) => {
            const item = document.createElement("li");
            item.classList.toggle("completed", task.done);

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.checked = task.done;
            checkbox.setAttribute("aria-label", "Complete " + task.text);

            checkbox.addEventListener("change", () => {
                tasks[index].done = checkbox.checked;
                saveData("tminus-tasks", tasks);
                renderTasks();
            });

            const text = document.createElement("span");
            text.textContent = task.text;

            const remove = document.createElement("button");
            remove.type = "button";
            remove.className = "delete-task";
            remove.textContent = "Remove";
            remove.setAttribute("aria-label", "Remove " + task.text);

            remove.addEventListener("click", () => {
                tasks.splice(index, 1);
                saveData("tminus-tasks", tasks);
                renderTasks();
            });

            item.append(checkbox, text, remove);
            taskList.append(item);
        });

        const completed = tasks.filter(task => task.done).length;
        taskProgress.textContent =
            `${completed} of ${tasks.length} objectives complete`;

        if (tasks.length > 0 && completed === tasks.length) {
            taskProgress.textContent += " — Mission accomplished! 🎉";
        }
    }

    taskForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const text = taskInput.value.trim();
        if (!text) return;

        tasks.push({ text, done: false });
        saveData("tminus-tasks", tasks);
        renderTasks();

        taskInput.value = "";
        taskInput.focus();
    });

    renderTasks();

    // 2. PAYLOAD CHECKLIST
    const payloadItems = document.querySelectorAll("[data-payload]");

    payloadItems.forEach((checkbox) => {
        const key = "tminus-payload-" + checkbox.dataset.payload;
        checkbox.checked = loadData(key, false) === true;

        checkbox.addEventListener("change", () => {
            saveData(key, checkbox.checked);
        });
    });

    // 3. LAUNCH COUNTDOWN
    const launchInput = $("#launch-time");
    const countdown = $("#countdown");
    const launchButton = $("#set-countdown");

    let launchTarget = loadData("tminus-launch", null);
    let countdownTimer;

    function updateCountdown() {
        if (!launchTarget) {
            countdown.textContent =
                "Set a launch time to begin your countdown.";
            return;
        }

        const remaining = new Date(launchTarget).getTime() - Date.now();

        if (!Number.isFinite(remaining)) {
            countdown.textContent = "Please choose a valid launch time.";
            return;
        }

        if (remaining <= 0) {
            countdown.textContent =
                "🚀 Launch time reached! You're ready to go.";
            return;
        }

        const totalSeconds = Math.floor(remaining / 1000);
        const days = Math.floor(totalSeconds / 86400);
        const hours = Math.floor((totalSeconds % 86400) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        countdown.textContent =
            `T-minus ${days}d ${hours}h ${minutes}m ${seconds}s`;
    }

    function startCountdown() {
        clearInterval(countdownTimer);
        updateCountdown();

        if (launchTarget &&
            new Date(launchTarget).getTime() > Date.now()) {
            countdownTimer = setInterval(updateCountdown, 1000);
        }
    }

    if (launchTarget) {
        launchInput.value = launchTarget;
    }

    launchButton.addEventListener("click", () => {
        if (!launchInput.value) {
            countdown.textContent = "Choose your launch date and time first.";
            launchInput.focus();
            return;
        }

        const chosenTime = new Date(launchInput.value).getTime();

        if (!Number.isFinite(chosenTime) || chosenTime <= Date.now()) {
            countdown.textContent = "Choose a future date and time.";
            return;
        }

        launchTarget = launchInput.value;
        saveData("tminus-launch", launchTarget);
        startCountdown();
    });

    startCountdown();

    // 4. MISSION ANOMALIES
    const tips = [
        "Running late? Pick the three things that matter most and start there.",
        "Feeling overwhelmed? Break your next task into a step that takes five minutes.",
        "Forgot something? Pause, check your payload list, and adjust your plan.",
        "Lost focus? Take a breath, clear one distraction, and restart with one small step.",
        "Plans changed? That's okay, astronaut. Choose your next best action.",
        "Low on energy? Take a short break and return to one manageable task."
    ];

    let lastTip = -1;

    $("#anomaly-button").addEventListener("click", () => {
        let nextTip;

        do {
            nextTip = Math.floor(Math.random() * tips.length);
        } while (tips.length > 1 && nextTip === lastTip);

        lastTip = nextTip;
        $("#anomaly-message").textContent = tips[nextTip];
    });
});
