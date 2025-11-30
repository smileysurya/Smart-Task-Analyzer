const tasks = []; // local list before sending to backend

document.getElementById("task-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const t = {
    id: Date.now().toString(),
    title: document.getElementById("title").value.trim(),
    due_date: document.getElementById("due_date").value || null,
    estimated_hours: parseFloat(document.getElementById("estimated_hours").value) || 1,
    importance: parseInt(document.getElementById("importance").value) || 5,
    dependencies: (document.getElementById("dependencies").value || "").split(",").map(s => s.trim()).filter(x => x)
  };
  tasks.push(t);
  document.getElementById("task-form").reset();
  renderLocalTasks();
});

function renderLocalTasks(){
  const r = document.getElementById("results");
  r.innerHTML = "<h4>Local Input (not scored)</h4>";
  tasks.forEach(t => {
    const div = document.createElement("div");
    div.className = "task";
    div.innerHTML = `<div><strong>${t.title}</strong><div class="details">due: ${t.due_date || "—"} • est: ${t.estimated_hours}h • imp: ${t.importance}</div></div>
                     <div class="code">${t.id}</div>`;
    r.appendChild(div);
  });
}

document.getElementById("analyze").addEventListener("click", async () => {
  let payloadTasks = [];
  const bulkText = document.getElementById("bulk").value.trim();
  if (bulkText) {
    try {
      const parsed = JSON.parse(bulkText);
      if (Array.isArray(parsed)) payloadTasks = parsed;
      else { alert("Bulk JSON must be an array of tasks."); return; }
    } catch (e) {
      alert("Invalid JSON."); return;
    }
  }
  if (tasks.length && payloadTasks.length) {
    // merge
    payloadTasks = tasks.concat(payloadTasks);
  } else if (tasks.length) {
    payloadTasks = tasks;
  } else if (!payloadTasks.length) {
    alert("Add tasks or paste JSON first.");
    return;
  }

  // If user selected a client-side strategy, we can reorder locally; else use backend scoring
  const strategy = document.getElementById("strategy").value;
  if (strategy === "fastest") {
    payloadTasks.sort((a,b) => (a.estimated_hours || 0) - (b.estimated_hours || 0));
    showResults(payloadTasks.map(t => ({...t, score: (10/(1+(t.estimated_hours||1))).toFixed(2), explanation:["Client strategy: Fastest Wins"]})));
    showSuggestions(payloadTasks.slice(0,3));
    return;
  } else if (strategy === "impact") {
    payloadTasks.sort((a,b) => (b.importance||0) - (a.importance||0));
    showResults(payloadTasks.map(t => ({...t, score: (t.importance||0).toFixed(2), explanation:["Client strategy: High Impact"]})));
    showSuggestions(payloadTasks.slice(0,3));
    return;
  } else if (strategy === "deadline") {
    payloadTasks.sort((a,b) => new Date(a.due_date || "9999-12-31") - new Date(b.due_date || "9999-12-31"));
    showResults(payloadTasks.map((t,i)=>({...t, score: (100 - i).toFixed(2), explanation:["Client strategy: Deadline Driven"]})));
    showSuggestions(payloadTasks.slice(0,3));
    return;
  }

  // Default: call backend analyze
  try {
    const resp = await fetch("/api/tasks/analyze/", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({tasks: payloadTasks})
    });
    const data = await resp.json();
    if (!resp.ok) {
      alert("Error: " + JSON.stringify(data));
      return;
    }
    const out = data.tasks || [];
    showResults(out);
    showSuggestions(out.slice(0,3));
  } catch (err) {
    alert("Network error: " + err.message);
  }
});

function showResults(list){
  const r = document.getElementById("results");
  r.innerHTML = "";
  list.forEach(t => {
    const div = document.createElement("div");
    div.className = "task";
    const level = t.score >= 15 ? "high" : t.score >= 8 ? "medium" : "low";
    div.innerHTML = `<div>
      <strong>${t.title}</strong>
      <div class="details">due: ${t.due_date || "—"} • est: ${t.estimated_hours || "—"}h • imp: ${t.importance || "—"}</div>
      <div class="details">explanation: ${Array.isArray(t.explanation) ? t.explanation.join(" | ") : t.explanation}</div>
    </div>
    <div>
      <div class="badge ${level}">${t.score}</div>
      <div class="code">${t.id}</div>
    </div>`;
    r.appendChild(div);
  });
}

function showSuggestions(list) {
  const s = document.getElementById("suggestions");
  s.innerHTML = "";
  list.forEach(t => {
    const div = document.createElement("div");
    div.className = "task";
    div.innerHTML = `<div><strong>${t.title}</strong><div class="details">Reason: ${t.reason_summary || (Array.isArray(t.explanation) ? t.explanation[0] : "")}</div></div><div class="code">${t.id}</div>`;
    s.appendChild(div);
  });
}
