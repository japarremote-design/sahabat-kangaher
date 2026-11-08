# fanskangaher.web.id

Landing page penggemar **Kang Aher (Ahmad Heryawan)**: profil, perjalanan karier, program untuk Jawa Barat, 206 penghargaan (bisa disaring per tahun & dicari), jejak pemilu, isu & klarifikasi, serta sumber.

Situs statis murni (HTML + CSS + JS, tanpa build). Semua file ada di folder `public/`.

## Jalankan lokal

```bash
npx serve public
```

## Deploy ke Cloudflare

**Opsi A: Workers (rekomendasi, sudah ada `wrangler.jsonc`)**
1. Cloudflare Dashboard → Workers & Pages → Create → Import a repository → pilih repo ini.
2. Build command: kosongkan. Deploy command: `npx wrangler deploy`.
3. Setelah live: Settings → Domains & Routes → Add → Custom domain → `fanskangaher.web.id`.

**Opsi B: Pages**
1. Workers & Pages → Create → Pages → Connect to Git → pilih repo ini.
2. Framework preset: None. Build command: kosong. Build output directory: `public`.
3. Custom domains → Set up a custom domain → `fanskangaher.web.id`.

Domain `.web.id` harus sudah aktif di Cloudflare (Add a domain → ganti nameserver di registrar ke nameserver Cloudflare).

## Sumber & lisensi

Isi diolah dari artikel [Ahmad Heryawan di Wikipedia bahasa Indonesia](https://id.wikipedia.org/wiki/Ahmad_Heryawan) (CC BY-SA 4.0), ditambah rujukan berita untuk jabatan di DPR RI. Teks situs berlisensi CC BY-SA 4.0.

Situs penggemar, **tidak resmi**, tidak berafiliasi dengan Ahmad Heryawan, PKS, maupun Pemprov Jawa Barat.

Dibuat oleh [Qfaz Digital](https://qfazdigital.my.id).
