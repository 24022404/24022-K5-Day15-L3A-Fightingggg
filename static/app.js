"use strict";
/* Lớp học AI20K · giao diện kiểu Canvas. Không dùng framework; dữ liệu bài lấy từ /api/lesson, hỏi đáp qua /api/ask. */
const COURSE = "Nền tảng LLM (Day 1)", MAX_Q = 15, KEY = "ai20k-lms-v1";
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const ICON = {
  account: "<circle cx='12' cy='8' r='4'/><path d='M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8'/>",
  dash: "<path d='M3 17a9 9 0 1 1 18 0'/><path d='M12 17l4-5'/><circle cx='12' cy='17' r='1.2'/>",
  courses: "<path d='M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z'/><path d='M5 17a3 3 0 0 1 3-3h11'/><path d='M9 8h6'/>",
  inbox: "<path d='M3 13l3-8h12l3 8v6H3z'/><path d='M3 13h5l1 3h6l1-3h5'/>",
  help: "<circle cx='12' cy='12' r='9'/><path d='M9.5 9.5a2.5 2.5 0 1 1 4 2c-1 .7-1.5 1.2-1.5 2.5'/><path d='M12 17.5v.01'/>",
  page: "<path d='M6 3h8l4 4v14H6z'/><path d='M14 3v4h4'/><path d='M9 12h6M9 16h6'/>",
  send: "<path d='M4 12l16-8-6 16-3-7z'/>",
  chat: "<path d='M4 5h16v11H9l-5 4z'/>",
  menu: "<path d='M4 6h16M4 12h16M4 18h16'/>",
  caret: "<path d='M6 9l6 6 6-6'/>",
  check: "<circle cx='12' cy='12' r='9'/><path d='M8 12l3 3 5-6'/>",
  trash: "<path d='M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13'/>",
  mega: "<path d='M4 10v4h3l7 4V6L7 10z'/><path d='M17 9a4 4 0 0 1 0 6'/>",
  tok: "<rect x='4' y='4' width='7' height='7'/><rect x='13' y='4' width='7' height='7'/><rect x='4' y='13' width='7' height='7'/><path d='M13 16.5h7M16.5 13v7'/>",
  tune: "<path d='M5 7h8M17 7h2M5 17h2M11 17h8'/><circle cx='15' cy='7' r='2'/><circle cx='9' cy='17' r='2'/>",
  rag: "<path d='M5 4h9l4 4v12H5z'/><circle cx='11' cy='13' r='3'/><path d='M13.2 15.2L16 18'/>",
  ext: "<path d='M14 4h6v6M20 4l-9 9M18 14v6H4V6h6'/>",
};
/* dấu hiệu của sản phẩm: quyển sách mở có góc gấp và một tia sáng (chỗ được trích) */
const brand = (px = 36, dark = 0) => `<svg class="brand" width="${px}" height="${px}" viewBox="0 0 40 40" aria-hidden="true"><path d="M0 0H29L40 11V40H0Z" fill="${dark ? "#2a4fb0" : "#0c1a4b"}"/><path d="M29 0L40 11H29Z" fill="#9fc0f5"/><path d="M7 30V17c5-2 9-1 13 2v13c-4-3-8-4-13-2z" fill="#fff"/><path d="M33 30V17c-5-2-9-1-13 2v13c4-3 8-4 13-2z" fill="#9fc0f5"/><path d="M19 4l1.8 4.7L25.5 10.5l-4.7 1.8L19 17l-1.8-4.7L12.5 10.5l4.7-1.8z" fill="#ffd23f"/></svg>`;
const ic = (n, cls = "") => `<svg class="i ${cls}" viewBox="0 0 24 24">${ICON[n]}</svg>`;

/* ---------- trạng thái (lưu trong trình duyệt này) */
let S = { user: null, loginAt: null, done: [], msgs: [], n: 0, quiz: {} };
try { Object.assign(S, JSON.parse(localStorage.getItem(KEY) || "{}")); } catch (e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };
let P = [], QZ = [], QA = {}, curChips = null;            // các đoạn bài
let busy = false, cnavHide = window.innerWidth < 760, pendAsk = null;

const initials = n => { const w = n.trim().split(/\s+/).filter(Boolean); return (w.length > 1 ? w[0][0] + w[w.length - 1][0] : (w[0] || "?").slice(0, 2)).toUpperCase(); };
const toast = t => { const d = document.createElement("div"); d.className = "toast"; d.textContent = t; $("#toasts").appendChild(d); setTimeout(() => d.remove(), 3200); };
const bar = (w, hold) => { const b = $("#topbar"); b.style.opacity = 1; b.style.width = w + "%"; if (!hold) setTimeout(() => { b.style.width = "100%"; setTimeout(() => { b.style.opacity = 0; b.style.width = "0"; }, 250); }, 120); };

