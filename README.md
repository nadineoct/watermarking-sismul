# Tugas Watermarking Sismul
Dikerjakan oleh: **Nadine Arindy Octavia**  
NIM: **18224012**

## Struktur Project
```text
watermarking-sismul/
├── data/                  # Foto wajah dan logo watermark (Input)
├── tool/                  # Script Python untuk pemrosesan
│   └── run_experiment.py  # Script utama eksperimen
├── hasil_deliverable/     # Hasil gambar watermark yang diekstrak (QF 100-0)
└── README.md              # Dokumentasi ini
```

## Deskripsi Tugas
Project ini mengimplementasikan teknik **Digital Watermarking** menggunakan metode **Least Significant Bit (LSB)** dengan optimasi bit redundansi dan sistem voting untuk ketahanan terhadap kompresi JPEG.

### Alur Kerja
1.  **Embedding**: Menyisipkan bit logo watermark ke dalam bit ke-3 (Bit Position 3) pada kanal hijau gambar asli.
2.  **Compression**: Simulasi kompresi JPEG manual menggunakan DCT (Discrete Cosine Transform) dengan berbagai Quality Factor (QF) dari 100 hingga 0.
3.  **Extraction**: Mengambil kembali bit watermark dari gambar yang terkompresi menggunakan sistem voting pada blok piksel untuk meminimalkan error.

## Cara Menjalankan
1. Letakkan foto wajah Anda dengan nama `face.jpeg` di folder `data/`.
2. Letakkan logo watermark Anda dengan nama `logo_watermark.png` di folder `data/`.
3. Jalankan script:
   ```bash
   python tool/run_experiment.py
   ```
4. Cek hasil ekstraksi di folder `hasil_deliverable/`.
