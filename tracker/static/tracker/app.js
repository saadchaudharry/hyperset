// Date picker on the day page
const datePick = document.getElementById("datepick");
if (datePick) {
  datePick.addEventListener("change", () => {
    if (datePick.value) window.location = `/day/${datePick.value}/`;
  });
}

// "+ Set" adds another reps/weight row to an exercise card
document.querySelectorAll("[data-add-set]").forEach((button) => {
  button.addEventListener("click", () => {
    const sets = button.closest("form").querySelector("[data-sets]");
    const rows = sets.querySelectorAll(".setrow:not(.head)");
    const row = rows[rows.length - 1].cloneNode(true);
    row.querySelectorAll("input").forEach((input) => (input.value = ""));
    row.querySelector(".setno").textContent = rows.length + 1;
    sets.appendChild(row);
    row.querySelector("input").focus();
  });
});

// Show a busy label while the AI estimates calories
document.querySelectorAll("form[data-busy-text]").forEach((form) => {
  form.addEventListener("submit", () => {
    const button = form.querySelector("button.btn.wide");
    button.disabled = true;
    button.textContent = form.dataset.busyText;
  });
});

// AI coach chat
const composer = document.getElementById("composer");
if (composer) {
  const chat = document.getElementById("chat");
  const input = document.getElementById("coach-input");
  const sendButton = document.getElementById("coach-send");
  const csrfToken = composer.querySelector("[name=csrfmiddlewaretoken]").value;

  const addBubble = (role, html) => {
    document.getElementById("chat-empty")?.remove();
    const bubble = document.createElement("div");
    bubble.className = `bubble ${role}`;
    bubble.innerHTML = html;
    chat.appendChild(bubble);
    bubble.scrollIntoView({ behavior: "smooth", block: "end" });
    return bubble;
  };

  const escapeHtml = (text) => {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  };

  const send = async () => {
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendButton.disabled = true;
    const userBubble = addBubble("user", `<p>${escapeHtml(text)}</p>`);
    const thinking = addBubble("assistant thinking", "<p>Checking your logs…</p>");

    try {
      const response = await fetch(composer.dataset.url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify({ message: text }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Something went wrong.");
      userBubble.innerHTML = data.user_html;
      thinking.className = "bubble assistant";
      thinking.innerHTML = data.reply_html;
    } catch (error) {
      thinking.className = "bubble error";
      thinking.textContent = error.message;
      userBubble.remove();
      input.value = text;
    } finally {
      sendButton.disabled = false;
      input.focus();
    }
  };

  composer.addEventListener("submit", (event) => {
    event.preventDefault();
    send();
  });

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      send();
    }
  });

  document.querySelectorAll("[data-ask]").forEach((button) => {
    button.addEventListener("click", () => {
      input.value = button.dataset.ask;
      send();
    });
  });

  chat.lastElementChild?.scrollIntoView({ block: "end" });
}

// "Show all" on the strength progress table
document.querySelectorAll("[data-show-all]").forEach((button) => {
  button.addEventListener("click", () => {
    document.getElementById(button.dataset.showAll).classList.add("all");
    button.remove();
  });
});

// Profile report charts, drawn as plain SVG
const chartData = document.getElementById("chart-data");
if (chartData) {
  const data = JSON.parse(chartData.textContent);
  const drawAll = () => {
    document.querySelectorAll("[data-chart]").forEach((el) => {
      const series = data[el.dataset.chart];
      if (el.dataset.kind === "line") drawLineChart(el, series);
      else drawBarChart(el, series);
    });
  };
  drawAll();
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(drawAll, 150);
  });
}

function niceStep(range, count) {
  const raw = range / count;
  const power = Math.pow(10, Math.floor(Math.log10(raw)));
  const unit = [1, 2, 2.5, 5, 10].find((n) => n * power >= raw);
  return unit * power;
}

function formatNumber(value) {
  return value >= 1000 ? `${+(value / 1000).toFixed(1)}K` : `${+value.toFixed(1)}`;
}