/* ---------- đăng nhập */
function renderLogin() {
  $("#app").innerHTML = `<div class="login" data-ghost="p01 p02 p03"><div class="pitch"><div class="brandline">${brand(42)}<span>Lớp học AI20K</span></div>
    <h1>Học Nền tảng LLM, hỏi trợ giảng ngay trên trang bài.</h1>
    <p><b>Mỗi câu trả lời kèm mã đoạn.</b> Bấm vào là thấy đúng đoạn trong bài, để bạn tự kiểm lại.</p>
    <p><b>Bài không nói thì trợ giảng nói là không có,</b> thay vì đoán.</p>
    <p><b>Không làm hộ bài nộp</b> và không đưa đáp án quiz.</p></div>
    <div class="wrap"><div class="box fold"><h2>Đăng nhập</h2><p class="sub">Khoá 5 · Nền tảng LLM · Day 1</p>
    <form id="lf" autocomplete="off">
      <label class="field"><span>Tên đăng nhập</span><input id="lu" autocomplete="username" required></label>
      <label class="field"><span>Mật khẩu</span><input id="lp" type="password" autocomplete="current-password" required></label>
      <div class="err" id="lerr" role="alert"></div>
      <button class="btn pri full" type="submit">Đăng nhập</button>
      <button class="btn ghost full" type="button" id="guest">Vào với tư cách khách</button>
    </form>
    <div class="hint"><b>Tài khoản dùng thử</b><br>Tên đăng nhập: <code>hocvien</code> · Mật khẩu: <code>ai20k2026</code></div></div>
    <div class="note">Sản phẩm của nhóm Fightingggg (Hackathon AI Day 15, track A). Tài khoản chung cho mọi người dùng thử, không có dữ liệu cá nhân thật. Tiến độ và lịch sử chat chỉ lưu trong trình duyệt này.</div></div></div>`;
  const enter = (name, id) => { S.user = { name, id, email: "" }; S.loginAt = new Date().toLocaleString("vi-VN"); save(); location.hash = "#/home"; boot(); };
  $("#lf").onsubmit = async ev => {
    ev.preventDefault(); const u = $("#lu").value.trim(), pw = $("#lp").value, er = $("#lerr"); er.textContent = "";
    try {
      const r = await fetch("/api/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username: u, password: pw }) });
      const j = await r.json(); if (!r.ok) { er.textContent = j.error || "Đăng nhập thất bại."; return; }
      enter(u === "hocvien" ? "Học viên" : u, u);
    } catch (e) { er.textContent = "Không kết nối được máy chủ."; }
  };
  $("#guest").onclick = () => enter("Khách", "guest");
  $("#lu").focus();
}
const logout = () => { S = { user: null, loginAt: null, done: [], msgs: [], n: 0, quiz: {} }; QA = {}; save(); location.hash = ""; boot(); };

/* ---------- khung chung */
const NAV = [["home", "Trang chủ"], ["announcements", "Thông báo"], ["assignments", "Bài tập"], ["grades", "Điểm số"], ["people", "Thành viên"], ["files", "Tệp"], ["syllabus", "Đề cương"], ["modules", "Học phần"]];
const GNAV = [["account", "Tài khoản"], ["dash", "Tổng quan"], ["courses", "Khoá học"], ["inbox", "Hộp thư"], ["help", "Trợ giúp"]];

function shell() {
  $("#app").innerHTML = `<div class="shell">
    <nav class="gnav" aria-label="Điều hướng chung"><div class="logo">${brand(42, 1)}</div>
      ${GNAV.map(([k, l]) => `<button data-g="${k}">${ic(k)}<span>${l}</span>${k === "inbox" ? '<span class="badge">2</span>' : ""}</button>`).join("")}</nav>
    <div class="scrim" id="scrim"></div><aside class="tray" id="tray"></aside>
    <nav class="cnav ${cnavHide ? "hide" : ""}" id="cnav" aria-label="Điều hướng khoá học"><div class="term">AI20K · Khoá 5 · Day 1</div>
      ${NAV.map(([k, l]) => `<a href="#/${k}" data-c="${k}">${l}</a>`).join("")}
      <div class="me"><b>${esc(S.user.name)}</b><a href="#" id="lo">Đăng xuất</a></div></nav>
    <div class="main"><div class="head"><button class="burger" id="burger" aria-label="Ẩn hiện menu khoá học">${ic("menu")}</button><div class="crumb" id="crumb"></div><div class="grow"></div></div>
      <div id="stage" style="flex:1;min-height:0;display:flex"></div></div>
    <aside class="msgr" id="msgr" aria-label="Trợ giảng"></aside><button class="fab" id="fab">${ic("chat")} Trợ giảng</button></div>`;
  $("#lo").onclick = e => { e.preventDefault(); logout(); };
  $("#burger").onclick = () => { cnavHide = !cnavHide; $("#cnav").classList.toggle("hide", cnavHide); };
  $("#scrim").onclick = closeTray;
  document.querySelectorAll("[data-g]").forEach(b => b.onclick = () => gclick(b.dataset.g));
  $("#fab").onclick = () => $("#msgr").classList.toggle("open");
}
let trayKey = null;
function closeTray() { trayKey = null; $("#tray").classList.remove("open"); $("#scrim").classList.remove("on"); }
function openTray(html) { $("#tray").innerHTML = `<button class="x" aria-label="Đóng">✕</button>` + html; $("#tray").classList.add("open"); $("#scrim").classList.add("on"); $("#tray .x").onclick = closeTray; $("#tray").querySelectorAll("[data-go]").forEach(a => a.onclick = e => { e.preventDefault(); closeTray(); location.hash = "#/" + a.dataset.go; }); const lo = $("#tray #tlo"); if (lo) lo.onclick = logout; }
function gclick(k) {
  if ((k === "account" || k === "courses") && trayKey === k && $("#tray").classList.contains("open")) return closeTray();
  if (k === "account") return (trayKey = k, openTray)(`<h2>Tài khoản</h2><div class="who"><span class="avatar">${initials(S.user.name)}</span><b>${esc(S.user.name)}</b></div>
    <ul><li><button data-go="account">Hồ sơ</button></li><li><button data-go="grades">Điểm và tiến độ</button></li><li><button id="tlo">Đăng xuất</button></li></ul>`);
  if (k === "courses") return (trayKey = k, openTray)(`<h2>Khoá học</h2><ul><li><a href="#" data-go="home"><b>${COURSE}</b><br><small style="color:#6b7780">AI20K · Khoá 5</small></a></li></ul><p style="margin-top:1rem"><a href="#" data-go="courses">Tất cả khoá học</a></p>`);
  closeTray(); location.hash = "#/" + k;
}

/* ---------- định tuyến */
const route = () => { const h = (location.hash || "#/home").slice(2).split("/"); return { page: h[0] || "home", arg: h[1] }; };
const crumbs = (...a) => a.map((x, i) => i < a.length - 1 ? `<a href="${x[1]}">${x[0]}</a><span class="sep"> › </span>` : `<span>${x[0]}</span>`).join("");
const done = c => S.done.includes(c);
const doneN = () => P.filter(p => done(p.code)).length;
const ann = (t, d) => `<div class="ann"><span class="ico">${ic("mega")}</span><div><h3>${t}</h3><p>${d}</p></div><div class="d">Đăng ngày<br>27/11/2026</div></div>`;
const ANNS = [["Day 1 đã mở: Nền tảng LLM", "Bài đọc trước giờ lên lớp gồm nhiều trang chia theo module. Vào mục Học phần, mở từng trang; bên phải mỗi trang có khung hỏi đáp để bạn hỏi ngay chỗ chưa hiểu."],
  ["Về bài mẫu và độ tin cậy", "Trang 1 đến 8 do nhóm Fightingggg tự viết. Trang 9 trở đi do nhóm viết lại bằng lời của mình từ sách mở Foundations of Large Language Models (CC BY-NC 4.0) và bài khảo sát A Survey of LLMs, có ghi nguồn từng trang. Đây không phải tài liệu chính thức của khoá."]];
const srcOf = t => { const m = t.match(/\(Nguồn:\s*([^)]*)\)\.?\s*$/); return m ? m[1].replace(/\.$/, "") : ""; };
const bodyOf = t => t.replace(/\s*\(Nguồn:[^)]*\)\.?\s*$/, "");
const sentences = t => bodyOf(t).split(/(?<=[.!?])\s+/).filter(Boolean);
const sideBox = () => {
  const qleft = QZ.filter(q => !S.quiz[q.id]).length;
  return `<aside class="next"><h4>Tiến độ</h4><p class="sum">${doneN()}/${P.length} trang hoàn thành${QZ.length ? " · " + (QZ.length - qleft) + "/" + QZ.length + " bài trắc nghiệm" : ""}</p>${qleft ? `<p><a href="#/assignments">Còn ${qleft} bài trắc nghiệm chưa làm</a></p>` : "<p>Bạn đã làm hết các bài trắc nghiệm.</p>"}</aside>`;
};

