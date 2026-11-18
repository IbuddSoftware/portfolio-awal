# Portfolio Website — Mohamad Budi Wibowo

Website portofolio pribadi yang dibangun menggunakan Python Flask dan PostgreSQL. Website ini memiliki halaman publik untuk menampilkan informasi diri, pendidikan, pengalaman organisasi, keterampilan, dan proyek. Tersedia juga halaman admin untuk mengelola konten portofolio.

## 1. Teknologi yang Digunakan

- **Python** — bahasa pemrograman utama.
- **Flask** — framework backend.
- **HTML, CSS, JavaScript** — membangun tampilan website.
- **PostgreSQL (Neon)** — database penyimpanan data.
- **Flask-SQLAlchemy** — menghubungkan Flask dengan database.
- **Psycopg** — driver koneksi PostgreSQL.
- **Gunicorn** — server aplikasi untuk deployment.

## 2. Fitur Website

### Halaman Publik
- Menampilkan profil pribadi.
- Menampilkan riwayat pendidikan.
- Menampilkan pengalaman organisasi.
- Menampilkan keterampilan atau skills.
- Menampilkan proyek portofolio.
- Menampilkan informasi kontak dan media sosial.

### Halaman Admin
- Login dan logout administrator.
- Dashboard pengelolaan portofolio.
- Menambahkan, melihat, mengubah, dan menghapus data proyek.
- Menambahkan, melihat, mengubah, dan menghapus data keterampilan.
- Menambahkan, melihat, mengubah, dan menghapus data pengalaman.
- Mengubah informasi profil.

## 3. Struktur Folder

```text
portfolio_awal/
│
├── app.py
├── config.py
├── extensions.py
├── models.py
├── init_db.py
├── test_db.py
├── seed_data.py
├── create_admin.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── Procfile
│
├── templates/
│   ├── index.html
│   │
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── projects.html
│       ├── project_form.html
│       ├── skills.html
│       ├── skill_form.html
│       ├── experiences.html
│       ├── experience_form.html
│       └── profile_form.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── main.js
    │
    └── images/
```

## 4. Persiapan Lingkungan

Pastikan perangkat sudah memiliki:

1. Python.
2. Visual Studio Code.
3. Git.
4. Akun GitHub.
5. Akun Neon untuk database PostgreSQL.

Buka folder proyek melalui Visual Studio Code, kemudian buka terminal.

### Membuat Virtual Environment

Jalankan perintah:

```bash
python -m venv .venv
```

Aktifkan virtual environment di Windows:

```bash
.venv\Scripts\activate
```

### Menginstal Dependencies

```bash
pip install -r requirements.txt
```

Dependencies yang digunakan terdapat di dalam `requirements.txt`.

## 5. Konfigurasi Database Neon

Database menggunakan PostgreSQL yang di-host melalui Neon.

Langkah konfigurasi:

1. Buat proyek database di Neon.
2. Pilih database `portofolio-db`.
3. Pilih role database yang digunakan.
4. Buka menu **Connect**.
5. Salin connection string PostgreSQL.
6. Masukkan connection string ke file `.env`.

Contoh isi file `.env`:

```env
DATABASE_URL=postgresql://username:password@host/database?sslmode=require
SECRET_KEY=ganti_dengan_kunci_rahasia
FLASK_DEBUG=true
COOKIE_SECURE=false
```

**Catatan:** Contoh di atas hanya format. Gunakan connection string dan kunci rahasia milik sendiri. Jangan membagikan atau mengunggah file `.env` ke GitHub.

## 6. Pembuatan Database dan Tabel

Setelah konfigurasi database selesai, lakukan pengujian koneksi:

```bash
python test_db.py
```

Jika koneksi berhasil, buat tabel menggunakan:

```bash
python init_db.py
```

Pembuatan tabel menggunakan model yang didefinisikan dalam `models.py`.

Tabel yang digunakan meliputi:

| Tabel | Fungsi |
|---|---|
| `profile` | Menyimpan informasi profil |
| `skills` | Menyimpan keterampilan |
| `education` | Menyimpan riwayat pendidikan |
| `experiences` | Menyimpan pengalaman organisasi |
| `projects` | Menyimpan proyek portofolio |
| `admins` | Menyimpan akun administrator |

## 7. Mengisi Data Awal

Setelah tabel berhasil dibuat, jalankan:

