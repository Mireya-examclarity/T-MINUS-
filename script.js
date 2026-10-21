document.addEventListener("DOMContentLoaded", () => {
  // getting all elements - there is probably better way but this works


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

  // load from localStorage - sometimes it breaks so try catch

  let tasks = [];
  try 

    {let saved = localStorage.getItem("tminus-tasks");
    if (saved) 
      { tasks = JSON.parse(saved);}}
    
  
   catch (e) 
    { console.log("couldnt load tasks", e);
    tasks = [];}
  

  let payloadState = {};
  try 
   { let savedPayload = localStorage.getItem("tminus-payload");
    if (savedPayload) payloadState = JSON.parse(savedPayload);}
   catch 
    { payloadState = {};}
  

  let countdownTimer = null;
  let launchTimestamp = null;

  // function to call api - i copied this from stackoverflow and edited
  async function apiRequest(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json();
    if (!response.ok) 
      {  throw new Error(data.error || "Something went wrong.");}
    
    return data;}
  

  function formatTime(seconds) 
    { let days = Math.floor(seconds / 86400);
    let hours = Math.floor((seconds % 86400) / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;

    // pad with 0 if needed

    if (days < 10) days = "0" + days;
    if (hours < 10) hours = "0" + hours;
    if (minutes < 10) minutes = "0" + minutes;
    if (secs < 10) secs = "0" + secs;

    return days + ":" + hours + ":" + minutes + ":" + secs;} 
  

  function updateClock() {
    if (launchTimestamp == null) return;

    let remaining = Math.max(0, Math.floor((launchTimestamp - Date.now()) / 1000));
    countdown.textContent = formatTime(remaining);

    if (remaining == 0) 
      {launchStatus.textContent = "🚀 LAUNCH TIME REACHED";
      launchStatus.style.color = "#65ffbd";}
     else 
      { launchStatus.textContent = "SYSTEM ONLINE • COUNTDOWN ACTIVE";
      launchStatus.style.color = "";}}
    

  async function loadCountdown() {
    try 
      {const data = await apiRequest("/api/countdown");
      launchTimestamp = new Date(data.launch_time).getTime();

      if (countdownTimer) clearInterval(countdownTimer);
      updateClock();
      countdownTimer = setInterval(updateClock, 1000);

      launchDate.value = "";
      launchFeedback.textContent = "Launch target: " + new Date(launchTimestamp).toLocaleString();}
    catch (error) 
      {  launchStatus.textContent = "CONNECTION ERROR";
      launchFeedback.textContent = error.message + " Make sure Flask is running.";}}
    
  

  launchButton.addEventListener("click", async () => 
    {  if (!launchDate.value) 
      {launchFeedback.textContent = "Choose a  launch date and time first.";
      launchDate.focus();
      return;}
    

    const target = new Date(launchDate.value);
    if (isNaN(target.getTime()) || target <= new Date()) 
      {launchFeedback.textContent = "Please choose a valid date and time in the future.";
      return;}
    

    launchButton.disabled = true;
    launchFeedback.textContent = "Updating mission clock...";

    try 
       {  const data = await apiRequest("/api/countdown", 
       {  method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ launch_time: target.toISOString() }) });
     
      launchTimestamp = new Date(data.launch_time).getTime();
      updateClock();
      launchFeedback.textContent = "Launch time updated: " + target.toLocaleString();}
     catch (error) 
        {   launchFeedback.textContent = error.message;}
     finally 
      {launchButton.disabled = false;}});
    
  

  // show tasks on screen

  function renderTasks() 
    { taskList.innerHTML = ""; // clear old

    let completed = 0;
    for (let t of tasks) if (t.done) completed++;

    
    let total = tasks.length;
    taskSummary.textContent = completed + " of " + total + " objectives complete";
    
    if (total == 0) 
      {progressBar.style.width =  "0%";}
     else 
     {  progressBar.style.width = (completed / total * 100) + "%";}
    

    emptyTasks.hidden = total > 0;

    for (let task of tasks) 
      { const li = document.createElement("li");
      if (task.done) li.classList.add("completed");

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked =  task.done; 
      
      checkbox.addEventListener("change", () =>  
        {task.done = checkbox.checked;
        localStorage.setItem("tminus-tasks", JSON.stringify(tasks));
        renderTasks();});
      

      const text = document.createElement("span");

      text.textContent = task.text;
               
      const delBtn = document.createElement("button");

      delBtn.type = "button";

      delBtn.className = "delete-task";

      delBtn.textContent = " Delete ";
      delBtn.onclick = () => 
        {tasks = tasks.filter((entry) => entry.id !== task.id);   
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

    tasks.push
      ({ id: Date.now().toString() + "-" +  Math.random().toString(36 ).slice( 2, 5), 
      text: text,
      done: false});
    

    localStorage.setItem("tminus-tasks", JSON.stringify(tasks));
    renderTasks();
    taskInput.value = "";
    taskInput.focus();});
  

  // payload stuff
  function renderPayload() 
    {  const boxes = payloadList.querySelectorAll('input[type="checkbox"]');
    let secured = 0;
    boxes.forEach((box) => {
      let key = box.dataset.payload;
      if (payloadState[key]) 
        { box.checked = true;
        secured++;}
       else 
        {box.checked = false;} });
      
    payloadSummary.textContent = secured + " of " + boxes.length + " items secured";}
  

  payloadList.addEventListener("change", (event) => 
   { let checkbox = event.target;
    if (checkbox.type != "checkbox") return;
    payloadState[checkbox.dataset.payload] = checkbox.checked;
    localStorage.setItem("tminus-payload", JSON.stringify(payloadState));
    renderPayload(); });

  
 

  resetBtn.addEventListener("click", () => {
    let allBoxes = payloadList.querySelectorAll('input[type="checkbox"]');
    allBoxes.forEach((box) => {
      payloadState[box.dataset.payload] = false;});
    localStorage.setItem("tminus-payload", JSON.stringify(payloadState));
    renderPayload(); });
 

  // anomaly - gets random advice from backend

  anomalyButton.addEventListener("click", async () => {
    anomalyButton.disabled = true; 

    anomalyMessage.textContent = " Scanning for mission anomalies...";
    try {
      const data = await apiRequest("/api/anomaly");
      anomalyMessage.textContent = data.code + " — " + data.title + ": " + data.message;}
     catch (error) 
      {  anomalyMessage.textContent = error.message;}
     finally 
      {  anomalyButton.disabled = false;}});
    
  

  sideQuestButton.addEventListener("click", async () => {
    sideQuestButton.disabled = true;
    sideQuestMessage.textContent = "Finding a new side quest...";
    try 
      {const data = await apiRequest("/api/side-quest");
      sideQuestMessage.textContent = "✨ " + data.quest; }

     catch (error) 
      {   sideQuestMessage.textContent = error.message;}

     finally 
     {  sideQuestButton.disabled = false;}});
    
  

  // start
  renderTasks();
  renderPayload();

  // check if server is online
  fetch("/api/status").then(r => r.json()).then(() => 
    { loadCountdown();})

  .catch(() => 

   { launchStatus.textContent = "MISSION CONTROL OFFLINE";});});