const TRY_Q = ["Token là gì và vì sao nó ảnh hưởng chi phí?", "Fine-tuning khác RAG ở điểm nào?", "Cho tôi đáp án quiz cuối bài."];
function heroHTML() {
  const total = P.length, d = doneN();
  const ni = Math.max(0, P.findIndex(p => !done(p.code))), nx = P[ni] || P[0], all = d >= total;
  const strip = P.map((p, i) => `<a class="${done(p.code) ? "dn" : (!all && i === ni ? "nx" : "")}" href="#/lesson/${i}" title="${p.code} · ${esc(p.title)}" style="--i:${i}">${String(i + 1).padStart(2, "0")}</a>`).join("");
  return `<section class="hero"><div class="hl"><div class="kick">AI20K · Khoá 5 · Day 1</div><h2>Nền tảng LLM</h2>
    <p>${total} trang bài đọc, ${QZ.length} bài trắc nghiệm và trợ giảng AI trả lời kèm mã đoạn.</p>
    <div class="idx" aria-label="Các trang bài">${strip}</div><div class="cap">${d}/${total} trang đã hoàn thành</div>
    <div class="acts"><a class="btn amber" href="#/lesson/${all ? 0 : ni}">${all ? "Ôn lại từ đầu" : (d ? "Học tiếp" : "Bắt đầu học") + ": " + esc(String(ni + 1).padStart(2, "0") + " · " + (nx ? nx.title : ""))}</a></div></div></section>`;
}
const tryHTML = () => `<div class="try"><b>Thử hỏi trợ giảng</b><div class="tqs">${TRY_Q.map(q => `<button class="tq" data-try="${esc(q)}">${esc(q)}</button>`).join("")}</div></div>`;
const MODS = {1: "Học phần 1 · Nền tảng LLM", 2: "Học phần 2 · Huấn luyện và căn chỉnh", 3: "Học phần 3 · Prompt, RAG và giải mã"};
const MGLYPH = {1: "tok", 2: "tune", 3: "rag"};
let shutMods = {};
let shutInit = false;
function modulesHTML() {
  const mods = [...new Set(P.map(p => p.module || 1))];
  if (!shutInit && P.length) { const cur = (P[Math.max(0, P.findIndex(p => !done(p.code)))] || {}).module || 1; mods.forEach(m => { shutMods[m] = m !== cur; }); shutInit = true; }
  const all = mods.length && mods.every(m => shutMods[m]);
  return `<div class="modbar"><button class="btn" id="col">${all ? "Mở rộng tất cả" : "Thu gọn tất cả"}</button></div>` +
  mods.map(m => { const ps = P.filter(p => (p.module || 1) === m), dn = ps.filter(p => done(p.code)).length;
    return `<div class="mod ${shutMods[m] ? "shut" : ""}" data-m="${m}"><div class="mh" data-m="${m}" role="button" tabindex="0" aria-expanded="${!shutMods[m]}"><span class="g">${ic(MGLYPH[m] || "page")}</span><span class="mt"><b>${MODS[m] || "Học phần " + m}</b><small>${ps.length} trang · ${dn} đã hoàn thành</small></span><span class="car">${ic("caret")}</span></div><div class="items">
  ${P.map((p, i) => (p.module || 1) === m ? `<a class="mi ${done(p.code) ? "is-dn" : ""}" href="#/lesson/${i}"><span class="cd">${p.code}</span><span class="t">${esc(p.title)}</span>${done(p.code) ? `<span class="ok">${ic("check")} Đã hoàn thành</span>` : `<span class="c">Chưa đọc</span>`}</a>` : "").join("")}</div></div>`; }).join("");
}
function bindTry() { document.querySelectorAll("[data-try]").forEach(b => b.onclick = () => { pendAsk = b.dataset.try; location.hash = "#/lesson/0"; }); }
function bindModules() {
  bindTry();
  const c = $("#col"); if (!c) return;
  const mods = [...new Set(P.map(p => p.module || 1))];
  const sync = () => { const all = mods.every(m => shutMods[m]); c.textContent = all ? "Mở rộng tất cả" : "Thu gọn tất cả"; };
  c.onclick = () => { const all = mods.every(m => shutMods[m]); mods.forEach(m => { shutMods[m] = !all; const el = document.querySelector('.mod[data-m="' + m + '"]'); if (el) el.classList.toggle("shut", !all); }); sync(); };
  document.querySelectorAll(".mh").forEach(h => h.onclick = () => { const m = h.dataset.m; shutMods[m] = !shutMods[m]; h.parentElement.classList.toggle("shut", shutMods[m]); h.setAttribute("aria-expanded", !shutMods[m]); sync(); });
  sync();
}