// Shared axes, grid and tooltip. Returns helpers to place marks.
function chartFrame(el, series, yMin, yMax) {
  const width = el.clientWidth;
  const height = 200;
  const pad = { top: 16, right: 12, bottom: 24, left: 40 };
  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;
  const step = niceStep(yMax - yMin || 1, 4);
  const low = Math.floor(yMin / step) * step;
  const high = Math.ceil(yMax / step) * step || step;
  const y = (v) => pad.top + plotH - ((v - low) / (high - low)) * plotH;
  const slot = plotW / series.labels.length;
  const x = (i) => pad.left + slot * i + slot / 2;

  let svg = `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" role="img">`;
  for (let v = low; v <= high + step / 2; v += step) {
    svg += `<line class="grid" x1="${pad.left}" x2="${width - pad.right}" y1="${y(v)}" y2="${y(v)}"/>`;
    svg += `<text class="tick" x="${pad.left - 6}" y="${y(v) + 4}" text-anchor="end">${formatNumber(v)}</text>`;
  }
  const maxLabels = Math.max(2, Math.floor(plotW / 52));
  const every = Math.ceil(series.labels.length / maxLabels);
  series.labels.forEach((label, i) => {
    const last = i === series.labels.length - 1;
    if (i % every === 0 || last) {
      if (!last && series.labels.length - 1 - i < every) return;
      svg += `<text class="tick" x="${x(i)}" y="${height - 6}" text-anchor="middle">${label}</text>`;
    }
  });

  el.innerHTML = "";
  el.style.position = "relative";
  const tooltip = document.createElement("div");
  tooltip.className = "chart-tip";
  tooltip.hidden = true;
  const showTip = (i, px, py) => {
    tooltip.innerHTML = `<span>${series.labels[i]}</span><b>${series.values[i]} ${series.unit}</b>`;
    tooltip.hidden = false;
    const left = Math.min(Math.max(px - tooltip.offsetWidth / 2, 0), width - tooltip.offsetWidth);
    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${Math.max(py - tooltip.offsetHeight - 10, 0)}px`;
  };
  const hideTip = () => (tooltip.hidden = true);
  return { svg, x, y, slot, low, pad, width, height, plotH, tooltip, showTip, hideTip };
}

function emptyChart(el) {
  el.innerHTML = '<p class="chart-empty">No data in this period.</p>';
}

function drawBarChart(el, series) {
  const values = series.values.filter((v) => v !== null);
  if (!values.length) return emptyChart(el);
  const top = Math.max(...values, series.target || 0) * 1.08;
  const f = chartFrame(el, series, 0, top);
  const barW = Math.max(2, Math.min(24, f.slot - 2));
  let marks = "";
  series.values.forEach((v, i) => {
    if (v === null || v === 0) return;
    const x0 = f.x(i) - barW / 2;
    const yTop = f.y(v);
    const base = f.y(0);
    const r = Math.min(4, barW / 2, base - yTop);
    marks += `<path class="bar${!series.target || v >= series.target ? " hit" : ""}" data-i="${i}" d="M${x0},${base} V${yTop + r} Q${x0},${yTop} ${x0 + r},${yTop} H${x0 + barW - r} Q${x0 + barW},${yTop} ${x0 + barW},${yTop + r} V${base} Z"/>`;
    marks += `<rect class="hit-area" data-i="${i}" x="${f.x(i) - f.slot / 2}" y="${f.pad.top}" width="${f.slot}" height="${f.plotH}"/>`;
  });
  if (series.target) {
    const ty = f.y(series.target);
    marks += `<line class="target" x1="${f.pad.left}" x2="${f.width - f.pad.right}" y1="${ty}" y2="${ty}"/>`;
    marks += `<text class="target-label" x="${f.width - f.pad.right}" y="${ty - 5}" text-anchor="end">Target ${series.target}</text>`;
  }
  el.innerHTML = f.svg + marks + "</svg>";
  el.appendChild(f.tooltip);
  el.querySelectorAll(".hit-area").forEach((area) => {
    const i = +area.dataset.i;
    area.addEventListener("mouseenter", () => f.showTip(i, f.x(i), f.y(series.values[i])));
    area.addEventListener("click", () => f.showTip(i, f.x(i), f.y(series.values[i])));
    area.addEventListener("mouseleave", f.hideTip);
  });
}

function drawLineChart(el, series) {
  if (!series.values.length) return emptyChart(el);
  const min = Math.min(...series.values);
  const max = Math.max(...series.values);
  const f = chartFrame(el, series, min - 0.5, max + 0.5);
  const points = series.values.map((v, i) => [f.x(i), f.y(v)]);
  const path = points.map(([px, py], i) => `${i ? "L" : "M"}${px},${py}`).join(" ");
  const area = `${path} L${points[points.length - 1][0]},${f.y(f.low)} L${points[0][0]},${f.y(f.low)} Z`;
  const [lastX, lastY] = points[points.length - 1];
  let marks = `<path class="area" d="${area}"/><path class="line" d="${path}"/>`;
  marks += `<line class="crosshair" x1="0" x2="0" y1="${f.pad.top}" y2="${f.pad.top + f.plotH}" visibility="hidden"/>`;
  marks += `<circle class="dot" cx="${lastX}" cy="${lastY}" r="5"/>`;
  marks += `<text class="end-label" x="${lastX - 8}" y="${lastY - 10}" text-anchor="end">${series.values[series.values.length - 1]} kg</text>`;
  marks += `<rect class="hit-area" x="${f.pad.left}" y="${f.pad.top}" width="${f.width - f.pad.left - f.pad.right}" height="${f.plotH}"/>`;
  el.innerHTML = f.svg + marks + "</svg>";
  el.appendChild(f.tooltip);
  const crosshair = el.querySelector(".crosshair");
  const hit = el.querySelector(".hit-area");
  const track = (event) => {
    const box = hit.getBoundingClientRect();
    const px = event.clientX - box.left + f.pad.left;
    const i = Math.max(0, Math.min(series.values.length - 1, Math.round((px - f.pad.left - f.slot / 2) / f.slot)));
    crosshair.setAttribute("x1", f.x(i));
    crosshair.setAttribute("x2", f.x(i));
    crosshair.setAttribute("visibility", "visible");
    f.showTip(i, f.x(i), f.y(series.values[i]));
  };
  hit.addEventListener("mousemove", track);
  hit.addEventListener("click", track);
  hit.addEventListener("mouseleave", () => {
    crosshair.setAttribute("visibility", "hidden");
    f.hideTip();
  });
}
