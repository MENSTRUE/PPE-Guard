# PPE-Guard — Panduan Lengkap (Bahasa Indonesia)

**Proyek Day 21 · 100 Days of Projects** — sistem berbasis AI untuk mendeteksi objek terkait Alat Pelindung Diri (APD/PPE) pada foto dan membantu pemeriksa manusia meninjau temuan. **Bukan alat sertifikasi K3, bukan penentu otomatis pelanggaran, dan bukan sistem penilaian kepatuhan per pekerja.**

## 1. Before → Now → Next

**Before:** audit dua dataset, penyatuan target 12 kelas, pelatihan YOLOv8s dan evaluasi held-out. **Now:** bobot `.pt` dan `.onnx`, FastAPI inference nyata, React/TypeScript UI, JSON laporan dan contoh anotasi telah tersedia di repo. **Next:** uji browser build, metrik per kelas, deteksi duplikasi lintas split, evaluasi domain baru, uji paritas ONNX, perlindungan data, deployment yang diamankan.

## 2. Sumber kebenaran (source of truth)

Untuk jumlah gambar/kelas, periksa `reports/final_summary.json`, `selection_audit.json`, dan `annotation_inventory.json`. Untuk metrik, periksa `reports/heldout_metrics.json`. Untuk perilaku inference, baca `backend/app/` dan `frontend/src/`. Mapping kelas yang dibekukan ada di `backend/app/inference/contract.py` dan diverifikasi ulang terhadap model sesungguhnya saat dimuat. Pernyataan naratif tidak boleh menimpa fakta dari kode/artefak.

## 3. Dataset dan audit

Lokasi Kaggle asal tercatat: `/kaggle/input/datasets/loliwibu/ppe-guard-datset` (penulisan `datset` sesuai path asli). Dua sumber:

1. `Hard Hat Workers.v14-raw_headclassonly.yolov8` — anotasi awal hanya `head`.
2. `construction-ppe` — 11 kelas sumber termasuk `Person` yang dinormalisasi ke `person`.

**8.451 gambar** digunakan pada tahap staging: **6.048 train, 1.556 validation, 847 test**. Inventaris melaporkan **10 orphan labels** (label tanpa pasangan gambar yang teridentifikasi). Audit pemilihan mencatat 8.451 gambar eligible dan selected; ini **bukan** bukti bahwa orphan labels sudah terselesaikan atau tidak ada data leakage. Perlu audit hash serta perceptual hash lintas split dan telaah kemiripan sekuens/sumber.

**Distribusi box:** `head` 26.424; `person` 2.245; `helmet` 1.734; `vest` 1.618; `boots` 1.597; `gloves` 1.445; `none` 797; `no_gloves` 556; `goggles` 518; `no_helmet` 485; `no_goggle` 411; `no_boots` 115. Hitungan ini adalah **box anotasi**, bukan pekerja atau insiden. Ketidakseimbangan dan perbedaan ontologi kedua sumber berisiko menciptakan partial labels.

## 4. Model dan metrik

Model eksperimen: `yolov8s.pt` (lihat `reports/final_summary.json`). Bobot serving: `models/ppe_guard_best.pt`, artefak ekspor: `models/ppe_guard_best.onnx` (belum ada bukti paritas output dan belum dipakai API).

| Metrik held-out (847 gambar) | Nilai |
|---|---:|
| Precision | **63,06%** |
| Recall | **53,93%** |
| mAP@50 | **55,49%** |
| mAP@50:95 | **29,19%** |

Metrik tersebut bersumber dari `reports/heldout_metrics.json` (angka dibulatkan), **bukan accuracy keselamatan**, bukan evaluasi pekerja individual, dan bukan bukti generalisasi ke seluruh lokasi konstruksi. Belum ada metrik per kelas/kalibrasi atau validasi lintas domain yang memadai.

## 5. Dua belas kelas dan batas klaim

```text
0 helmet       1 no_helmet     2 vest       3 boots
4 gloves       5 goggles       6 head       7 no_boots
8 no_gloves    9 no_goggle    10 none      11 person
```

`head` **tidak sama** dengan `no_helmet`; `none` **bukan** status semua APD tidak digunakan; `person` tidak mengenali identitas orang; kelas `no_*` hanya **indikasi berlabel sumber yang harus ditinjau**. Tidak terdeteksinya helm juga bukan bukti helm tidak ada. Kode API mengembalikan `compliance_status="not_assessed"` sebab belum ada asosiasi APD ke pekerja tertentu maupun konteks kebijakan lokasi kerja. Risiko negatif palsu/positif palsu harus selalu diakui.

## 6. Arsitektur dan alur