const PAGES = {
  home: () => ({ crumb: crumbs([COURSE, "#/home"]), html: `${heroHTML()}<div class="home1">${tryHTML()}<div class="sechd"><h2>Thông báo gần đây</h2></div>${ann(...ANNS[0])}<div class="sechd"><h2>Các học phần</h2></div>${modulesHTML()}</div>`, after: bindModules }),
  announcements: () => ({ crumb: crumbs([COURSE, "#/home"], ["Thông báo"]), html: `<h1 class="pt">Thông báo</h1>${ANNS.map(a => ann(...a)).join("")}` }),
  assignments: () => ({ crumb: crumbs([COURSE, "#/home"], ["Bài tập"]), html: `<h1 class="pt">Bài tập</h1>
    <p style="color:#6b7780">Ba bài trắc nghiệm, mỗi bài có thể làm lại. Điểm được chấm ở máy chủ. Trợ giảng AI ở bên phải giải thích khái niệm nhưng không đưa đáp án.</p>
    <table class="tb"><tr><th>Bài</th><th>Số câu</th><th>Trạng thái</th><th>Điểm</th><th></th></tr>${QZ.map(q => { const r = S.quiz[q.id]; return `<tr><td><a href="#/quiz/${q.id}">${esc(q.title)}</a><br><small style="color:#6b7780">${esc(q.desc)}</small></td><td>${q.questions.length}</td><td>${r ? "Đã nộp" : "Chưa làm"}</td><td>${r ? r.score + "/" + r.total : "-"}</td><td><a class="btn ${r ? "" : "pri"}" href="#/quiz/${q.id}" style="text-decoration:none;display:inline-block">${r ? "Xem lại" : "Làm bài"}</a></td></tr>`; }).join("")}</table>` }),
  grades: () => ({ crumb: crumbs([COURSE, "#/home"], ["Điểm số"]), html: `<h1 class="pt">Điểm số: tiến độ của bạn</h1><div class="stat"><div><b>${doneN()}/${P.length}</b>Trang đã hoàn thành</div><div><b>${P.length - doneN()}</b>Còn lại</div></div>
    <h3>Bài trắc nghiệm</h3><table class="tb"><tr><th>Bài</th><th>Điểm</th></tr>${QZ.map(q => `<tr><td>${esc(q.title)}</td><td>${S.quiz[q.id] ? S.quiz[q.id].score + "/" + S.quiz[q.id].total : "Chưa làm"}</td></tr>`).join("")}</table><h3 style="margin-top:1.4rem">Trang bài đã đọc</h3><table class="tb"><tr><th>Trang</th><th>Mã đoạn</th><th>Trạng thái</th></tr>${P.map(p => `<tr><td>${esc(p.title)}</td><td>${p.code}</td><td>${done(p.code) ? "Đã hoàn thành" : "Chưa"}</td></tr>`).join("")}</table><p class="src">Tiến độ lưu trong trình duyệt này.</p>` }),
  people: () => ({ crumb: crumbs([COURSE, "#/home"], ["Thành viên"]), html: `<h1 class="pt">Thành viên</h1><h3>Học viên</h3><table class="tb"><tr><th>Tên</th><th>Vai trò</th><th>Tên đăng nhập</th></tr><tr><td><span class="avatar sm">${initials(S.user.name)}</span> ${esc(S.user.name)}</td><td>Học viên (bạn)</td><td>${esc(S.user.id || "-")}</td></tr></table>
    <h3 style="margin-top:1.6rem">Nhóm phát triển bản demo (Fightingggg · Hackathon AI Day 15 · Track A)</h3><table class="tb"><tr><th>Thành viên</th><th>Phụ trách</th></tr>
    <tr><td><span class="avatar sm">M</span> Minh</td><td>Prototype, bộ khung chạy thử, spec</td></tr><tr><td><span class="avatar sm">S</span> Sang</td><td>Số liệu pain, bằng chứng</td></tr><tr><td><span class="avatar sm">P</span> Phương</td><td>Phỏng vấn, canvas, slide</td></tr><tr><td><span class="avatar sm">L</span> Long</td><td>Bài mẫu, bộ câu thử, thẻ dữ liệu</td></tr></table><p class="src">Giảng viên và TA chưa có trong bản demo.</p>` }),
  files: () => ({ crumb: crumbs([COURSE, "#/home"], ["Tệp"]), html: `<h1 class="pt">Tệp</h1><table class="tb"><tr><th>Tên</th><th>Mô tả</th><th></th></tr>
    <tr><td>lesson_sample.md</td><td>Nội dung chính các trang bài (p01 đến p21), kèm ghi chú nguồn</td><td><a href="/files/lesson_sample.md">Tải về</a></td></tr>
    <tr><td>DATA_CARD.md</td><td>Thẻ dữ liệu: nguồn gốc và giới hạn dữ liệu của bản demo</td><td><a href="/files/DATA_CARD.md">Tải về</a></td></tr></table>` }),
  syllabus: () => ({ crumb: crumbs([COURSE, "#/home"], ["Đề cương"]), html: `<h1 class="pt">Đề cương: Day 1 · Nền tảng LLM</h1><p>Bài đọc gồm 3 module. Mỗi trang có nội dung chính, một ví dụ và các liên kết đọc thêm.</p>
    <table class="tb"><tr><th>Mã</th><th>Trang</th><th>Ý chính</th></tr>${P.map(p => `<tr><td>${p.code}</td><td>${esc(p.title)}</td><td>${esc(sentences(p.text)[0])}</td></tr>`).join("")}</table>` }),
  modules: () => ({ crumb: crumbs([COURSE, "#/home"], ["Học phần"]), html: `<h1 class="pt">Học phần</h1><div class="cols"><div class="l">${modulesHTML()}</div><div class="r">${sideBox()}</div></div>`, after: bindModules }),
  dash: () => ({ crumb: crumbs(["Dashboard"]), html: `<h1 class="pt">Dashboard</h1><p>Xin chào ${esc(S.user.name)}.</p><div class="grid"><div class="card fold" onclick="location.hash='#/home'"><div class="top">AI20K · Khoá 5</div><div class="bd"><b>${COURSE}</b><span>Tiến độ ${doneN()}/${P.length} trang · ${Object.keys(S.quiz).length}/${QZ.length} bài trắc nghiệm</span></div><div class="ft">${P.length} trang bài đọc · 3 học phần</div></div></div>
    <div class="sechd"><h2>Thông báo gần đây</h2></div>${ann(...ANNS[0])}`, flat: 1 }),
  courses: () => ({ crumb: crumbs(["Tất cả khoá học"]), html: `<h1 class="pt">Tất cả khoá học</h1><table class="tb"><tr><th>Khoá</th><th>Học kỳ</th><th>Vai trò</th></tr><tr><td><a href="#/home">${COURSE}</a></td><td>AI20K · Khoá 5</td><td>Học viên</td></tr></table>`, flat: 1 }),
  inbox: () => ({ crumb: crumbs(["Hộp thư"]), html: `<h1 class="pt">Hộp thư</h1><table class="tb"><tr><th>Từ</th><th>Chủ đề</th><th>Ngày</th></tr><tr><td>Ban tổ chức khoá</td><td>Chào mừng bạn đến với Day 1</td><td>27/11/2026</td></tr><tr><td>Hệ thống</td><td>Bài đọc mới: Nền tảng LLM</td><td>27/11/2026</td></tr></table><p class="src">Thư mẫu cho bản demo.</p>`, flat: 1 }),
  help: () => ({ crumb: crumbs(["Trợ giúp"]), html: `<h1 class="pt">Trợ giúp</h1>
    <details class="q"><summary>Trợ giảng trả lời dựa vào đâu?</summary><div>Chỉ dựa vào nội dung chính của các trang bài, và luôn ghi mã đoạn (ví dụ p02, p15) để bạn mở ra kiểm tra.</div></details>
    <details class="q"><summary>Trợ giảng không trả lời được thì sao?</summary><div>Nếu bài không có thông tin, trợ giảng nói rõ "không có trong bài" thay vì đoán. Yêu cầu làm hộ bài nộp bị từ chối.</div></details>
    <details class="q"><summary>Dữ liệu của tôi được lưu ở đâu?</summary><div>Tên, tiến độ và lịch sử chat chỉ lưu trong trình duyệt của bạn. Câu hỏi gửi tới máy chủ chỉ để lấy câu trả lời.</div></details>
    <details class="q"><summary>Giới hạn số câu hỏi?</summary><div>${MAX_Q} câu mỗi phiên để giữ hạn mức miễn phí. Bấm biểu tượng thùng rác trong khung trợ giảng để bắt đầu phiên mới.</div></details>`, flat: 1 }),
  account: () => ({ crumb: crumbs(["Tài khoản"]), html: `<h1 class="pt">Tài khoản</h1><div style="display:flex;gap:2rem;align-items:flex-start"><span class="avatar lg">${initials(S.user.name)}</span><div style="flex:1"><dl class="dl"><dt>Họ và tên</dt><dd>${esc(S.user.name)}</dd><dt>Tên đăng nhập</dt><dd>${esc(S.user.id || "-")}</dd><dt>Vai trò</dt><dd>Học viên</dd><dt>Khoá đang học</dt><dd>${COURSE}</dd><dt>Đăng nhập lúc</dt><dd>${esc(S.loginAt || "")}</dd><dt>Tiến độ</dt><dd>${doneN()}/${P.length} trang</dd></dl>
    <label class="field" style="max-width:360px"><span>Đổi tên hiển thị</span><input id="rn" value="${esc(S.user.name)}"></label><button class="btn pri" id="sv">Lưu tên</button> <button class="btn" id="lo2">Đăng xuất</button></div></div>`, flat: 1,
    after: () => { $("#sv").onclick = () => { const v = $("#rn").value.trim(); if (v) { S.user.name = v; save(); toast("Đã lưu tên"); shell(); render(); } }; $("#lo2").onclick = logout; } }),
};

