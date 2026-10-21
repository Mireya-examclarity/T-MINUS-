document.addEventListener("DOMContentLoaded", () => {
  const countdown = document.querySelector("#countdown"); 
  const launchStatus = document.querySelector("#launch-status");
  const launchDate = document.querySelector("#launch-date");
  const launchButton = document.querySelector("#set-launch");
  const launchFeedback = document.querySelector("#launch-feedback");

  const taskForm = document.querySelector("#task-form");
  const taskInput = document.querySelector("#task-input");
  const taskList = document.querySelector("#task-list");
  const taskSummary = document.querySelector("#task-summary");
  const emptyTasks = document.querySelector("#empty-tasks");
  const progressBar = document.querySelector("#progress-bar");

  const payloadList = document.querySelector("#payload-list");
  const payloadSummary = document.querySelector("#payload-summary");
  const resetBtn = document.querySelector("#reset-payload");

  const anomalyMessage = document.querySelector("#anomaly-message");
  const anomalyButton = document.querySelector("#anomaly-button");
  const sideQuestMessage = document.querySelector("#side-quest-message");
  const sideQuestButton = document.querySelector("#side-quest-button");

  // same data but now in frontend - no api needed
  const SIDE_QUESTS = [
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
    "Stand up, go outside(Can you feel the air?) and return with fresh energy." ];
 

  const ANOMALIES = [
    {code: "ANOMALY-001", title: " LOW FOCUS DETECTED", message: "Your attention is drifting. Focus on one small objective."},
    {code: "ANOMALY-002", title: "UNKNOWN DISTRACTION", message: "Remove one distraction pulling you off course."},
    {code: "ANOMALY-003", title: "MISSION  DELAY", message: "Break the next objective into a smaller step."},
    {code: "ANOMALY-004", title: "LOW ENERGY SIGNAL", message: "Drink water or take a short break."},
    {code: "ANOMALY-005", title: "UNEXPECTED TASK", message: "Decide whether the surprise objective needs attention now.(IS PROJECTS IMPORTANT?)"},
    {code: "ANOMALY-006", title: "NAVIGATION  ERROR", message: "Choose your next single step."},
    {code: "ANOMALY-007", title: "SYSTEMS  OVERLOADED", message: "Pause. You don't have to solve everything at once."},
    {code: "ANOMALY-008", title: " UNPLANNED COMMUNICATION", message: "Notifications can wait(Your exam will not bro 🥹 ). Return to your objective."}];
  

  let tasks = [];
  try { let saved = localStorage.getItem("tminus-tasks"); if (saved) tasks = JSON.parse(saved); } 
  catch (e) { console.log("couldnt load tasks", e); tasks = []; }

  let payloadState = {};
  try { let savedPayload = localStorage.getItem("tminus-payload"); if (savedPayload) payloadState = JSON.parse(savedPayload); }
  catch { payloadState = {}; }

  let countdownTimer = null;
  let launchTimestamp = null;

  // load launch from localStorage instead of api

  let savedLaunch = localStorage.getItem("tminus-launch");
  if (savedLaunch) launchTimestamp = parseInt(savedLaunch);
  else launchTimestamp = Date.now() + 3600000; // 2 hour default

  function formatTime(seconds) 
    
  {let days = Math.floor(seconds / 86400);
    let hours = Math.floor((seconds % 86400) / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;
    if (days < 10) days = "0" + days;
    if (hours < 10) hours = "0" + hours;
    if (minutes < 10) minutes = "0" + minutes;
    if (secs < 10) secs = "0" + secs;
    return days + ":" + hours + ":" + minutes + ":" + secs; }
  

  function updateClock() 
    {if (launchTimestamp == null) return;
    let remaining = Math.max(0, Math.floor((launchTimestamp - Date.now()) / 1000));
    countdown.textContent = formatTime(remaining);
    if (remaining == 0) {
      launchStatus.textContent = "🚀 LAUNCH TIME REACHED";
      launchStatus.style.color = "#65ffbd";}
     else 
      { launchStatus.textContent = "SYSTEM ONLINE • COUNTDOWN ACTIVE";
      launchStatus.style.color = "";}}
    
  

  // start clock immediately 

  updateClock();
  countdownTimer = setInterval(updateClock, 1000);
  launchFeedback.textContent = "Launch target: " + new Date(launchTimestamp).toLocaleString();
  launchStatus.textContent = "SYSTEM ONLINE • COUNTDOWN ACTIVE";

  launchButton.addEventListener("click", () => 
  
    { if (!launchDate.value) 
     { launchFeedback.textContent = "Choose a  launch date and time first.";
      launchDate.focus(); return;}
    
    const target = new Date(launchDate.value);
    if (isNaN(target.getTime()) || target <= new Date()) 
     { launchFeedback.textContent = "Please choose a valid date and time in the future."; return;}
    
    launchTimestamp = target.getTime();
    localStorage.setItem("tminus-launch", launchTimestamp.toString());
    updateClock();
    launchFeedback.textContent = "Launch time updated: " + target.toLocaleString(); });

 

  function renderTasks()

   { taskList.innerHTML = "";
    let completed = 0;
    for (let t of tasks) if (t.done) completed++;
    let total = tasks.length;
    taskSummary.textContent = completed + " of " + total + " objectives complete";
    if (total == 0) progressBar.style.width = "0%";
    else progressBar.style.width = (completed / total * 100) + "%";
    emptyTasks.hidden = total > 0;

    for (let task of tasks) 
     { const li = document.createElement("li");
      if (task.done) li.classList.add("completed");
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = task.done; 
      checkbox.addEventListener("change", () => 
       { task.done = checkbox.checked;
        localStorage.setItem("tminus-tasks", JSON.stringify(tasks));
        renderTasks();});
      
      const text = document.createElement("span");
      text.textContent = task.text;
      const delBtn = document.createElement("button");
      delBtn.type = "button";
      delBtn.className = "delete-task";
      delBtn.textContent = " Delete ";
      delBtn.onclick = () => 
       { tasks = tasks.filter((entry) => entry.id !== task.id);   
        localStorage.setItem("tminus-tasks", JSON.stringify(tasks));
        renderTasks();};
      
      li.appendChild(checkbox);
      li.appendChild(text);
      li.appendChild(delBtn);
      taskList.appendChild(li);}}
    
  

  taskForm.addEventListener("submit", (e) => 
    { e.preventDefault();
    let text = taskInput.value.trim();
    if (!text) return;
    tasks.push({ id: Date.now().toString() + "-" + Math.random().toString(36).slice(2, 5), text: text, done: false});
    localStorage.setItem("tminus-tasks", JSON.stringify(tasks));
    renderTasks();
    taskInput.value = "";
    taskInput.focus(); });
 

  function renderPayload() 
    { const boxes = payloadList.querySelectorAll('input[type="checkbox"]');
    let secured = 0;
    boxes.forEach((box) => 
      { let key = box.dataset.payload;
      if (payloadState[key]) { box.checked = true; secured++; }
      else box.checked = false;});
    
    payloadSummary.textContent = secured + " of " + boxes.length + " items secured";}
  

  payloadList.addEventListener("change", (event) => 
    { let checkbox = event.target;
    if (checkbox.type != "checkbox") return;
    payloadState[checkbox.dataset.payload] = checkbox.checked;
    localStorage.setItem("tminus-payload", JSON.stringify(payloadState));
    renderPayload(); });
 

  resetBtn.addEventListener("click", () => 
    { let allBoxes = payloadList.querySelectorAll('input[type="checkbox"]');
    allBoxes.forEach((box) => { payloadState[box.dataset.payload] = false; });
    localStorage.setItem("tminus-payload", JSON.stringify(payloadState));
    renderPayload(); });
  

  anomalyButton.addEventListener("click", () => 
    { let picked = ANOMALIES[Math.floor(Math.random() * ANOMALIES.length)];
    anomalyMessage.textContent = picked.code + " — " + picked.title + ": " + picked.message;});
  

  sideQuestButton.addEventListener("click", () => {
    let quest = SIDE_QUESTS[Math.floor(Math.random() * SIDE_QUESTS.length)];
    sideQuestMessage.textContent = "✨ " + quest;});
  

  renderTasks();
  renderPayload();});
