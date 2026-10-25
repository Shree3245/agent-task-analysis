(function () {
"use strict";
var D = JSON.parse(document.getElementById("report-data").textContent);
var MARGIN = 1 - D.target;

function money(v) {
  if (v == null || !isFinite(v)) return "—";
  if (v >= 100) return "$" + v.toFixed(0);
  if (v >= 0.1) return "$" + v.toFixed(2);
  if (v >= 0.001) return "$" + v.toFixed(3);
  return "$" + v.toPrecision(2);
}
function pct(v) { return v == null || !isFinite(v) ? "—" : Math.round(v * 100) + "%"; }
function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]; }); }
function date(s) {
  if (!s) return "—";
  var d = new Date(s + "T00:00:00Z");
  return d.toLocaleDateString("en-US", {month: "short", day: "numeric", year: "numeric", timeZone: "UTC"});
}
// Validated numbers rescale exactly with price: cost stays fixed, revenue scales.
function expected(g, p) { return 1 - g.loss * g.price / p; }
function conservative(g, p) { return 1 - g.upper * g.price / p; }
function safePrice(g) { return g.upper * g.price / 0.9; }
function over(g, p) { var n = 0; g.costs.forEach(function (c) { if (c > p) n++; }); return g.costs.length ? n / g.costs.length : 0; }
function shown(g) { return g.status === "risky" ? safePrice(g) : g.price; }

function oneLiner(g) {
  if (g.status === "more") return g.reason;
  var c = conservative(g, g.price);
  if (g.status === "risky") return "A few runs cost far more than the rest. At " + money(g.price) + " you could lose money. " + money(safePrice(g)) + " would hold.";
  if (g.status === "watch") return "Holds, keeping at least " + pct(c) + ", but recent runs cost " + pct(Math.abs(g.drift.ratio - 1)) + " " + (g.drift.ratio < 1 ? "less" : "more") + ". Review the price.";
  return "Keeps about " + pct(expected(g, g.price)) + " margin, and at least " + pct(c) + " in a bad stretch.";
}

// ---------- header ----------
var priced = D.groups.filter(function (g) { return g.status === "ready" || g.status === "watch"; }).length;
document.getElementById("d-headline").textContent = D.groups.length
  ? "You can charge a fixed price for " + priced + " of " + D.groups.length + " task type" + (D.groups.length === 1 ? "" : "s") + " today."
  : "No priced runs were found.";
var facts = [
  "<span><b>" + D.n_tasks.toLocaleString() + "</b> runs</span>",
  "<span><b>" + date(D.start) + " – " + date(D.end) + "</b></span>",
  "<span><b>" + money(D.spend) + "</b> model spend</span>",
  "<span>Analyzed on this computer. Nothing was uploaded.</span>"
];
document.getElementById("d-facts").innerHTML = facts.join("");
var notes = [];
if (D.benchmark) notes.push("These are benchmark tasks, not production traffic.");
if (D.repricing === "FAIL") notes.push("Repricing did not match your recorded costs. Check the cost audit below before using these prices.");
if (D.overrides) notes.push("Some prices use rates you supplied, not public list prices.");
document.getElementById("d-notes").innerHTML = notes.map(function (n) { return "<p class=\"d-note\">" + esc(n) + "</p>"; }).join("");
document.getElementById("d-sub").textContent = "Each price is set to keep a " + pct(MARGIN) + " margin after model costs, then tested on runs it never saw. Pick a task type to see why.";

// ---------- rows ----------
var rowsEl = document.getElementById("d-rows");
var first = D.groups.filter(function (g) { return g.status === "ready" || g.status === "watch"; })[0] || D.groups[0];
var selected = first ? first.name : null;
function renderRows() {
  rowsEl.innerHTML = D.groups.map(function (g, i) {
    var price = g.status === "more" ? "—" : money(shown(g));
    var sub = g.status === "more" ? "not enough runs" : g.status === "risky" ? "per run, safer price" : "per run";
    return "<button class=\"d-row\" type=\"button\" role=\"tab\" aria-selected=\"" + (g.name === selected) + "\" data-i=\"" + i + "\">" +
      "<span class=\"d-chip " + g.status + "\">" + esc(g.label) + "</span>" +
      "<span class=\"d-nm\"><span class=\"d-name\">" + esc(g.name) + "</span><br><span class=\"d-runs\">" + g.n.toLocaleString() + " runs</span></span>" +
      "<span class=\"d-price\">" + price + "<small>" + sub + "</small></span>" +
      "<span class=\"d-why\">" + esc(oneLiner(g)) + "</span></button>";
  }).join("");
}
rowsEl.addEventListener("click", function (e) {
  var b = e.target.closest(".d-row"); if (!b) return;
  selected = D.groups[+b.getAttribute("data-i")].name;
  renderRows(); renderDetail();
});