function lessonPage(i) {
  const p = P[i]; if (!p) { location.hash = "#/modules"; return null; }
  const cited = (S.msgs.length ? S.msgs[S.msgs.length - 1].codes : []).includes(p.code);
  return { crumb: crumbs([COURSE, "#/home"], ["Trang bài", "#/modules"], [String(i + 1).padStart(2, "0") + " · " + esc(p.title)]), lesson: 1, i,
    chips: ['Giải thích "' + p.title + '" giúp tôi.', "Viết hộ tôi bài nộp tuần này.", "Token là gì và vì sao nó ảnh hưởng chi phí?"],
    html: `<div class="lh"><h1>${esc(p.title)}</h1><button class="btn ${done(p.code) ? "" : "pri"}" id="dn">${done(p.code) ? "✓ Đã hoàn thành" : "Đánh dấu hoàn thành"}</button></div>
    <div class="page fold" id="pg"><div class="meta2"><span class="code">${p.code}</span><span>${MODS[p.module || 1] || ""} · Trang ${i + 1}/${P.length}</span>${cited ? '<span class="tag">đoạn được trích</span>' : ""}</div><ul>${sentences(p.text).map(s => `<li>${esc(s)}</li>`).join("")}</ul>
    <div class="ex"><b>Ví dụ.</b> ${esc(p.example || "")}</div><div class="more"><b>Đọc thêm</b><ul>${(p.links || []).map(l => `<li><a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.title)} ${ic("ext")}</a></li>`).join("")}</ul></div>
    <div class="src">${srcOf(p.text) ? "Nguồn: " + esc(srcOf(p.text)) + ". " : ""}${(p.module || 1) === 1 ? "Nội dung chính do nhóm viết (data/lesson_sample.md)." : "Nội dung chính do nhóm viết lại từ sách mở Foundations of LLMs (Xiao và Zhu, CC BY-NC 4.0), xem mục nguồn trong đoạn."} Ví dụ do nhóm viết. Liên kết là nguồn công khai trên web, tìm ngày 27/11/2026; khung hỏi đáp chỉ dựa vào nội dung chính.</div></div>
    <div class="pn"><button class="btn" id="pv" ${i === 0 ? "disabled" : ""}><small>‹ Trang trước</small><b>${i ? esc(P[i - 1].title) : ""}</b></button><button class="btn" id="nx" ${i >= P.length - 1 ? "disabled" : ""}><small>Trang sau ›</small><b>${P[i + 1] ? esc(P[i + 1].title) : ""}</b></button></div>`,
    after: () => { $("#dn").onclick = () => { S.done = done(p.code) ? S.done.filter(c => c !== p.code) : [...S.done, p.code]; save(); render(); };
      $("#pv").onclick = () => location.hash = "#/lesson/" + (i - 1); $("#nx").onclick = () => location.hash = "#/lesson/" + (i + 1); } };
}


