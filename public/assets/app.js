(function () {
  "use strict";
  var $ = function (s) { return document.querySelector(s); };

  /* ---- menu ponsel ---- */
  var toggle = $(".nav-toggle"), nav = $("#menu");
  toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
    toggle.textContent = open ? "Tutup" : "Menu";
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && nav.classList.contains("open")) toggle.click();
  });

  /* ---- penanda menu aktif ---- */
  var links = Array.prototype.slice.call(nav.querySelectorAll("a"));
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          a.setAttribute("aria-current", a.getAttribute("href") === "#" + en.target.id ? "true" : "false");
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    links.forEach(function (a) { var s = $(a.getAttribute("href")); if (s) io.observe(s); });
  }

  /* ---- penghargaan ---- */
  var data = window.PENGHARGAAN || [];
  var histo = $("#histo"), list = $("#daftar"), q = $("#q"), info = $("#info"), more = $("#lebih");
  var state = { year: null, query: "", all: false };
  var LIMIT = window.matchMedia("(max-width: 700px)").matches ? 12 : 24;

  var counts = {};
  data.forEach(function (d) { counts[d.y] = (counts[d.y] || 0) + 1; });
  var years = Object.keys(counts).map(Number).sort();
  var max = Math.max.apply(null, years.map(function (y) { return counts[y]; }));

  function bar(label, n, val, pct) {
    var b = document.createElement("button");
    b.type = "button";
    b.dataset.y = val;
    b.setAttribute("aria-pressed", "false");
    b.setAttribute("aria-label", label + ": " + n + " penghargaan");
    b.innerHTML = '<span class="n">' + n + '</span><span class="bar" style="--h:' + pct + '%"></span><span class="y">' + label + "</span>";
    histo.appendChild(b);
  }
  bar("Semua", data.length, "", 100);
  years.forEach(function (y) { bar(String(y), counts[y], y, Math.round(counts[y] / max * 78)); });
  histo.firstChild.setAttribute("aria-pressed", "true");

  histo.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    state.year = b.dataset.y ? Number(b.dataset.y) : null;
    state.all = false;
    Array.prototype.forEach.call(histo.children, function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
    render();
  });

  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function hl(text, query) {
    var safe = esc(text);
    if (!query) return safe;
    var re = new RegExp("(" + query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
    return safe.replace(re, "<mark>$1</mark>");
  }

  var t;
  q.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(function () { state.query = q.value.trim(); state.all = false; render(); }, 120);
  });
  more.addEventListener("click", function () { state.all = true; render(); });

  function render() {
    var nq = norm(state.query);
    var rows = data.filter(function (d) {
      return (state.year === null || d.y === state.year) && (!nq || norm(d.t).indexOf(nq) > -1);
    });
    var shown = state.all ? rows : rows.slice(0, LIMIT);
    list.innerHTML = shown.map(function (d) {
      return "<li><span>" + d.y + "</span><div>" + hl(d.t, state.query) + "</div></li>";
    }).join("");
    if (!rows.length) {
      list.innerHTML = '<li class="kosong">Tidak ada penghargaan yang cocok dengan "' + esc(state.query) + '". Coba kata lain, atau pilih "Semua".</li>';
    }
    var scope = state.year ? "tahun " + state.year : "2008–2016";
    info.textContent = rows.length + " penghargaan, " + scope + (shown.length < rows.length ? ". Menampilkan " + shown.length + "." : ".");
    more.hidden = shown.length >= rows.length;
    more.textContent = "Tampilkan semua " + rows.length;
  }
  render();

  /* ---- referensi ---- */
  var refs = window.REFERENSI || [];
  $("#nref").textContent = refs.length;
  $("#ref").innerHTML = refs.map(function (r) { return "<li>" + esc(r) + "</li>"; }).join("");

  /* ---- feed medsos: dimuat saat section terlihat ---- */
  var feedBox = document.querySelector("#medsos");
  function muatFeed() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-embed]"), function (box) {
      var jenis = box.dataset.embed;
      if (jenis === "tt") {
        if (!document.querySelector('script[src*="tiktok.com/embed.js"]')) {
          var sc = document.createElement("script"); sc.async = true; sc.src = "https://www.tiktok.com/embed.js";
          document.body.appendChild(sc);
        }
        return;
      }
      var f = document.createElement("iframe");
      var src = box.dataset.src;
      if (jenis === "fb") {
        var w = Math.max(180, Math.min(500, Math.floor(box.clientWidth)));
        src = src.replace(/width=\d+/, "width=" + w).replace(/height=\d+/, "height=" + Math.floor(box.clientHeight || 560));
      }
      f.src = src; f.loading = "lazy"; f.title = jenis === "fb" ? "Facebook Kang Aher" : "Instagram Kang Aher";
      f.setAttribute("allow", "encrypted-media; clipboard-write; picture-in-picture");
      f.setAttribute("scrolling", "yes");
      box.innerHTML = ""; box.appendChild(f);
    });
  }
  if (feedBox && "IntersectionObserver" in window) {
    var fio = new IntersectionObserver(function (en) {
      if (en.some(function (e) { return e.isIntersecting; })) { muatFeed(); fio.disconnect(); }
    }, { rootMargin: "400px 0px" });
    fio.observe(feedBox);
  } else if (feedBox) { muatFeed(); }

  /* ---- bagikan ---- */
  var url = location.origin + "/";
  var text = "Kenali lebih dekat Kang Aher, Ahmad Heryawan: dari Sukaraja ke Gedung Sate dua periode, lalu Senayan.";
  var e = encodeURIComponent;
  var share = {
    wa: "https://wa.me/?text=" + e(text + " " + url),
    fb: "https://www.facebook.com/sharer/sharer.php?u=" + e(url),
    x: "https://twitter.com/intent/tweet?text=" + e(text) + "&url=" + e(url),
    tg: "https://t.me/share/url?url=" + e(url) + "&text=" + e(text)
  };
  Array.prototype.forEach.call(document.querySelectorAll("[data-bagi]"), function (a) { a.href = share[a.dataset.bagi]; });

  var toast = $("#toast"), tt;
  function say(msg) {
    toast.textContent = msg; toast.classList.add("on");
    clearTimeout(tt); tt = setTimeout(function () { toast.classList.remove("on"); }, 2200);
  }
  $("#salin").addEventListener("click", function () {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(function () { say("Tautan tersalin"); }, function () { say("Salin manual: " + url); });
    } else { say("Salin manual: " + url); }
  });
})();
