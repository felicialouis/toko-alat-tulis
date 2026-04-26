# 🖊️ Sistem Informasi Alat Tulis (SIMAT)

![Build Status](https://github.com/felicialouis/toko-alat-tulis/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)

Sistem manajemen inventori sederhana untuk toko alat tulis yang dibangun menggunakan Python dan Flask. Proyek ini dibuat untuk memenuhi tugas Final Project mata kuliah Pengujian Perangkat Lunak.

## 🚀 Fitur Utama
- **Manajemen Stok**: Menambah, memperbarui, dan menghapus data alat tulis.
- **Sistem Penjualan**: Mencatat transaksi penjualan dan otomatis memotong stok.
- **Laporan Laba**: Menghitung total pendapatan bersih secara otomatis.

## 🛠️ Cara Menjalankan Aplikasi
1. Clone repository ini.
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
3. Jalankan aplikasi:
   ```bash
   python run.py
4. Buka browser di (http://127.0.0.1:5000).

## 🧪 Cara Menjalankan Test
Gunakan perintah berikut untuk menjalankan seluruh test case dan melihat laporan coverage:
   ```bash
   python -m pytest --cov=app tests/ --cov-report=term-missing
   ```

## 🎯 Strategi Pengujian
Pengujian dilakukan dengan pendekatan Automated Testing yang mencakup:

1. **Unit Testing**: Menguji logika bisnis di logic.py secara mendalam (validasi input, perhitungan profit, integritas stok). Terdapat lebih dari 15 skenario test.
2. **Integration Testing**: Menguji alur aplikasi secara end-to-end melalui endpoint API/GUI di routes.py.
3. **Negative Testing**: Memastikan sistem mampu menangani input salah (stok negatif, nama kosong, dll) tanpa mengalami crash.
4. **Continuous Integration**: Menggunakan GitHub Actions untuk menjalankan testing secara otomatis setiap kali ada perubahan kode (push/pull request).