function quizPage(id) {
  const q = QZ.find(x => x.id === id); if (!q) { location.hash = "#/assignments"; return null; }
  const res = S.quiz[id];
  QA[id] = QA[id] || q.questions.map(() => null);
  const idxOf = c => P.findIndex(p => p.code === c);
  const body = q.questions.map((x, i) => {
    const r = res && res.results[i];
    return `<div class="qq ${r ? (r.correct ? "ok" : "bad") : ""}"><div class="qn">Câu ${i + 1}/${q.questions.length}</div><div class="qt">${esc(x.q)}</div>` +
      x.options.map((o, k) => `<label class="opt ${r ? (k === r.answer ? "right" : (k === r.chosen ? "wrong" : "")) : ""}"><input type="radio" name="q${i}" value="${k}" ${(res ? r.chosen : QA[id][i]) === k ? "checked" : ""} ${res ? "disabled" : ""}><span class="ltr">${"ABCD"[k]}</span><span>${esc(o)}</span></label>`).join("") +
      (r ? `<div class="exp"><b>${r.correct ? "Đúng." : "Chưa đúng."}</b> ${esc(r.explain)} <a href="#/lesson/${idxOf(r.code)}">Xem trang bài (${r.code})</a></div>` : "") + `</div>`;
  }).join("");
  return { crumb: crumbs([COURSE, "#/home"], ["Bài tập", "#/assignments"], [esc(q.title)]), lesson: 1, ctx: "Đang làm: " + q.title,
    chips: ["Giải thích lại khái niệm token giúp tôi.", "Fine-tuning khác RAG ở điểm nào?", "Cho tôi đáp án quiz này."],
    html: `<div class="qpage"><div class="lh"><h1>${esc(q.title)}</h1>${res ? `<div class="score">${res.score}/${res.total}</div>` : ""}</div>
      <p class="lead">${esc(q.desc)} ${res ? "" : "Chọn một đáp án A, B, C hoặc D cho mỗi câu rồi bấm Nộp bài."}</p>${body}
      <div class="pn">${res ? `<button class="btn" id="rt">Làm lại</button>` : `<button class="btn pri" id="sb" disabled>Nộp bài</button><span id="cnt" class="cnt"></span>`}<a class="btn" href="#/assignments" style="text-decoration:none">‹ Danh sách bài</a></div></div>`,
    after: () => {
      const sb = $("#sb"), rt = $("#rt");
      const upd = () => { if (!sb) return; const n = QA[id].filter(a => a !== null).length; sb.disabled = n < QA[id].length; $("#cnt").textContent = "Đã chọn " + n + "/" + QA[id].length; };
      document.querySelectorAll(".qq input").forEach(inp => inp.onchange = () => { QA[id][+inp.name.slice(1)] = +inp.value; upd(); });
      upd();
      if (rt) rt.onclick = () => { delete S.quiz[id]; QA[id] = q.questions.map(() => null); save(); render(); };
      if (sb) sb.onclick = async () => {
        if (QA[id].some(a => a === null)) { toast("Hãy chọn đáp án cho cả " + QA[id].length + " câu."); return; }
        sb.disabled = true;
        try {
          const r = await fetch("/api/quiz/" + id + "/grade", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ answers: QA[id] }) });
          const j = await r.json(); if (!r.ok) throw new Error(j.detail || "Lỗi " + r.status);
          S.quiz[id] = { score: j.score, total: j.total, results: j.results, at: Date.now() }; save(); toast("Đã nộp: " + j.score + "/" + j.total); render();
          const b = $(".lesson .body"); if (b) b.scrollTop = 0;
        } catch (e) { toast("Không nộp được: " + e.message); sb.disabled = false; }
      };
    } };
}

