#!/usr/bin/env python3
"""Membangun situs Sahabat Kang Aher (multi-halaman) ke folder public/.

Pakai:  python3 site/build.py
Sumber: site/parts/*.html (potongan bagian), site/kabar.py (artikel Kabar).
Hasil:  public/index.html, public/<halaman>/index.html, public/kabar/<slug>/index.html,
        public/404.html, public/sitemap.xml
"""
import datetime, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE, PUB = ROOT / "site", ROOT / "public"
sys.path.insert(0, str(SITE))
from kabar import KABAR  # noqa: E402
from tanya import TANYA  # noqa: E402

DOMAIN = "https://sahabat.kangaher.web.id"
VER = datetime.datetime.now().strftime("%y%m%d%H%M")
HARI_INI = datetime.date.today().isoformat()
BULAN = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


def part(n):
    return (SITE / "parts" / n).read_text(encoding="utf-8")


def tgl(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{d} {BULAN[m]} {y}"


# ---------------------------------------------------------------- ikon
IK = {
 "rumah": "M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8h5Z",
 "profil": "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm0 2c-2.7 0-8 1.3-8 4v2h16v-2c0-2.7-5.3-4-8-4Z",
 "kartu": "M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm5 3a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm-3 7.5V16h6v-.5C11 14 9.6 13.2 8 13.2S5 14 5 15.5ZM13 9v1.6h6V9h-6Zm0 3.4V14h4.5v-1.6H13Z",
 "toga": "M5 13.2v4L12 21l7-3.8v-4L12 17l-7-3.8ZM12 3 1 9l11 6 9-4.9V17h2V9L12 3Z",
 "tas": "M10 4h4a2 2 0 0 1 2 2v1h4a2 2 0 0 1 2 2v4H2V9a2 2 0 0 1 2-2h4V6a2 2 0 0 1 2-2Zm0 3h4V6h-4v1ZM2 15h8v2h4v-2h8v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-4Z",
 "grup": "M16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm-8 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm0 2c-2.3 0-7 1.2-7 3.5V19h14v-2.5C15 14.2 10.3 13 8 13Zm8 0c-.3 0-.6 0-1 .1 1.2.8 2 1.9 2 3.4V19h6v-2.5c0-2.3-4.7-3.5-7-3.5Z",
 "buku": "M21 5c-1.1-.4-2.3-.5-3.5-.5-1.9 0-4 .4-5.5 1.5-1.4-1.1-3.6-1.5-5.5-1.5S2.5 4.9 1 6v14.6c0 .3.3.5.5.5h.3c1.4-.7 3.3-1.1 4.7-1.1 1.9 0 4.1.4 5.5 1.5 1.4-.9 3.8-1.5 5.5-1.5 1.7 0 3.4.3 4.8 1.1h.3c.3 0 .5-.3.5-.5V6c-.6-.5-1.3-.8-2.1-1Zm0 13.5c-1.1-.3-2.3-.5-3.5-.5-1.7 0-4.1.7-5.5 1.5V8c1.4-.9 3.8-1.5 5.5-1.5 1.2 0 2.4.2 3.5.5v11.5Z",
 "rute": "M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Z",
 "pensil": "M3 17.2V21h3.8l11-11-3.8-3.8-11 11Zm17.7-10.2a1 1 0 0 0 0-1.4l-2.3-2.3a1 1 0 0 0-1.4 0l-1.8 1.8 3.8 3.8 1.7-1.9Z",
 "gedung": "M4 10v7h3v-7H4Zm6 0v7h3v-7h-3ZM2 22h19v-3H2v3Zm14-12v7h3v-7h-3Zm-4.5-9L2 6v2h19V6l-9.5-5Z",
 "kopiah": "M12 4c-4.4 0-8 2.7-8 6v3h16v-3c0-3.3-3.6-6-8-6ZM3 15v2c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-2H3Z",
 "senayan": "M12 2 3 7v2h18V7l-9-5Zm-7 9v6h2v-6H5Zm4 0v6h2v-6H9Zm4 0v6h2v-6h-2Zm4 0v6h2v-6h-2ZM3 19v3h18v-3H3Z",
 "kotak": "M18 13h-.7l-2 2h1.9L19 17H5l1.8-2h2l-2-2H6l-3 3v4c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-4l-3-3Zm-1-5.1-5 5-3.5-3.5 5-5L17 7.9Zm-4.3-6.6L6.3 7.7a1 1 0 0 0 0 1.4l4.9 4.9a1 1 0 0 0 1.4 0l6.4-6.4a1 1 0 0 0 0-1.4L14.1 1.3a1 1 0 0 0-1.4 0Z",
 "estafet": "M4 11h11.2l-4.6-4.6L12 5l7 7-7 7-1.4-1.4 4.6-4.6H4v-2Z",
 "grafik": "M5 9h3v11H5V9Zm5.5-5h3v16h-3V4ZM16 13h3v7h-3v-7Z",
 "papan": "M19 3h-4.2C14.4 1.8 13.3 1 12 1s-2.4.8-2.8 2H5a2 2 0 0 0-2 2v14c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2Zm-7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2Zm-2 14-4-4 1.4-1.4 2.6 2.6 6.6-6.6L18 9l-8 8Z",
 "jalan": "M2 17h20v2H2v-2Zm1-7h2v6H3v-6Zm16 0h2v6h-2v-6ZM7 10h2v6H7v-6Zm8 0h2v6h-2v-6Zm-4 0h2v6h-2v-6ZM2 9c3-4 17-4 20 0v1H2V9Z",
 "air": "M12 2s-7 7.6-7 12.5a7 7 0 0 0 14 0C19 9.6 12 2 12 2Zm-3.5 13h2a1.5 1.5 0 0 0 1.5 1.5v2A3.5 3.5 0 0 1 8.5 15Z",
 "daun": "M17 8C8 10 5.9 16.2 3.8 21.3l1.9.7.9-2.3c.5.2 1 .3 1.4.3C19 20 22 3 22 3c-1 2-8 2.3-13 3.3S2 11.5 2 13.5s1.8 3.8 1.8 3.8C7 8 17 8 17 8Z",
 "pabrik": "M2 22V10l6-3.5V10l6-3.5V10l6-3.5V22H2Zm4-6v3h3v-3H6Zm5 0v3h3v-3h-3Zm5 0v3h3v-3h-3ZM20 2h-3v4.3l3-1.7V2Z",
 "perisai": "M12 1 3 5v6c0 5.6 3.8 10.7 9 12 5.2-1.3 9-6.4 9-12V5l-9-4Zm-2 16-4-4 1.4-1.4 2.6 2.6 6.6-6.6L18 9l-8 8Z",
 "piala": "M19 5h-2V3H7v2H5a2 2 0 0 0-2 2v1c0 2.5 1.9 4.6 4.4 4.9.6 1.5 2 2.7 3.6 3V19H7v2h10v-2h-4v-3.1c1.6-.3 3-1.5 3.6-3C19.1 12.6 21 10.5 21 8V7a2 2 0 0 0-2-2ZM5 8V7h2v3.8C5.8 10.4 5 9.3 5 8Zm14 0c0 1.3-.8 2.4-2 2.8V7h2v1Z",
 "daftar": "M3 13h2v-2H3v2Zm0 4h2v-2H3v2Zm0-8h2V7H3v2Zm4 4h14v-2H7v2Zm0 4h14v-2H7v2ZM7 7v2h14V7H7Z",
 "medali": "M12 8a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13Zm2.3 10.2L12 16.9l-2.3 1.3.6-2.6-2-1.7 2.6-.2 1.1-2.4 1.1 2.4 2.6.2-2 1.7.6 2.6ZM7 1h4l1.5 5.3a8.4 8.4 0 0 0-3.3.9L7 1Zm10 0h-4l-.6 2.2 1.1 3.7c1 .2 1.9.6 2.7 1.1L17 1Z",
 "koran": "M20 4H6a2 2 0 0 0-2 2v11a1 1 0 0 1-2 0V8H0v9a3 3 0 0 0 3 3h16a3 3 0 0 0 3-3V6a2 2 0 0 0-2-2Zm-1 13H7V7h12v10ZM9 9h4v4H9V9Zm6 0h2v1.5h-2V9Zm0 2.5h2V13h-2v-1.5ZM9 14h8v1.5H9V14Z",
 "info": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 15h-2v-6h2v6Zm0-8h-2V7h2v2Z",
 "bintang": "M12 2l2.9 6.9 7.1.6-5.4 4.7 1.6 7L12 17.3 5.8 21.2l1.6-7L2 9.5l7.1-.6L12 2Z",
 "pustaka": "M4 6H2v14a2 2 0 0 0 2 2h14v-2H4V6Zm16-4H8a2 2 0 0 0-2 2v12c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2Zm-1 9H9V9h10v2Zm-4 4H9v-2h6v2Zm4-8H9V5h10v2Z",
 "chat": "M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2ZM8 11a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm4 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm4 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z",
 "menu": "M4 6h16v2H4V6Zm0 5h16v2H4v-2Zm0 5h16v2H4v-2Z",
 "panah": "M4 11h11.2l-4.6-4.6L12 5l7 7-7 7-1.4-1.4 4.6-4.6H4v-2Z",
}


def ik(name, c):
    return f'<i class="ik {c}" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{IK[name]}"/></svg></i>'


CHEV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.4 8.6 12 13.2l4.6-4.6L18 10l-6 6-6-6 1.4-1.4Z"/></svg>'

# ---------------------------------------------------------------- halaman
# kunci -> (path, judul tab, deskripsi, judul h1, kalimat pembuka, bagian, butuh data.js, og)
HAL = {
 "profil": dict(path="/profil/", nav="Profil",
   title="Profil Kang Aher | Biografi Dr. H. Ahmad Heryawan, Lc., M.Si.",
   desc="Biografi lengkap Ahmad Heryawan (Kang Aher): data diri, pendidikan SD sampai S3, riwayat pekerjaan, organisasi, kisah awal, dan akun media sosial.",
   h1="Profil Kang Aher", lead="Data diri, pendidikan, pekerjaan, dan organisasi Dr. H. Ahmad Heryawan, Lc., M.Si.",
   parts=["profil.html"], og=("Profil", "Kang Aher", "Biografi Dr. H. Ahmad Heryawan, Lc., M.Si.")),
 "perjalanan": dict(path="/perjalanan/", nav="Perjalanan",
   title="Perjalanan Kang Aher | Dari Sukaraja, Gedung Sate, ke Senayan",
   desc="Linimasa Ahmad Heryawan 1966–2025: DPRD DKI Jakarta, dua periode Gubernur Jawa Barat, Pilpres 2014, DPR RI, hingga Ketua BAM, plus jejak pemilu.",
   h1="Perjalanan Kang Aher", lead="Dari anak kampung di Sukaraja, ke Gedung Sate dua periode, lalu Senayan.",
   parts=["perjalanan.html", "politik.html", "suara.html"], og=("Perjalanan", "1966–2025", "Dari Sukaraja ke Gedung Sate, lalu Senayan")),
 "program": dict(path="/program/", nav="Program",
   title="Program Kang Aher untuk Jawa Barat 2008–2018",
   desc="Tujuh bidang kerja Ahmad Heryawan sebagai Gubernur Jawa Barat: pendidikan, infrastruktur, lingkungan, pertanian dan kopi, industri, tata kelola, perumahan.",
   h1="Program untuk Jawa Barat", lead="Tujuh bidang kerja selama dua periode memimpin Jawa Barat, 2008–2018.",
   parts=["program.html"], og=("Program", "Jawa Barat", "Tujuh bidang kerja Kang Aher, 2008–2018")),
 "penghargaan": dict(path="/penghargaan/", nav="Penghargaan",
   title="206 Penghargaan Jawa Barat di Era Kang Aher | Tanda Kehormatan",
   desc="Daftar lengkap 206 penghargaan Pemprov Jawa Barat 2008–2016 di bawah Ahmad Heryawan, bisa disaring per tahun, plus 13 tanda kehormatan pribadi.",
   h1="Penghargaan &amp; tanda kehormatan", lead="206 penghargaan untuk Jawa Barat dan 13 tanda kehormatan pribadi Kang Aher.",
   parts=["penghargaan.html"], data=True, og=("206", "Penghargaan", "Untuk Jawa Barat di era Kang Aher, 2008–2016")),
 "kabar": dict(path="/kabar/", nav="Kabar",
   title="Kabar Kang Aher | Kiprah Ketua BAM DPR RI",
   desc="Kabar terbaru kiprah Ahmad Heryawan sebagai Ketua Badan Aspirasi Masyarakat (BAM) DPR RI: aspirasi petani, warga, dan daerah yang dikawal.",
   h1="Kabar Kang Aher", lead="Kiprah terbaru sebagai Ketua Badan Aspirasi Masyarakat DPR RI, dirangkum dari pemberitaan resmi dan media.",
   parts=[], og=("Kabar", "Kang Aher", "Kiprah Ketua BAM DPR RI")),
 "catatan": dict(path="/catatan/", nav="Catatan",
   title="Catatan &amp; Klarifikasi Seputar Kang Aher | Sumber",
   desc="Isu dan klarifikasi seputar Ahmad Heryawan (Jaipong, Gunung Ciremai, saksi Meikarta), serba-serbi, serta daftar sumber dan referensi situs ini.",
   h1="Catatan &amp; sumber", lead="Isu, klarifikasi, serba-serbi, dan semua rujukan yang dipakai situs ini.",
   parts=["catatan.html", "sumber.html"], data=True, og=("Catatan", "&amp; Sumber", "Isu, klarifikasi, dan rujukan")),
 "medsos": dict(path="/medsos/", nav="Medsos",
   title="Media Sosial Kang Aher | Instagram, YouTube, TikTok, X, Threads, Facebook",
   desc="Ikuti Ahmad Heryawan di Instagram @aheryawan, YouTube, X, Threads, Facebook, dan TikTok @aheryawanofficial. Feed terbaru langsung di satu halaman.",
   h1="Medsos Kang Aher", lead="Enam akun resmi Kang Aher, lengkap dengan feed terbarunya.",
   parts=["medsos.html"], og=("Medsos", "Kang Aher", "Enam akun, satu halaman")),
}

# ---------------------------------------------------------------- menu
MENU = [
 ("profil", "profil", "c1", [("#data-diri", "Data diri", "kartu", "c3"), ("#pendidikan", "Pendidikan", "toga", "c4"), ("#pekerjaan", "Pekerjaan", "tas", "c2"), ("#organisasi", "Riwayat organisasi", "grup", "c3"), ("#kisah-awal", "Kisah awal", "buku", "c2"), ("#tanya-jawab", "Tanya jawab", "info", "c5")]),
 ("perjalanan", "rute", "c2", [("#th-1966", "Masa kecil &amp; sekolah", "pensil", "c3"), ("#th-1999", "DPRD DKI Jakarta", "gedung", "c4"), ("#th-2008", "Gubernur Jawa Barat", "kopiah", "c1"), ("#th-2024", "DPR RI &amp; BAM", "senayan", "c2"), ("#pilpres-2014", "Pilpres 2014", "kotak", "c1"), ("#estafet", "Estafet Gubernur Jabar", "estafet", "c2"), ("#suara", "Jejak pemilu", "grafik", "c3")]),
 ("program", "papan", "c1", [("#bidang-pendidikan", "Pendidikan", "toga", "c4"), ("#bidang-infrastruktur", "Infrastruktur", "jalan", "c1"), ("#bidang-lingkungan", "Lingkungan", "air", "c5"), ("#bidang-pertanian", "Pertanian &amp; kopi", "daun", "c2"), ("#bidang-industri", "Industri", "pabrik", "c4"), ("#bidang-tatakelola", "Tata kelola", "perisai", "c3"), ("#bidang-perumahan", "Perumahan rakyat", "rumah", "c1")]),
 ("penghargaan", "piala", "c3", [("#daftar-penghargaan", "206 penghargaan", "daftar", "c3"), ("#tanda-kehormatan", "Tanda kehormatan", "medali", "c1")]),
 ("kabar", "koran", "c4", []),
 ("catatan", "info", "c4", [("#catatan", "Isu &amp; klarifikasi", "info", "c4"), ("#serba-serbi", "Serba-serbi", "bintang", "c3"), ("#sumber", "Sumber", "pustaka", "c2")]),
 ("medsos", "chat", "c5", []),
]


def menu_html(aktif):
    li = []
    for key, icon, c, subs in MENU:
        h = HAL[key]
        cur = ' aria-current="page"' if key == aktif else ""
        a = f'<a href="{h["path"]}"{cur}>{ik(icon, c)}<span>{h["nav"]}</span></a>'
        if subs:
            sub = "".join(f'<li><a href="{h["path"]}{x}">{ik(i, cc)}<span>{l}</span></a></li>' for x, l, i, cc in subs)
            li.append(f'        <li class="punya-sub">{a}<button class="sub-tg" type="button" aria-expanded="false" aria-label="Sub menu {h["nav"]}">{CHEV}</button>\n          <ul class="sub">{sub}</ul></li>')
        else:
            li.append(f"        <li>{a}</li>")
    return "\n".join(li)


def header_html(aktif):
    h = part("header.html")
    h = re.sub(r'<a class="brand" href="[^"]*"', '<a class="brand" href="/"', h)
    a = h.index("      <ul>\n") + len("      <ul>\n")
    b = h.index("      </ul>\n    </nav>")
    return h[:a] + menu_html(aktif) + "\n" + h[b:]


def bawah_html(aktif):
    items = [("beranda", "/", "Beranda", "rumah", "c1"), ("profil", "/profil/", "Profil", "profil", "c2"),
             ("penghargaan", "/penghargaan/", "Prestasi", "piala", "c3"), ("kabar", "/kabar/", "Kabar", "koran", "c4")]
    out = []
    for k, href, label, icon, c in items:
        cur = ' aria-current="page"' if k == aktif else ""
        out.append(f'  <a href="{href}"{cur}>{ik(icon, c)}<span>{label}</span></a>')
    out.append(f'  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu">{ik("menu", "c5")}<span>Menu</span></button>')
    return '<nav class="bawah" aria-label="Navigasi cepat">\n' + "\n".join(out) + '\n</nav>\n<div class="tirai" hidden></div>'


# ---------------------------------------------------------------- kerangka
def tanya_html():
    q = "\n".join(f'''      <details{" open" if i == 0 else ""}>
        <summary><h3>{t}</h3><span class="tanda" aria-hidden="true">+</span></summary>
        <p>{j}</p>
      </details>''' for i, (t, j) in enumerate(TANYA))
    return f'''<section id="tanya-jawab" class="tanya" aria-labelledby="h-tanya">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-tanya">Yang sering ditanyakan</h2>
      <p>Jawaban singkat untuk pertanyaan yang paling banyak dicari tentang Kang Aher.</p>
    </div>
    <div class="tanya-daftar">
{q}
    </div>
  </div>
</section>
'''


def faq_ld():
    polos = lambda x: html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": t, "acceptedAnswer": {"@type": "Answer", "text": polos(j)}} for t, j in TANYA]}


def head_html(title, desc, path, og_img, og_type="website", jsonld=None):
    url = DOMAIN + path
    ld = f'<script type="application/ld+json">\n{json.dumps(jsonld, ensure_ascii=False)}\n</script>\n' if jsonld else ""
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#fe5000">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="Sahabat Kang Aher">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}{og_img}?v={VER}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/literata.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v={VER}">
{ld}</head>
<body>
<a class="skip" href="#isi">Langsung ke isi</a>
'''


def kaki_html(data=False):
    s = "\n" + part("footer.html") + "\n" + "{BAWAH}\n" + '<div class="toast" id="toast" role="status" aria-live="polite"></div>\n'
    if data:
        s += f'<script src="/assets/data.js?v={VER}" defer></script>\n'
    s += f'<script src="/assets/app.js?v={VER}" defer></script>\n</body>\n</html>\n'
    return s


def remah(*items):
    out = ['<a href="/">Beranda</a>']
    for label, href in items:
        out.append(f'<a href="{href}">{label}</a>' if href else f'<span aria-current="page">{label}</span>')
    return '<nav class="remah" aria-label="Lokasi halaman">' + '<span class="sep" aria-hidden="true">/</span>'.join(out) + "</nav>"


def kepala_hal(h1, lead, crumbs, extra=""):
    return f'''<section class="kepala-hal">
  <div class="wrap">
    {remah(*crumbs)}
    <h1>{h1}</h1>
    <p>{lead}</p>{extra}
  </div>
</section>
'''


PERSON = {"@type": "Person", "@id": DOMAIN + "/#kang-aher", "name": "Ahmad Heryawan", "honorificPrefix": "Dr. H.", "honorificSuffix": "Lc., M.Si.", "alternateName": ["Aher", "Kang Aher"], "birthDate": "1966-06-19", "jobTitle": "Ketua Badan Aspirasi Masyarakat DPR RI"}


def breadcrumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- tautan antar-halaman
def kumpulkan_id(pages_html):
    peta = {}
    for key, h in pages_html.items():
        for i in re.findall(r'\sid="([^"]+)"', h):
            peta.setdefault(i, (key, HAL[key]["path"]))
    for key in HAL:
        peta[key] = (key, HAL[key]["path"])
    return peta


def tulis_ulang_tautan(h, peta, aktif):
    ids_sini = set(re.findall(r'\sid="([^"]+)"', h))

    def ganti(m):
        i = m.group(1)
        if i in ids_sini or i in ("isi", "menu"):
            return m.group(0)
        if i in peta:
            key, path = peta[i]
            return f'href="{path}"' if i == key else f'href="{path}#{i}"'
        return m.group(0)
    return re.sub(r'href="#([^"]+)"', ganti, h)


# ---------------------------------------------------------------- beranda
def beranda_html():
    profil = part("profil.html")
    nama = re.search(r'<p class="nama-lengkap">.*?</p>', profil, re.S).group(0)
    pil = re.search(r'<ul class="sekilas-pil">.*?</ul>', profil, re.S).group(0)
    sate = re.search(r'<figure class="sate">.*?</figure>', part("perjalanan.html"), re.S).group(0)

    prog = part("program.html")
    tiles = []
    for m in re.finditer(r'<details(?: open)? id="bidang-([a-z]+)">\s*<summary><h3>(<i class="ik[^"]*".*?</i>)(.*?)</h3><span class="ringkas">(.*?)</span>', prog, re.S):
        slug, ikon, judul, ringkas = m.groups()
        tiles.append(f'<a class="ubin" href="/program/#bidang-{slug}">{ikon}<b>{judul}</b><span>{ringkas}</span></a>')

    peng = part("penghargaan.html")
    lencana = re.findall(r'<li><span class="th-lencana">(\d{4})</span><b>(.*?)</b>', peng)[:6]
    lenc = "".join(f'<li><span class="th-lencana">{y}</span><b>{n}</b></li>' for y, n in lencana)

    kabar = "".join(kartu_kabar(k) for k in KABAR[:3])

    akun = re.search(r'<ul class="akun">.*?</ul>', profil, re.S).group(0)

    return f'''{part("hero.html")}
<section class="beranda-profil" id="sekilas" aria-labelledby="h-sekilas">
  <div class="wrap dua">
    <div>
      <h2 id="h-sekilas" class="sr">Sekilas Kang Aher</h2>
      {nama}
      {pil}
      <p class="pengantar">Lahir dari keluarga sederhana di Sukaraja, Sukabumi, Aher kecil berjualan gorengan sambil berangkat sekolah. Beasiswa membawanya kuliah di LIPIA Jakarta, lalu ia mengajar dan berdakwah sebelum terjun ke politik: dua periode di DPRD DKI, sepuluh tahun memimpin Jawa Barat, dan kini Ketua Badan Aspirasi Masyarakat DPR RI.</p>
      <a class="btn lanjut" href="/profil/">Baca profil lengkap {ik("panah", "c1")}</a>
    </div>
    <dl class="fakta ringkas-fakta">
      <dt>Lahir</dt><dd>19 Juni 1966, Sukaraja, Sukabumi</dd>
      <dt>Istri</dt><dd>Dr. Hj. Netty Prasetiyani, S.Si., M.Si.</dd>
      <dt>Anak</dt><dd>8 orang</dd>
      <dt>Pendidikan</dt><dd>S1 LIPIA, S2 IPB, S3 Unpad</dd>
      <dt>Jabatan kini</dt><dd>Ketua BAM DPR RI, Anggota DPR RI Dapil Jabar II</dd>
    </dl>
  </div>
</section>

<section class="alt beranda-lini" aria-labelledby="h-babak">
  <div class="wrap dua">
    <div class="sec-head">
      <h2 id="h-babak">Enam babak perjalanan</h2>
      <p>Dari bangku sekolah di Sukabumi, parlemen Jakarta, sepuluh tahun di Gedung Sate, sampai memimpin Badan Aspirasi Masyarakat DPR RI.</p>
      <a class="btn lanjut" href="/perjalanan/">Ikuti perjalanan lengkap {ik("panah", "c2")}</a>
    </div>
    {sate}
  </div>
</section>

<section aria-labelledby="h-prog">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-prog">Yang dikerjakan untuk Jawa Barat</h2>
      <p>Tujuh bidang kerja selama 2008–2018. Pilih bidang untuk membaca rinciannya.</p>
    </div>
    <div class="ubin-grid">{"".join(tiles)}</div>
  </div>
</section>

<section class="rak beranda-prestasi" aria-labelledby="h-pres">
  <div class="wrap dua">
    <div class="sec-head">
      <span class="angka-besar" aria-hidden="true">206</span>
      <h2 id="h-pres">Penghargaan untuk Jawa Barat</h2>
      <p>Tercatat 206 penghargaan untuk Pemprov Jabar sepanjang 2008–2016, ditambah 13 tanda kehormatan dan gelar pribadi.</p>
      <div class="cta-row">
        <a class="btn" href="/penghargaan/">Lihat 206 penghargaan</a>
        <a class="btn ghost" href="/penghargaan/#tanda-kehormatan">Tanda kehormatan</a>
      </div>
    </div>
    <ul class="lencana lencana-pilihan">{lenc}</ul>
  </div>
</section>

<section aria-labelledby="h-kabar">
  <div class="wrap">
    <div class="sec-head baris-kepala">
      <div>
        <h2 id="h-kabar">Kabar terbaru</h2>
        <p>Kiprah Kang Aher sebagai Ketua Badan Aspirasi Masyarakat DPR RI.</p>
      </div>
      <a class="btn lanjut" href="/kabar/">Semua kabar {ik("panah", "c4")}</a>
    </div>
    <div class="kabar-grid">{kabar}</div>
  </div>
</section>

<section class="alt beranda-medsos" aria-labelledby="h-ms">
  <div class="wrap dua">
    <div class="sec-head">
      <h2 id="h-ms">Ikuti di media sosial</h2>
      <p>Kabar harian, video kegiatan, dan pesan Kang Aher ada di enam akun ini.</p>
      <a class="btn lanjut" href="/medsos/">Lihat feed terbaru {ik("panah", "c5")}</a>
    </div>
    <div class="bio-kartu k-sosmed">{akun}</div>
  </div>
</section>

{part("sebar.html")}'''


# ---------------------------------------------------------------- kabar
def kartu_kabar(k):
    t = k.get("tanggal_teks") or tgl(k["tanggal"])
    return f'''<a class="kartu-kabar" href="/kabar/{k["slug"]}/">
  <time datetime="{k["tanggal"]}">{t}</time>
  <h3>{k["judul"]}</h3>
  <p>{k["ringkas"]}</p>
  <span class="baca">Baca kabar {ik("panah", "c4")}</span>
</a>'''


def kabar_index_html():
    return f'''<section class="kabar-daftar" aria-label="Daftar kabar">
  <div class="wrap">
    <div class="kabar-grid">{"".join(kartu_kabar(k) for k in KABAR)}</div>
    <p class="catatan-kecil">Setiap kabar adalah ringkasan dengan bahasa kami sendiri; tautan sumber aslinya tercantum di akhir artikel.</p>
  </div>
</section>
'''


def artikel_html(k, i):
    t = k.get("tanggal_teks") or tgl(k["tanggal"])
    isi = "\n".join(f"      <p>{p}</p>" for p in k["isi"])
    sumber = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{n}</a></li>' for n, u in k["sumber"])
    lain = [x for j, x in enumerate(KABAR) if j != i][:3]
    return f'''<section class="artikel-wrap">
  <div class="wrap artikel-grid">
    <article class="artikel">
{isi}
      <div class="sumber-artikel">
        <h2>Sumber</h2>
        <ul>{sumber}</ul>
      </div>
    </article>
    <aside class="kabar-lain" aria-label="Kabar lainnya">
      <h2>Kabar lainnya</h2>
      {"".join(kartu_kabar(x) for x in lain)}
      <a class="btn lanjut" href="/kabar/">Semua kabar {ik("panah", "c4")}</a>
    </aside>
  </div>
</section>
'''


# ---------------------------------------------------------------- rakit
def rakit(path, head, aktif, body, data=False):
    out = head + header_html(aktif) + '\n<main id="isi">\n' + body + "\n</main>\n" + kaki_html(data).replace("{BAWAH}", bawah_html(aktif))
    return out


def tulis(path, isi):
    f = PUB / path.strip("/") / "index.html" if path != "/" else PUB / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(isi, encoding="utf-8")


def main():
    # isi tiap halaman
    isi = {}
    for key, h in HAL.items():
        if key == "kabar":
            isi[key] = kabar_index_html()
        else:
            isi[key] = "\n".join(part(p) for p in h["parts"])
    peta = kumpulkan_id(isi)
    peta["sekilas"] = ("beranda", "/")

    urls = [("/", HARI_INI)]

    # beranda
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": DOMAIN + "/#situs", "name": "Sahabat Kang Aher", "alternateName": "SKA", "url": DOMAIN + "/", "inLanguage": "id"},
        {"@type": "ProfilePage", "url": DOMAIN + "/", "name": "Sahabat Kang Aher", "mainEntity": dict(PERSON, sameAs=[
            "https://id.wikipedia.org/wiki/Ahmad_Heryawan", "https://www.instagram.com/aheryawan/", "https://www.tiktok.com/@aheryawanofficial",
            "https://www.facebook.com/aheryawan", "https://www.youtube.com/@aheryawan", "https://x.com/aheryawan", "https://www.threads.com/@aheryawan"])}]}
    head = head_html("Sahabat Kang Aher (SKA) | Profil, Perjalanan &amp; Prestasi Ahmad Heryawan",
                     "Sahabat Kang Aher (SKA), situs komunitas tentang Ahmad Heryawan: dua periode Gubernur Jawa Barat 2008–2018, 206 penghargaan, program untuk Jabar, hingga kini Ketua Badan Aspirasi Masyarakat DPR RI.",
                     "/", "/og.png", jsonld=jsonld)
    body = tulis_ulang_tautan(beranda_html(), peta, "beranda")
    tulis("/", rakit("/", head, "beranda", body))

    # halaman
    for key, h in HAL.items():
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "url": DOMAIN + h["path"], "name": h["title"], "about": {"@id": DOMAIN + "/#kang-aher"}, "isPartOf": {"@id": DOMAIN + "/#situs"}},
            breadcrumb_ld([("Beranda", "/"), (h["nav"], h["path"])])]}
        if key == "profil":
            ld["@graph"][0]["@type"] = "ProfilePage"
            ld["@graph"][0]["mainEntity"] = PERSON
            ld["@graph"].append(faq_ld())
        head = head_html(h["title"], h["desc"], h["path"], f"/og/{key}.png", jsonld=ld)
        body = kepala_hal(h["h1"], h["lead"], [(h["nav"], None)]) + isi[key] + "\n" + (tanya_html() if key == "profil" else "") + part("sebar.html")
        body = tulis_ulang_tautan(body, peta, key)
        tulis(h["path"], rakit(h["path"], head, key, body, h.get("data", False)))
        urls.append((h["path"], HARI_INI))

    # artikel kabar
    for i, k in enumerate(KABAR):
        path = f"/kabar/{k['slug']}/"
        desc = html.unescape(k["ringkas"]).replace('"', "&quot;")
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "NewsArticle", "headline": html.unescape(k["judul"]), "datePublished": k["tanggal"], "description": html.unescape(k["ringkas"]),
             "url": DOMAIN + path, "image": DOMAIN + "/og/kabar.png", "about": {"@id": DOMAIN + "/#kang-aher"},
             "author": {"@type": "Organization", "name": "Sahabat Kang Aher", "url": DOMAIN + "/"},
             "publisher": {"@type": "Organization", "name": "Sahabat Kang Aher", "logo": {"@type": "ImageObject", "url": DOMAIN + "/icon-512.png"}},
             "isBasedOn": [u for _, u in k["sumber"]]},
            breadcrumb_ld([("Beranda", "/"), ("Kabar", "/kabar/"), (html.unescape(k["judul"]), path)])]}
        head = head_html(f'{k["judul"]} | Sahabat Kang Aher', desc, path, "/og/kabar.png", og_type="article", jsonld=ld)
        t = k.get("tanggal_teks") or tgl(k["tanggal"])
        body = kepala_hal(k["judul"], k["ringkas"], [("Kabar", "/kabar/"), ("Artikel", None)],
                          extra=f'\n    <p class="meta-artikel"><time datetime="{k["tanggal"]}">{t}</time></p>')
        body += artikel_html(k, i) + "\n" + part("sebar.html")
        body = tulis_ulang_tautan(body, peta, "kabar")
        tulis(path, rakit(path, head, "kabar", body))
        urls.append((path, k["tanggal"]))

    # 404
    head = head_html("Halaman tidak ditemukan | Sahabat Kang Aher", "Halaman yang Anda cari tidak ada.", "/404", "/og.png")
    body = kepala_hal("Halaman tidak ditemukan", "Alamatnya mungkin salah ketik, atau halamannya sudah dipindah.", [("404", None)],
                      extra='\n    <div class="cta-row" style="margin-top:1.5rem"><a class="btn" href="/">Kembali ke beranda</a><a class="btn ghost" href="/kabar/">Baca kabar terbaru</a></div>')
    (PUB / "404.html").write_text(rakit("/404", head.replace('<link rel="canonical" href="' + DOMAIN + '/404">\n', '<meta name="robots" content="noindex">\n'), "", tulis_ulang_tautan(body, peta, "")), encoding="utf-8")

    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, d in urls:
        sm.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{d}</lastmod></url>")
    sm.append("</urlset>")
    (PUB / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    print(f"selesai: {len(urls)} halaman, versi {VER}")


if __name__ == "__main__":
    main()
