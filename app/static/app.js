let defaults = {};
let colTypes = {};
let columns = [];
let outcomes = [];

function setStatus(msg) {
  document.getElementById("status").textContent = msg || "";
}

function activeOutcome() {
  return document.getElementById("outcome").value;
}

function gatherFilters() {
  const excludePrev = document.getElementById("excludePrev").checked;
  const period = document.getElementById("period").value || null;
  const smoking_fix = document.getElementById("smoking_fix").value;
  return { exclude_prevalent: excludePrev, PERIOD: period ? Number(period) : null, smoking_fix };
}

function gatherPredictors() {
  const el = document.getElementById("predictors");
  return Array.from(el.selectedOptions).map(o => o.value);
}

function switchTab(name) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tablink").forEach(t => t.classList.remove("active"));
  document.getElementById("tab-" + name).classList.add("active");
  document.querySelector('.tablink[data-tab="' + name + '"]').classList.add("active");
}

async function fetchColumns() {
  const r = await fetch("/api/columns");
  const j = await r.json();
  columns = j.columns;
  colTypes = j.types;
  defaults = j.defaults;
  outcomes = Object.keys(defaults);
  const outcomeSel = document.getElementById("outcome");
  outcomes.forEach(o => {
    const opt = document.createElement("option");
    opt.value = o;
    opt.textContent = o;
    outcomeSel.appendChild(opt);
  });
  // Populate predictors (exclude time/event/outcome columns by heuristic)
  const predSel = document.getElementById("predictors");
  columns.forEach(c => {
    if (!c.toLowerCase().startsWith("time") && colTypes[c] !== "binary" || (colTypes[c] !== "binary" || !["ANGINA","HOSPMI","MI_FCHD","ANYCHD","STROKE","CVD","DEATH","HYPERTEN"].includes(c))) {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c + " (" + colTypes[c] + ")";
      predSel.appendChild(opt);
    } else {
      // still list binaries too
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c + " (" + colTypes[c] + ")";
      predSel.appendChild(opt);
    }
  });
}

async function runKM() {
  setStatus("Running KM...");
  try {
    const payload = { outcome: activeOutcome(), filters: gatherFilters() };
    const r = await fetch("/api/km", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload) });
    const j = await r.json();
    if (j.error) throw new Error(j.error);
    document.getElementById("kmJson").textContent = JSON.stringify(j.meta, null, 2);
    // load plot
    await loadPlot("km", "kmPlot");
    switchTab("km");
    setStatus("");
    // summary tab
    document.getElementById("summaryJson").textContent = JSON.stringify(j.meta, null, 2);
  } catch (e) {
    setStatus("KM error: " + e.message);
  }
}

async function runCox() {
  setStatus("Running Cox...");
  try {
    const payload = { outcome: activeOutcome(), filters: gatherFilters(), predictors: gatherPredictors(), missing: document.getElementById("missing").value };
    const r = await fetch("/api/cox", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload) });
    const j = await r.json();
    if (j.error) throw new Error(j.error);
    document.getElementById("coxJson").textContent = JSON.stringify(j.meta, null, 2);
    // table
    const tbl = document.getElementById("coxTable");
    tbl.innerHTML = "<tr><th>Variable</th><th>Level</th><th>HR</th><th>95% CI</th><th>p</th></tr>";
    j.rows.forEach(r => {
      const tr = document.createElement("tr");
      const ci = r.lcl.toFixed(3) + "–" + r.ucl.toFixed(3);
      tr.innerHTML = `<td>${r.var}</td><td>${r.level || ""}</td><td>${r.hr.toFixed(3)}</td><td>${ci}</td><td>${r.p.toExponential(2)}</td>`;
      tbl.appendChild(tr);
    });
    // load plot
    await loadPlot("cox", "coxPlot", { predictors: gatherPredictors(), missing: document.getElementById("missing").value });
    switchTab("cox");
    setStatus("");
    // summary tab
    document.getElementById("summaryJson").textContent = JSON.stringify(j.meta, null, 2);
  } catch (e) {
    setStatus("Cox error: " + e.message);
  }
}

async function loadPlot(kind, imgId, extra = {}) {
  const payload = Object.assign({ type: kind, format: "png", outcome: activeOutcome(), filters: gatherFilters() }, extra);
  const r = await fetch("/api/export_plot", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload) });
  if (!r.ok) throw new Error("plot export failed");
  const blob = await r.blob();
  document.getElementById(imgId).src = URL.createObjectURL(blob);
}

async function downloadPlot(kind) {
  const payload = { type: kind, format: "png", outcome: activeOutcome(), filters: gatherFilters() };
  const r = await fetch("/api/export_plot", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload) });
  if (!r.ok) { setStatus("Download failed"); return; }
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = kind + "_plot.png";
  a.click();
  URL.revokeObjectURL(url);
}

document.addEventListener("DOMContentLoaded", () => {
  fetchColumns();
  document.querySelectorAll(".tablink").forEach(btn => btn.addEventListener("click", () => switchTab(btn.dataset.tab)));
  document.getElementById("runKM").addEventListener("click", runKM);
  document.getElementById("runCox").addEventListener("click", runCox);
  document.getElementById("dlKM").addEventListener("click", () => downloadPlot("km"));
  document.getElementById("dlCox").addEventListener("click", () => downloadPlot("cox"));
});