const GHOST = { home: "token  RAG", announcements: "thông báo", assignments: "bài tập", grades: "điểm số", people: "thành viên", files: "tệp", syllabus: "đề cương", modules: "học phần", dash: "tổng quan", courses: "khoá học", inbox: "hộp thư", help: "trợ giúp", account: "tài khoản" };
let lastKey = "";
function render() {
  if (!S.user) return;
  const anim = location.hash !== lastKey; lastKey = location.hash;
  const oldScroll = (document.querySelector(".lesson .body, .scroll") || {}).scrollTop || 0;
  const { page, arg } = route();
  const def = page === "lesson" ? lessonPage(+arg) : page === "quiz" ? quizPage(arg) : (PAGES[page] || PAGES.home)();
  if (!def) return;
  document.querySelectorAll("[data-c]").forEach(a => a.classList.toggle("on", a.dataset.c === (page === "lesson" ? "modules" : page === "quiz" ? "assignments" : page)));
  const gk = ["account", "dash", "inbox", "help"].includes(page) ? page : "courses";
  document.querySelectorAll("[data-g]").forEach(b => b.classList.toggle("on", b.dataset.g === gk));
  $("#crumb").innerHTML = def.crumb;
  $("#cnav").style.display = def.flat ? "none" : "";
  $("#burger").style.visibility = def.flat ? "hidden" : "";
  const st = $("#stage"), m = $("#msgr");
  const ghost = page === "lesson" ? (P[+arg].code + "  " + P[+arg].title.toLowerCase()) : page === "quiz" ? "trắc nghiệm" : (GHOST[page] || "token  ngữ cảnh  RAG");
  m.style.display = def.lesson ? "" : "none"; $("#fab").style.display = def.lesson ? "" : "none";
  if (def.lesson) { st.innerHTML = `<div class="lesson"><div class="body ${anim ? "view" : ""}" data-ghost="${esc(ghost)}">${def.html}</div></div>`; if (!anim) { const bd = $(".lesson .body"); if (bd) bd.scrollTop = oldScroll; } def.after && def.after(); curCtx = def.ctx || ""; const pc = curChips; curChips = def.chips || null; if (!m.dataset.ready) buildMsgr(); else { ctx(); if (!S.msgs.length && pc !== curChips) drawLog(); } if (pendAsk) { const q = pendAsk; pendAsk = null; setTimeout(() => { m.classList.add("open"); ask(q); }, 120); } }
  else { st.innerHTML = `<div class="scroll ${page} ${anim ? "view" : ""}" data-ghost="${esc(ghost)}" style="flex:1">${def.html}</div>`; if (!anim) { const sc = $(".scroll"); if (sc) sc.scrollTop = oldScroll; } def.after && def.after(); }
}

