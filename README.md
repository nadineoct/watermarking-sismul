# Digital Watermarking: LSB Optimization & JPEG Robustness Analysis

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

Proyek ini mengimplementasikan teknik *digital watermarking* menggunakan metode **Least Significant Bit (LSB)** yang dioptimasi untuk ketahanan terhadap kompresi JPEG. Analisis difokuskan pada korelasi antara *Quality Factor* JPEG dengan integritas watermark (*Bit Error Rate*) dan kualitas visual citra (*PSNR*).

## Informasi Mahasiswa
- **Nama:** Nadine Arindy Octavia
- **NIM:** 18224012
- **Mata Kuliah:** Sistem Multimedia

## Fitur Utama
- **LSB Optimization:** Penggunaan Bit ke-3 dan sistem redundansi blok 3x3 untuk meningkatkan *robustness*.
- **Majority Voting System:** Mekanisme *error correction* sederhana pada tahap ekstraksi bit.
- **Manual JPEG Simulation:** Simulasi kompresi JPEG menggunakan *Discrete Cosine Transform* (DCT) dan kuantisasi kustom.
- **Visualisasi Data:** Analisis blok piksel 8x8 dan perbandingan metrik performa secara otomatis.

## Struktur Folder
```text
C:\Users\hp\watermarking-sismul\
├── data\                             # Output eksperimen (grafik, tabel, citra ekstraksi)
├── Hasil\                            # Citra input (host image & logo watermark)
├── tool\
│   └── watermarking_analysis.ipynb   # Notebook utama eksperimen
├── Nadine Arindy Octavia_18224012_Laporan Hasil Watermarking  # Draft laporan teknis
└── README.md                         # Informasi proyek
```

## Metodologi
1. **Embedding:** Menyisipkan bit watermark ke dalam blok 3x3 pada bit ke-3 komponen citra.
2. **Compression:** Melakukan kompresi JPEG manual dengan variasi *Quality Factor* (10-100).
3. **Extraction:** Mengambil kembali bit watermark menggunakan sistem voting mayoritas.
4. **Evaluation:** Menghitung nilai PSNR untuk kualitas citra dan BER untuk akurasi watermark.