// ---------- detail ----------
var detailEl = document.getElementById("d-detail");
var tryPrice = null;
function cls(v) { return v >= 0.2 ? "good" : v >= 0.1 ? "warn" : "bad"; }
function renderDetail() {
  var g = D.groups.filter(function (x) { return x.name === selected; })[0];
  if (!g) { detailEl.innerHTML = ""; return; }
  var enough = g.status !== "more";
  tryPrice = enough ? shown(g) : null;
  var html = "<div class=\"d-dhead\"><h2>" + esc(g.name) + "</h2><span class=\"d-chip " + g.status + "\">" + esc(g.label) + "</span></div>" +
    (splitLine(g) ? "<p class=\"d-split\">" + esc(splitLine(g)) + "</p>" : "") + "<div class=\"d-grid\"><div class=\"d-panel\">";
  if (enough) {
    var lo = Math.max((g.median || g.price) * 0.5, g.price * 0.4), hi = g.price * 2.6;
    html += "<span class=\"d-label\">Try a price</span>" +
      "<div class=\"d-big\"><span id=\"d-pv\"></span><small> per run</small></div>" +
      "<input type=\"range\" id=\"d-price\" min=\"" + lo + "\" max=\"" + hi + "\" step=\"" + ((hi - lo) / 400) + "\" value=\"" + tryPrice + "\" aria-label=\"Price per run\">" +
      "<div class=\"d-ends\"><span>" + money(lo) + "</span><span>" + money(hi) + "</span></div>" +
      "<p class=\"d-verdict\" id=\"d-vline\"></p>" +
      "<div class=\"d-stats\">" +
      "<div class=\"d-stat\"><span class=\"v\" id=\"d-exp\"></span><span class=\"k\">Expected margin on runs the price never saw</span></div>" +
      "<div class=\"d-stat\"><span class=\"v\" id=\"d-con\"></span><span class=\"k\">Conservative margin, kept in 19 of 20 replays</span></div>" +
      "<div class=\"d-stat\"><span class=\"v\" id=\"d-over\"></span><span class=\"k\">Runs that cost more than the price. The rest cover them.</span></div>" +
      "<div class=\"d-stat\"><span class=\"v\" id=\"d-max\"></span><span class=\"k\">Most expensive run</span></div></div>" +
      "<button class=\"d-reset\" id=\"d-reset\" type=\"button\">Back to recommended " + money(shown(g)) + "</button>";
  } else {
    var mean = g.costs.length ? g.costs.reduce(function (a, b) { return a + b; }, 0) / g.costs.length : null;
    html += "<span class=\"d-label\">Not enough runs yet</span><p class=\"d-verdict\">" + esc(g.reason) + "</p>" +
      (mean ? "<p class=\"d-muted\">The average run so far costs " + money(mean) + ", so a " + pct(MARGIN) + " margin would mean about " + money(mean / D.target) + " per run. That price is untested.</p>" : "");
  }
  html += "</div><div class=\"d-panel\"><span class=\"d-label\">What each run cost</span><div id=\"d-hist\"></div>" +
    "<div class=\"d-legend\"><span><i class=\"lo\"></i>Runs that cost less than the price</span><span><i class=\"hi\"></i>Runs that cost more</span></div>" +
    "<p class=\"d-muted\">Most runs are cheap and a few are expensive. One fixed price works when the cheap runs pay for the expensive ones.</p></div></div>" +
    "<div class=\"d-watch\"><h3>Things to watch</h3>" + watch(g) + "</div>";
  detailEl.innerHTML = html;
  if (enough) {
    var input = document.getElementById("d-price");
    input.addEventListener("input", function () { tryPrice = +input.value; update(g); });
    document.getElementById("d-reset").addEventListener("click", function () { tryPrice = shown(g); input.value = tryPrice; update(g); });
    update(g);
  } else {
    hist(g, null);
  }
}
function splitLine(g) {
  if (g.grouped) return "Tested by holding out whole task groups the price never saw.";
  if (!g.fit_window || !g.test_window || g.n_fit == null) return null;
  return "Price set on " + g.n_fit + " runs from " + date(g.fit_window[0]) + " to " + date(g.fit_window[1]) +
    ", then tested on the " + g.n_test + " newer runs from " + date(g.test_window[0]) + " to " + date(g.test_window[1]) + "." +
    (g.backdated ? " The test started earlier for this task type so it had enough runs." : "");
}
function update(g) {
  var p = tryPrice, e = expected(g, p), c = conservative(g, p);
  document.getElementById("d-pv").textContent = money(p);
  var se = document.getElementById("d-exp"), sc = document.getElementById("d-con");
  se.textContent = pct(e); se.className = "v " + cls(e);
  sc.textContent = pct(c); sc.className = "v " + cls(c);
  document.getElementById("d-over").textContent = pct(over(g, p));
  document.getElementById("d-max").textContent = g.max != null ? money(g.max) + " · " + (g.max / p).toFixed(1) + "× price" : "—";
  var line;
  if (c >= 0.1) line = "<b>Holds.</b> At " + money(p) + " a run you keep about " + pct(e) + ", and at least " + pct(c) + " even in a bad stretch.";
  else if (c >= 0) line = "<b>Thin.</b> You still make money in a bad stretch, but only " + pct(c) + ". " + money(safePrice(g)) + " or more keeps at least 10%.";
  else line = "<b>Could lose money.</b> In a bad stretch these runs cost more than you charge. " + money(safePrice(g)) + " or more keeps at least 10%.";
  document.getElementById("d-vline").innerHTML = line;
  hist(g, p);
}