React/Vite → unggah JPEG/PNG/WebP + threshold → FastAPI `/api/v1/predict/image` → pemeriksaan format/ukuran → YOLO `.pt` → box/class/confidence → rangkuman observasi yang hati-hati → JSON + gambar JPEG Base64 opsional → tampilan/ekspor frontend. Default threshold `0.25`; `1.0` dapat menyaring hampir semua box.

Struktur utama: `backend/` (API), `frontend/` (UI), `models/` (checkpoint), `reports/` (evidence), `assets/` (contoh/diagram), `scripts/` (smoke test), `docs/` (panduan), `AGENTS.md` (aturan kontribusi). Lihat README root untuk pohon terperinci.

## 7. Menjalankan secara lokal (Windows)

Terminal backend:

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe ..\scripts\smoke_model.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Terminal frontend:

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\frontend"
npm ci
npm run build
npm run dev
```

Buka `http://127.0.0.1:5173` dan `http://127.0.0.1:8000/docs`. Coba foto APD jelas dengan confidence 0.25 dan `include_annotated=true`. Hasil deteksi tidak perlu selalu positif; evaluasi isi box secara visual. `GET /health` menunjukkan API hidup, bukan jaminan checkpoint dapat dipakai.

## 8. Testing, reproduksibilitas, dan privasi

Sebelumnya pengujian backend lokal melaporkan **9 passed, 1 warning**, tetapi tes API menggunakan mock inference pada kasus tertentu. Validasi bobot asli dan gambar nyata harus terpisah. Belum ada kepastian tes browser otomatis, CI publik, atau deploy produksi. Untuk mengulang eksperimen training diperlukan notebook Kaggle, versi dataset, konfigurasi, seed, dependency lock, checkpoint selection dan manifest; laporan saja belum cukup.

Unggahan gambar diproses sementara di memori backend yang sekarang, namun untuk produksi wajib menambah auth, TLS, rate limit, kebijakan retensi, kontrol akses dan perlindungan data pribadi. `.pt` hanya boleh dimuat dari sumber tepercaya karena risiko deserialisasi.

## 9. Roadmap

**P0:** validasi end-to-end dan dokumentasi kontrak. **P1:** audit orphan/near-duplicate, metrik per kelas, evaluasi domain baru, penyesuaian overlay aspect-ratio, paritas ONNX. **P2:** autentikasi, deployment hardened, monitoring, versi model. **P3:** streaming dan asosiasi APD-ke-orang jika tersedia metodologi/data valid. Semuanya yang berstatus roadmap **belum boleh diklaim sebagai fitur selesai**.

## 10. Troubleshooting

| Gejala | Solusi awal |
|---|---|
| `SyntaxError` docstring smoke script | Pastikan tiga tanda kutip `"""` penutup; gunakan versi repo terkini |
| `ModuleNotFoundError` | Pakai Python dalam `backend/.venv` dan install requirements |
| Checkpoint tidak ditemukan | Cek `models/ppe_guard_best.pt` |
| HTTP 503 | Baca log backend, jalankan smoke test |
| HTTP 413/415/422 | Ukuran terlalu besar, MIME/format salah, atau gambar korup |
| Deteksi kosong `confidence=1` | Coba 0.25; belum tentu model akan mendeteksi |
| Frontend terputus | Hidupkan backend port 8000 dan cek Vite proxy/env |
| Box meleset | Cek scaling/letterbox; gunakan gambar anotasi dari server |
| Git menyimpan file besar | Evaluasi Git LFS/Releases dan izin distribusi bobot |

## 11. FAQ

**Apakah semua pekerja otomatis diklasifikasi aman/tidak?** Tidak. Sistem hanya menampilkan prediksi objek. **Apakah `no_helmet` membuktikan pelanggaran?** Tidak, hanya label prediksi yang perlu diperiksa. **Apakah ONNX dipakai backend?** Saat ini tidak, `.pt` yang dipakai. **Apakah model bisa dipakai secara komersial?** Hak penggunaan kode, sumber data, bobot model, dan ketentuan Ultralytics harus diperiksa terpisah.

## 12. Lisensi dan kontribusi

Akar repo memiliki `LICENSE` **MIT** untuk kode/dokumentasi yang haknya dimiliki penerbit; jangan menganggap lisensi MIT otomatis mencakup dataset pihak ketiga, foto, atau bobot pretrained/model turunan. Periksa atribusi/ketentuan sumber sebelum distribusi. Semua kontribusi mengikuti `../../AGENTS.md`, dan perubahan harus menyertakan bukti tes, Before–Now–Next, dan pembaruan README terkait.
