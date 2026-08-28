const state = { planId: "", petId: "", tasks: [], observation: null };
const $ = (selector) => document.querySelector(selector);

function isoDate(offsetDays = 0) {
  const value = new Date();
  value.setDate(value.getDate() + offsetDays);
  return value.toISOString().slice(0, 10);
}

function seedForm() {
  $("#plan-id").value = `demo-pika-${Date.now().toString().slice(-7)}`;
  $("#start-date").value = isoDate();
  $("#review-date").value = isoDate(7);
  updateCounter();
  loadRuntime();
}

async function loadRuntime() {
  try {
    const response = await fetch("/health");
    const health = await response.json();
    const cloud = health.storage_backend === "firestore";
    $("#storage-label").textContent = cloud ? "Firestore persisted" : "In-memory local mode";
    $("#storage-detail").textContent = cloud ? "Tasks and observation history" : "Offline reproducible development";
    $(".cloud-state").innerHTML = `<i aria-hidden="true"></i> ${cloud ? "Cloud Connected" : "Local Runtime"}`;
  } catch (_) {
    $("#storage-detail").textContent = "Runtime status unavailable";
  }
}

function setNotice(message, kind = "") {
  const notice = $("#notice");
  notice.textContent = message;
  notice.className = `notice ${kind}`.trim();
}

async function request(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data;
}

function activateStep(index) {
  document.querySelectorAll(".rail-step").forEach((step, i) => step.classList.toggle("active", i === index));
}

function renderTimeline(tasks) {
  const byDay = new Map();
  tasks.filter((task) => task.kind !== "PROFESSIONAL_REVIEW").forEach((task) => {
    if (!byDay.has(task.due_day)) byDay.set(task.due_day, []);
    byDay.get(task.due_day).push(task);
  });
  $("#timeline").innerHTML = Array.from({ length: 7 }, (_, i) => {
    const day = i + 1;
    const items = byDay.get(day) || [];
    const complete = items.length && items.every((item) => item.status === "COMPLETED");
    const status = complete ? "Done" : day < 3 ? "Due" : "Pending";
    const kind = complete ? "complete" : day < 3 ? "due" : "pending";
    const label = items.length ? items.map((item) => item.kind.replaceAll("_", " ")).join(" · ") : "No owner task";
    return `<li class="${kind}"><span>Day ${day}</span><span class="task-label" title="${label}">${label}</span><span class="task-status">${status}</span></li>`;
  }).join("");
}

function renderActions(actions) {
  $("#actions").innerHTML = actions.length ? actions.map((action) => `
    <div class="action-item">
      <strong>${action.action_type}</strong>
      Day ${action.day} · ${action.reason}
    </div>`).join("") : `<p class="empty-state">No missing actions at this checkpoint.</p>`;
}

function renderBrief(brief) {
  const outstanding = brief.outstanding_tasks.length
    ? `<ul>${brief.outstanding_tasks.map((item) => `<li>${item}</li>`).join("")}</ul>`
    : `<p>None due.</p>`;
  const timeline = brief.longitudinal_summary.length
    ? brief.longitudinal_summary.join("<br>")
    : "No owner observations yet.";
  $("#brief").innerHTML = `
    <h3><span>${brief.pet_id}</span><span>${brief.plan_id}</span></h3>
    <h4>Adherence</h4><div class="score">${brief.adherence_percent}%</div>
    <h4>Longitudinal summary</h4><p>${timeline}</p>
    <h4>Outstanding tasks</h4>${outstanding}
    <h4>Safety status</h4><span class="safety-state">${brief.safety_status}</span>`;
}

function updateCounter() { $("#message-count").textContent = $("#owner-message").value.length; }

$("#plan-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  setNotice("Creating typed tasks and persisting them…");
  try {
    state.planId = $("#plan-id").value.trim();
    state.petId = $("#pet-id").value.trim();
    const result = await request("/plans", {
      plan_id: state.planId,
      pet_id: state.petId,
      instructions: $("#instructions").value.trim(),
      start_date: $("#start-date").value,
      review_date: $("#review-date").value,
    });
    state.tasks = result.tasks;
    $("#task-count").textContent = `${state.tasks.length} typed tasks`;
    renderTimeline(state.tasks);
    activateStep(1);
    setNotice(`${state.tasks.length} tasks persisted to Firestore.`, "success");
    $("#observation-section").scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (error) { setNotice(error.message, "error"); }
  finally { button.disabled = false; }
});

$("#observation-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.planId) return setNotice("Create a care plan first.", "error");
  const button = event.submitter;
  button.disabled = true;
  setNotice("Gemini is structuring the owner update…");
  try {
    const result = await request("/observations", {
      plan_id: state.planId,
      pet_id: state.petId,
      day: Number($("#observation-day").value),
      message: $("#owner-message").value.trim(),
    });
    state.observation = result.observation;
    state.tasks = result.tasks;
    renderTimeline(state.tasks);
    const output = $("#structured-output");
    output.hidden = false;
    output.innerHTML = `<strong>Structured observation</strong><br>Stool: ${result.observation.stool_score ?? "—"} · Appetite: ${result.observation.appetite ?? "—"} · Vomiting: ${result.observation.vomiting ?? "—"}<br>Safety: ${result.safety.status}`;
    activateStep(2);
    setNotice("Observation persisted and safety routing complete.", "success");
  } catch (error) { setNotice(error.message, "error"); }
  finally { button.disabled = false; }
});

$("#check-followup").addEventListener("click", async () => {
  if (!state.planId) return setNotice("Create a care plan first.", "error");
  try {
    const result = await request("/follow-up/check", { plan_id: state.planId, current_day: 4 });
    renderActions(result.actions);
    activateStep(2);
    setNotice(`${result.actions.length} follow-up action(s) evaluated.`, "success");
  } catch (error) { setNotice(error.message, "error"); }
});

$("#generate-brief").addEventListener("click", async () => {
  if (!state.planId) return setNotice("Create a care plan first.", "error");
  try {
    const result = await request("/vetbrief", { plan_id: state.planId, pet_id: state.petId, through_day: 4 });
    renderBrief(result.brief);
    activateStep(3);
    setNotice("VetBrief generated from persisted workflow evidence.", "success");
  } catch (error) { setNotice(error.message, "error"); }
});

document.querySelectorAll(".rail-step").forEach((step, index) => step.addEventListener("click", () => {
  document.getElementById(step.dataset.target).scrollIntoView({ behavior: "smooth", block: "start" });
  activateStep(index);
}));
$("#owner-message").addEventListener("input", updateCounter);
seedForm();