function hist(g, price) {
  var el = document.getElementById("d-hist");
  var xs = g.costs.filter(function (c) { return c > 0; });
  if (xs.length < 2) { el.innerHTML = "<p class=\"d-muted\">Not enough priced runs to draw.</p>"; return; }
  var W = 640, H = 230, L = 46, R = 14, TOP = 26, BOT = 40, nb = Math.min(26, Math.max(8, Math.round(Math.sqrt(xs.length) * 2)));
  var mn = Math.log(xs[0]), mx = Math.log(xs[xs.length - 1] * 1.02);
  if (mx - mn < 1e-9) mx = mn + 1;
  var bins = []; for (var i = 0; i < nb; i++) bins.push(0);
  xs.forEach(function (c) { var k = Math.floor((Math.log(c) - mn) / (mx - mn) * nb); bins[Math.min(nb - 1, k)]++; });
  var top = Math.max.apply(null, bins), bw = (W - L - R) / nb;
  function X(v) { return L + (Math.log(v) - mn) / (mx - mn) * (W - L - R); }
  var s = "<svg viewBox=\"0 0 " + W + " " + H + "\" role=\"img\" aria-label=\"Run costs for " + esc(g.name) + "\">";
  s += "<line class=\"base\" x1=\"" + L + "\" y1=\"" + (H - BOT) + "\" x2=\"" + (W - R) + "\" y2=\"" + (H - BOT) + "\"/>";
  bins.forEach(function (n, k) {
    if (!n) return;
    var h = Math.max(2, n / top * (H - BOT - TOP)), x = L + k * bw + 1, low = Math.exp(mn + k / nb * (mx - mn));
    s += "<rect class=\"bar" + (price != null && low >= price ? " over" : "") + "\" x=\"" + x.toFixed(1) + "\" y=\"" + (H - BOT - h).toFixed(1) + "\" width=\"" + Math.max(1, bw - 2).toFixed(1) + "\" height=\"" + h.toFixed(1) + "\"><title>" + n + " runs</title></rect>";
  });
  s += "<text class=\"axis\" x=\"" + (L - 8) + "\" y=\"" + (TOP + 4) + "\" text-anchor=\"end\">" + top + "</text><text class=\"axis\" x=\"" + (L - 8) + "\" y=\"" + (H - BOT) + "\" text-anchor=\"end\">0</text>";
  [0, 1 / 3, 2 / 3, 1].forEach(function (f, k) {
    s += "<text class=\"axis\" x=\"" + X(Math.exp(mn + f * (mx - mn))).toFixed(1) + "\" y=\"" + (H - BOT + 18) + "\" text-anchor=\"" + (k === 0 ? "start" : k === 3 ? "end" : "middle") + "\">" + money(Math.exp(mn + f * (mx - mn))) + "</text>";
  });
  s += "<text class=\"axis\" x=\"" + L + "\" y=\"" + (H - 6) + "\">cost per run, log scale</text>";
  if (price != null && price > xs[0] && price < xs[xs.length - 1] * 1.02) {
    var px = X(price), end = px > W - 120;
    s += "<line class=\"pline\" x1=\"" + px.toFixed(1) + "\" y1=\"" + (TOP - 6) + "\" x2=\"" + px.toFixed(1) + "\" y2=\"" + (H - BOT) + "\"/>";
    s += "<text class=\"plabel\" x=\"" + (px + (end ? -6 : 6)).toFixed(1) + "\" y=\"" + (TOP + 6) + "\" text-anchor=\"" + (end ? "end" : "start") + "\">price " + money(price) + "</text>";
  }
  el.innerHTML = s + "</svg>";
}

