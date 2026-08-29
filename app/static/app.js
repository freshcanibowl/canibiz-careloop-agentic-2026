const state = { planId: "", petId: "", tasks: [], observation: null, renderedBrief: "" };
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

const pause = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

$("#run-demo").addEventListener("click", async (event) => {
  const button = event.currentTarget;
  button.disabled = true;
  $("#plan-id").value = `guided-pika-${Date.now().toString().slice(-7)}`;
  $("#pet-id").value = "pet-pika";
  $("#observation-day").value = "3";
  $("#owner-message").value = "Pika's poop was softer today, around 5. She finished her food and has not vomited.";
  updateCounter();
  try {
    state.planId = $("#plan-id").value;
    state.petId = $("#pet-id").value;
    state.renderedBrief = "";
    $("#download-brief").disabled = true;

    setNotice("Step 1/4 · Creating and persisting typed follow-up tasks…");
    const created = await request("/plans", {
      plan_id: state.planId,
      pet_id: state.petId,
      instructions: $("#instructions").value.trim(),
      start_date: $("#start-date").value,
      review_date: $("#review-date").value,
    });
    state.tasks = created.tasks;
    $("#task-count").textContent = `${state.tasks.length} typed tasks`;
    renderTimeline(state.tasks);
    activateStep(1);
    await pause(350);

    setNotice("Step 2/4 · Gemini is structuring Pika’s owner update…");
    const observed = await request("/observations", {
      plan_id: state.planId,
      pet_id: state.petId,
      day: 3,
      message: $("#owner-message").value,
    });
    state.observation = observed.observation;
    state.tasks = observed.tasks;
    renderTimeline(state.tasks);
    const output = $("#structured-output");
    output.hidden = false;
    output.innerHTML = `<strong>Structured observation</strong><br>Stool: ${observed.observation.stool_score ?? "—"} · Appetite: ${observed.observation.appetite ?? "—"} · Vomiting: ${observed.observation.vomiting ?? "—"}<br>Safety: ${observed.safety.status}`;
    activateStep(2);
    await pause(350);

    setNotice("Step 3/4 · Detecting missing actions and creating follow-up…");
    const checked = await request("/follow-up/check", { plan_id: state.planId, current_day: 4 });
    renderActions(checked.actions);
    activateStep(2);
    await pause(350);

    setNotice("Step 4/4 · Building the professional VetBrief…");
    const briefResult = await request("/vetbrief", { plan_id: state.planId, pet_id: state.petId, through_day: 4 });
    renderBrief(briefResult.brief);
    state.renderedBrief = briefResult.rendered;
    $("#download-brief").disabled = false;
    activateStep(3);
    setNotice("Guided demo complete · Persistent task state, Gemini, agent follow-up, and VetBrief verified.", "success");
    $("#brief-section").scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (error) {
    setNotice(`Guided demo stopped · ${error.message}`, "error");
  } finally {
    button.disabled = false;
  }
});

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
    state.renderedBrief = result.rendered;
    $("#download-brief").disabled = false;
    activateStep(3);
    setNotice("VetBrief generated from persisted workflow evidence.", "success");
  } catch (error) { setNotice(error.message, "error"); }
});

$("#download-brief").addEventListener("click", () => {
  if (!state.renderedBrief) return;
  const blob = new Blob([state.renderedBrief], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  const safePlanId = state.planId.replace(/[^a-z0-9_-]/gi, "-");
  link.href = URL.createObjectURL(blob);
  link.download = `VetBrief-${safePlanId}.txt`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(link.href);
  setNotice("VetBrief downloaded for professional review.", "success");
});

document.querySelectorAll(".rail-step").forEach((step, index) => step.addEventListener("click", () => {
  document.getElementById(step.dataset.target).scrollIntoView({ behavior: "smooth", block: "start" });
  activateStep(index);
}));
$("#owner-message").addEventListener("input", updateCounter);
seedForm();