```bash
python seed_data.py
```

File tersebut digunakan untuk memasukkan data awal portofolio ke dalam database.

Data dapat diperiksa melalui dashboard Neon atau melalui aplikasi database seperti DBeaver.

## 8. Membuat Akun Administrator

Untuk membuat akun administrator, jalankan:

```bash
python create_admin.py
```

Ikuti instruksi pada terminal untuk memasukkan username dan password administrator.

Password disimpan dalam bentuk hash, bukan sebagai teks biasa.

## 9. Menjalankan Website Secara Lokal

Setelah seluruh konfigurasi selesai, jalankan aplikasi:

```bash
python app.py
```

Buka browser dan akses:

```text
http://127.0.0.1:5000
```

Untuk membuka halaman administrator:

```text
http://127.0.0.1:5000/admin/login
```

Login menggunakan akun administrator yang telah dibuat.

## 10. Pengelolaan Data melalui Admin

Setelah berhasil login, administrator dapat mengelola beberapa bagian portofolio.

| Menu | Kegunaan |
|---|---|
| Dashboard | Melihat ringkasan data |
| Projects | Mengelola proyek |
| Skills | Mengelola keterampilan |
| Experiences | Mengelola pengalaman organisasi |
| Profile | Mengubah informasi profil |

Perubahan data yang dilakukan melalui halaman admin akan disimpan ke database PostgreSQL Neon.

## 11. Deployment ke Railway

Website direncanakan untuk di-deploy menggunakan Railway, sedangkan database tetap menggunakan Neon PostgreSQL.

### Persiapan GitHub

Pastikan file `.gitignore` memiliki aturan berikut:

```gitignore
.env
.venv/
venv/
__pycache__/
*.py[cod]
instance/
.pytest_cache/
```

Pastikan `.env` tidak ikut diunggah ke GitHub.

Jalankan perintah:

```bash
git init
git add .
git status
git commit -m "Persiapan deployment portfolio"
git branch -M main
git remote add origin https://github.com/USERNAME/portfolio-awal.git
git push -u origin main
```

Ganti `USERNAME` dengan username GitHub sendiri.

### Konfigurasi Railway

1. Login ke Railway.
2. Pilih **New → Web Service**.
3. Hubungkan repository GitHub.
4. Pilih repository `portfolio-awal`.
5. Gunakan konfigurasi berikut:

| Pengaturan | Nilai |
|---|---|
| Language | Python 3 |
| Branch | main |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

### Environment Variables

Tambahkan variabel lingkungan berikut melalui dashboard Railway:

| Key | Value |
|---|---|
| `DATABASE_URL` | Connection string dari Neon |
| `SECRET_KEY` | Kunci rahasia baru |
| `COOKIE_SECURE` | `true` |
| `FLASK_DEBUG` | `false` |

Setelah konfigurasi selesai, lakukan deployment.

## 12. Keamanan Proyek

Beberapa hal yang perlu diperhatikan:

- File `.env` tidak boleh diunggah ke GitHub.
- Gunakan `SECRET_KEY` yang kuat dan tidak dibagikan.
- Password administrator harus disimpan dalam bentuk hash.
- Halaman admin dilindungi menggunakan autentikasi.
- Formulir yang mengubah data menggunakan validasi CSRF.
- Gunakan HTTPS saat website sudah dipublikasikan.

## 13. Status Pengembangan

- [x] Membuat struktur proyek Flask.
- [x] Mengatur virtual environment dan dependencies.
- [x] Menghubungkan Flask dengan Neon PostgreSQL.
- [x] Membuat model database.
- [x] Membuat tabel database.
- [x] Memasukkan data awal portofolio.
- [x] Membuat autentikasi administrator.
- [x] Membuat dashboard admin.
- [x] Membuat CRUD proyek.
- [x] Membuat CRUD keterampilan.
- [x] Membuat CRUD pengalaman organisasi.
- [x] Membuat halaman pengelolaan profil.
- [x] Mengunggah proyek ke GitHub.
- [x] Melakukan deployment ke Railway.
- [x] Menguji website setelah deployment.

---

**Dibuat oleh:** Mohamad Budi Wibowo  
**Proyek:** Website Portofolio Pribadi  
**Backend:** Python Flask  
**Database:** PostgreSQL Neon  
**Deployment:** Render