function item(kind, title, body) {
  return "<div class=\"d-item " + kind + "\"><span class=\"stripe\"></span><div><b>" + esc(title) + "</b><p>" + esc(body) + "</p></div></div>";
}
function watch(g) {
  var out = [], enough = g.status !== "more", p = enough ? shown(g) : null;
  if (g.drift.ratio != null && g.drift.moved) {
    var down = g.drift.ratio < 1, np = g.drift.recent_mean / D.target;
    out.push(item("warn", "Costs " + (down ? "fell " : "rose ") + pct(Math.abs(g.drift.ratio - 1)) + " in the last 30 days",
      "Recent runs average " + money(g.drift.recent_mean) + ", against " + money(g.drift.fit_mean) + " for the runs the price was set on. " +
      (down ? "You could lower the price to about " + money(np) + ", or keep it and earn more." : "Raise the price to about " + money(np) + " to keep a " + pct(MARGIN) + " margin.")));
  } else if (g.drift.ratio != null && g.drift.small && Math.abs(g.drift.ratio - 1) > 0.25) {
    out.push(item("info", "Recent costs look " + (g.drift.ratio < 1 ? "lower" : "higher") + ", on few runs",
      "The last 30 days average " + money(g.drift.recent_mean) + " over " + g.drift.recent_n + " runs. Too few to act on yet."));
  }
  if (enough && g.max != null && g.max > 3 * p) {
    out.push(item("info", "Your most expensive run cost " + money(g.max) + ", " + (g.max / p).toFixed(0) + "× the price",
      (g.cap ? "Stopping runs at " + money(g.cap.price) + " would affect about " + pct(g.cap.stopped) + " of runs and limit what one run can cost you. " : "") + "The price above already covers runs like this without a cap."));
  }
  if (enough && g.rate) {
    var c0 = conservative(g, p), c1 = 1 - g.upper * (1 + g.rate.change) * g.price / p;
    out.push(item(c1 < 0.1 ? "bad" : "info", "A model price change on " + date(g.rate.date) + " changes cost by " + (g.rate.change > 0 ? "+" : "") + pct(g.rate.change),
      "Models: " + g.rate.models.join(", ") + ". At " + money(p) + " the conservative margin goes from " + pct(c0) + " to " + pct(c1) + "."));
  }
  if (enough && g.success) {
    var basis = g.success.basis === "resolved" ? "resolved task" : "confirmed success";
    out.push(item("good", "Charging only for successful runs: " + money(g.success.price) + " per " + basis,
      (g.success_share != null ? pct(g.success_share) + " of runs are " + (g.success.basis === "resolved" ? "resolved" : "confirmed successes") + ". " : "") +
      "Customers pay nothing for the others, and this price covers them" + (g.success.target ? " at a " + pct(1 - g.success.target) + " margin." : ".") +
      (g.success.upper != null && g.success.upper >= 0.9 ? " It does not pass the conservative test yet." : "")));
  }
  if (g.status === "risky" && g.risk_reasons.length) {
    out.push(item("bad", "Why this price did not pass", g.risk_reasons.join("; ") + "."));
  }
  if (g.n_unpriced) out.push(item("warn", g.n_unpriced + " runs have unknown costs", "They used a model without a known price, so they are left out of these numbers."));
  if (g.override_share) out.push(item("info", "Rates you supplied price " + pct(g.override_share) + " of this spend", "Those are not public list prices."));
  if (!out.length) out.push(item("good", "Nothing to flag", "Costs are steady and no single run stands out."));
  return out.join("");
}

renderRows();
renderDetail();
})();
