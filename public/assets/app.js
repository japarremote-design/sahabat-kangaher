(function () {
  "use strict";
  var $ = function (s) { return document.querySelector(s); };
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---- menu ponsel (bawah, dekat jempol) ---- */
  var toggle = $(".nav-toggle"), nav = $("#menu"), tirai = $(".tirai");
  function setMenu(open) {
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open);
    tirai.hidden = !open;
  }
  toggle.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  tirai.addEventListener("click", function () { setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) { setMenu(false); tutupSub(); } });

  /* sub menu: tombol panah membuka/menutup */
  function tutupSub(kecuali) {
    Array.prototype.forEach.call(nav.querySelectorAll(".punya-sub.open"), function (li) {
      if (li === kecuali) return;
      li.classList.remove("open"); li.querySelector(".sub-tg").setAttribute("aria-expanded", "false");
    });
  }
  Array.prototype.forEach.call(nav.querySelectorAll(".sub-tg"), function (b) {
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var li = b.parentNode, buka = !li.classList.contains("open");
      tutupSub(li);
      li.classList.toggle("open", buka); b.setAttribute("aria-expanded", buka);
    });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest("#menu")) tutupSub(); });

  /* tautan ke bidang program: buka rinciannya */
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]'); if (!a) return;
    var t = document.getElementById(a.getAttribute("href").slice(1));
    if (t && t.tagName === "DETAILS") t.open = true;
  });

  /* datang dari halaman lain ke #bidang-x: buka rinciannya */
  if (location.hash) {
    var tujuan = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (tujuan && tujuan.tagName === "DETAILS") tujuan.open = true;
  }

  /* tusuk sate beranimasi saat terlihat */
  var sate = $(".sate");
  if (sate && "IntersectionObserver" in window) {
    sate.classList.add("tunggu");
    var sio = new IntersectionObserver(function (en) {
      if (en[0].isIntersecting) { sate.classList.add("jalan"); sio.disconnect(); }
    }, { threshold: .25 });
    sio.observe(sate);
  }

  /* ---- penghargaan (hanya di halaman yang memuatnya) ---- */
  var histo = $("#histo");
  if (histo && window.PENGHARGAAN) (function () {
  var data = window.PENGHARGAAN || [];
  var list = $("#daftar"), q = $("#q"), info = $("#info"), more = $("#lebih");
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
  })();

  /* ---- referensi ---- */
  var refBox = $("#ref");
  if (refBox && window.REFERENSI) {
    $("#nref").textContent = window.REFERENSI.length;
    refBox.innerHTML = window.REFERENSI.map(function (r) { return "<li>" + esc(r) + "</li>"; }).join("");
  }

  /* ---- feed medsos: dimuat saat section terlihat ---- */
  var feedBox = document.querySelector("#medsos");
  function muatFeed() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-embed]"), function (box) {
      var jenis = box.dataset.embed;
      var src = box.dataset.src;
      if (jenis === "tt") {
        if (!document.querySelector('script[src*="tiktok.com/embed.js"]')) {
          var sc = document.createElement("script"); sc.async = true; sc.src = "https://www.tiktok.com/embed.js";
          document.body.appendChild(sc);
        }
        return;
      }
      if (jenis === "x") {
        if (!document.querySelector('script[src*="platform.twitter.com/widgets.js"]')) {
          var xs = document.createElement("script"); xs.async = true; xs.src = "https://platform.twitter.com/widgets.js"; xs.charset = "utf-8";
          document.body.appendChild(xs);
        }
        return;
      }
      if (jenis === "yt") {
        var ch = box.dataset.channel; if (!ch) return;
        src = "https://www.youtube-nocookie.com/embed/videoseries?list=UU" + ch.slice(2);
        box.classList.remove("feed-kartu");
      }
      var f = document.createElement("iframe");
      if (jenis === "fb") {
        var w = Math.max(180, Math.min(500, Math.floor(box.clientWidth)));
        src = src.replace(/width=\d+/, "width=" + w).replace(/height=\d+/, "height=" + Math.floor(box.clientHeight || 560));
      }
      f.src = src; f.loading = "lazy"; f.title = { fb: "Facebook Kang Aher", ig: "Instagram Kang Aher", yt: "Video YouTube Kang Aher" }[jenis];
      f.setAttribute("allow", "encrypted-media; clipboard-write; picture-in-picture");
      f.setAttribute("scrolling", "yes"); f.setAttribute("allowfullscreen", "");
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
  var canon = document.querySelector('link[rel="canonical"]');
  var url = canon ? canon.href : location.href;
  var ogt = document.querySelector('meta[property="og:description"]');
  var text = ogt ? ogt.content : document.title;
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
  var salin = $("#salin");
  if (salin) salin.addEventListener("click", function () {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(function () { say("Tautan tersalin"); }, function () { say("Salin manual: " + url); });
    } else { say("Salin manual: " + url); }
  });
})();