/* ---------- Messenger (chỉ hiện ở trang bài) */
const CHIPS = ["Token là gì và vì sao nó ảnh hưởng chi phí?", "Fine-tuning khác RAG ở điểm nào?", "Viết hộ tôi bài nộp tuần này."];
const LAB = { answer: "Có căn cứ trong bài", ask: "Hỏi lại cho rõ", none: "Không có trong bài", refuse: "Từ chối", other: "Phản hồi", fake: "Chưa nối model", error: "Lỗi" };
const chipify = t => esc(t).replace(/\[?\b(p\d{2})\b\]?/g, '<button class="code" data-cite="$1">$1</button>');
let curCtx = "";
function ctx() { const c = $("#mctx"); if (!c) return; const { page, arg } = route(); c.textContent = curCtx || (page === "lesson" && P[+arg] ? "Đang xem: " + String(+arg + 1).padStart(2, "0") + " · " + P[+arg].title : ""); }
function buildMsgr() {
  const m = $("#msgr"); m.dataset.ready = 1;
  m.innerHTML = `<div class="mh2"><span class="ava">${brand(38, 1)}</span><div class="grow"><b>Trợ giảng AI</b><small id="mctx"></small></div><button class="ib" id="clr" title="Xoá cuộc trò chuyện" aria-label="Xoá cuộc trò chuyện">${ic("trash")}</button><button class="ib" id="cls" title="Đóng" aria-label="Đóng">✕</button></div>
  <div class="mlog" id="mlog" aria-live="polite"></div>
  <form class="mform" id="mf"><textarea id="mi" rows="1" maxlength="600" placeholder="Nhắn cho trợ giảng..." aria-label="Câu hỏi"></textarea><button id="ms" aria-label="Gửi" type="submit">${ic("send")}</button></form>
  <div class="mnote">Trợ giảng chỉ dựa vào nội dung chính của bài. Có thể sai, hãy mở đoạn được trích để kiểm tra. Đã hỏi ${"${n}"}/${MAX_Q} câu.</div>`;
  const ta = $("#mi");
  ta.oninput = () => { ta.style.height = "auto"; ta.style.height = Math.min(ta.scrollHeight, 120) + "px"; };
  ta.onkeydown = e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("#mf").requestSubmit(); } };
  $("#mf").onsubmit = e => { e.preventDefault(); const v = ta.value.trim(); if (v) { ta.value = ""; ta.style.height = "auto"; ask(v); } };
  $("#clr").onclick = () => { S.msgs = []; S.n = 0; save(); drawLog(); toast("Đã bắt đầu cuộc trò chuyện mới"); };
  $("#cls").onclick = () => m.classList.remove("open");
  m.onclick = e => { const c = e.target.closest("[data-cite]"); if (c) openCode(c.dataset.cite); const q = e.target.closest("[data-q]"); if (q) ask(q.dataset.q); };
  ctx(); drawLog();
}
function note() { const n = $(".mnote"); if (n) n.textContent = `Trợ giảng chỉ dựa vào nội dung chính của bài. Có thể sai, hãy mở đoạn được trích để kiểm tra. Đã hỏi ${S.n}/${MAX_Q} câu.`; }
function drawLog(typing) {
  const log = $("#mlog"); if (!log) return;
  let h = `<div class="row"><span class="ava">${brand(28)}</span><div class="bub bot">Chào ${/^(Học viên|Khách)/.test(S.user.name) ? "bạn" : esc(S.user.name.split(" ").pop())}! Mình là trợ giảng của khoá. Chỗ nào trong trang này chưa rõ thì cứ hỏi. Mình chỉ trả lời từ nội dung chính của bài và luôn ghi mã đoạn để bạn kiểm tra.</div></div>`;
  if (!S.msgs.length && !typing) h += `<div class="chips">${(curChips || CHIPS).map(c => `<button data-q="${esc(c)}">${esc(c)}</button>`).join("")}</div>`;
  S.msgs.forEach(m => {
    h += `<div class="row me"><div class="bub me">${esc(m.q)}</div></div><div class="row"><span class="ava">${brand(28)}</span><div class="bub bot"><span class="lab ${m.kind}">${LAB[m.kind] || "Phản hồi"}</span>${chipify(m.out)}</div></div>`;
    if (m.codes.length) h += `<div class="cites">${m.codes.map(c => { const p = P.find(x => x.code === c); return `<button class="cc" data-cite="${c}"><b>${c}${p ? " · " + esc(p.title) : ""}</b>${p ? `<span>${esc((sentences(p.text)[0] || "").slice(0, 110))}…</span>` : ""}<em>Mở đoạn này</em></button>`; }).join("")}</div>`;
    if (m.steps && m.steps.length) h += `<details class="steps"><summary>Trợ giảng đã làm gì (${m.steps.length} bước)</summary><ol>${m.steps.map(x => `<li><span class="by ${x.by}">${x.by === "model" ? "AI" : "code"}</span><div><b>${esc(x.t)}</b>${x.s != null ? ` <small>${x.s}s</small>` : ""}<br><span>${esc(x.d)}</span></div></li>`).join("")}</ol><p>Chỉ bước 3 dùng AI. Các bước còn lại là quy tắc bằng code, để chặn bịa mã đoạn và câu chèn chỉ dẫn.</p></details>`;
    h += `<div class="meta">${esc((m.models || []).join(", ") || "-")} · token ${m.tin || 0}/${m.tout || 0} · ${m.sec || 0} giây</div>`;
  });
  if (m_pending) h += `<div class="row me"><div class="bub me">${esc(m_pending)}</div></div>`;
  if (typing) h += `<div class="row"><span class="ava">${brand(28)}</span><div class="bub bot"><div class="typing"><i></i><i></i><i></i></div><small class="wait">Đang tìm đoạn liên quan trong bài và hỏi model…</small></div></div>`;
  log.innerHTML = h; log.scrollTop = log.scrollHeight; note();
}
let m_pending = "";
async function ask(q) {
  if (busy) return;
  if (S.n >= MAX_Q) { toast("Đã hết " + MAX_Q + " câu cho phiên này. Bấm thùng rác để hỏi tiếp."); return; }
  busy = true; $("#ms").disabled = true; m_pending = q; drawLog(true); bar(60, 1);
  let msg;
  try {
    const r = await fetch("/api/ask", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ q }) });
    const j = await r.json();
    if (!r.ok) throw new Error(j.error || j.detail || "Lỗi " + r.status);
    msg = { q, out: j.out, kind: j.kind, codes: j.codes, models: j.models, tin: j.tokens_in, tout: j.tokens_out, sec: j.sec, steps: j.steps || [] };
    S.n++;
  } catch (e) { msg = { q, out: "Lỗi khi gọi máy chủ: " + e.message, kind: "error", codes: [], models: [], sec: 0 }; }
  S.msgs.push(msg); m_pending = ""; save(); busy = false; bar(100);
  const ms = $("#ms"); if (ms) ms.disabled = false; drawLog(); render_cited_tag();
}
function render_cited_tag() { const { page, arg } = route(); if (page === "lesson") { const body = $(".lesson .body"); const y = body.scrollTop; const s = $("#pg"); if (s) { const p = P[+arg]; const last = S.msgs[S.msgs.length - 1]; const has = last && last.codes.includes(p.code); const t = s.querySelector(".tag"); if (has && !t) s.querySelector(".code").insertAdjacentHTML("afterend", '<span class="tag">đoạn được trích</span>'); if (!has && t) t.remove(); } body.scrollTop = y; } }
function openCode(c) { const i = P.findIndex(p => p.code === c); if (i < 0) return; const { page, arg } = route(); if (page === "lesson" && +arg === i) { const pg = $("#pg"); pg.classList.remove("hit"); void pg.offsetWidth; pg.classList.add("hit"); pg.scrollIntoView({ behavior: "smooth", block: "center" }); } else location.hash = "#/lesson/" + i; }

/* ---------- khởi động */
async function boot() {
  if (!S.user) { renderLogin(); return; }
  shell(); bar(40, 1);
  $("#stage").innerHTML = `<div class="scroll" style="flex:1">${'<div class="skel"></div>'.repeat(8)}</div>`;
  if (!P.length) { try { P = (await (await fetch("/api/lesson")).json()).passages; try { QZ = await (await fetch("/api/quiz")).json(); } catch (e2) { QZ = []; } } catch (e) { $("#stage").innerHTML = `<div class="empty">Không tải được bài học. Thử tải lại trang.</div>`; return; } }
  bar(100); render();
}
window.addEventListener("hashchange", () => { if (S.user && P.length) { $("#msgr") && $("#msgr").classList.remove("open"); if (window.innerWidth < 760 && $("#cnav")) { cnavHide = true; $("#cnav").classList.add("hide"); } bar(70); render(); } });
boot();
