# Digital Image Watermarking: Robust LSB & JPEG DCT Simulation

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Library-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)

Repositori ini mengimplementasikan sistem *Digital Image Watermarking* yang tangguh menggunakan metode **Robust LSB** dan simulasi kompresi JPEG berbasis **Discrete Cosine Transform (DCT)**. Proyek ini bertujuan untuk menyisipkan identitas digital ke dalam citra secara tidak kasat mata (*invisible*) namun tetap bertahan terhadap manipulasi kompresi.

---

## 🚀 Quick Demo

Berikut adalah ringkasan hasil penyisipan dan ekstraksi watermark pada kondisi ideal:

| Citra Host (Original) | Watermark Logo | Citra Ter-watermark | Hasil Ekstraksi |
|:---:|:---:|:---:|:---:|
| <img src="data/face.jpeg" width="200"> | <img src="data/barbie_logo.png" width="200"> | <img src="Hasil/watermarked/watermarked_BASE.png" width="200"> | <img src="Hasil/extracted/qf_experiment/extracted_qf100.png" width="200"> |

---

## 🛠️ Alur Kerja Sistem (Workflow)

Sistem ini mengikuti proses pipeline yang terbagi menjadi tahap *Embedding* dan *Extraction*. Berikut adalah penjelasan visual tiap tahap:

### 1. Pre-processing & Binarization
Watermark logo dikonversi menjadi citra biner (0 dan 1). Hal ini dilakukan untuk meminimalkan data yang disisipkan dan memungkinkan penggunaan teknik *Voting* saat ekstraksi.

<p align="center">
  <img src="Hasil/step1_binarization.png" width="500">
  <br><i>Transformasi logo asli menjadi representasi bit biner 64x64.</i>
</p>

### 2. Robust LSB Embedding
Alih-alih menggunakan LSB standar (Bit-0), sistem ini menyisipkan data pada **Bit ke-3**. Secara visual, perubahan ini tetap tidak terdeteksi oleh mata manusia (*imperceptible*), namun memiliki ketahanan yang jauh lebih tinggi terhadap pembulatan nilai akibat kompresi JPEG.

<p align="center">
  <img src="Hasil/step2_embedding_zoom.png" width="500">
  <br><i>Perbandingan host original vs watermarked pada area zoom. Perbedaan tidak terlihat secara visual.</i>
</p>

### 3. Spatial Redundancy (3x3 Block)
Setiap 1 bit dari watermark disebarkan ke dalam blok **3x3 piksel** pada kanal Hijau (Green) citra host. Redundansi ini berfungsi sebagai proteksi; jika satu piksel rusak akibat kompresi, bit asli masih bisa diselamatkan melalui piksel lainnya dalam blok yang sama.

<p align="center">
  <img src="Hasil/step3_redundancy_diagram.png" width="250">
  <br><i>Skema penyebaran 1 bit watermark ke dalam 9 piksel host.</i>
</p>

### 4. JPEG Compression Attack (DCT Manual)
Citra diuji dengan kompresi JPEG yang diimplementasikan secara manual menggunakan blok 8x8 dan transformasi DCT untuk mensimulasikan pembuangan informasi frekuensi tinggi.

<p align="center">
  <img src="Hasil/step4_dct_visualization.png" width="500">
  <br><i>Visualisasi transformasi blok piksel dari domain spasial ke domain frekuensi (DCT).</i>
</p>

### 5. Extraction & Majority Voting
Pada tahap ekstraksi, bit-bit dibaca dari posisi Bit-3. Untuk setiap blok 3x3, dilakukan **Majority Voting** (pengambilan suara terbanyak) untuk menentukan apakah bit tersebut bernilai 0 atau 1.

![Watermark Extraction Comparison](Hasil/exp1_watermark_extraction.png)
<p align="center"><i>Hasil pemulihan watermark setelah melewati berbagai tingkat kompresi.</i></p>

---

---

## 📊 Evaluasi Performa

Ketahanan sistem diuji terhadap berbagai tingkat kompresi JPEG (*Quality Factor* 10 hingga 100).

### Perbandingan Ekstraksi vs QF
Semakin rendah QF, citra akan semakin terkompresi (ukuran file mengecil), namun tingkat kesalahan ekstraksi (BER) akan meningkat.

![Watermark Extraction Comparison](Hasil/exp1_watermark_extraction.png)

### Analisis Statistik
Metrik yang digunakan adalah **PSNR** (kualitas visual citra) dan **BER** (tingkat kesalahan bit).

<p align="center">
  <img src="Hasil/exp1_table.png" width="600">
</p>

![Metrics Chart](Hasil/exp1_ber_psnr_chart.png)

---

## 💻 Cara Menjalankan

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/username/watermarking-sismul.git
   cd watermarking-sismul
   ```

2. **Instalasi Dependensi:**
   ```bash
   pip install opencv-python numpy matplotlib scipy
   ```

3. **Jalankan Notebook:**
   Buka `tool/watermarking_analysis.ipynb` menggunakan Jupyter Notebook atau VS Code dan jalankan semua sel secara berurutan.

---

## 📝 Informasi Proyek
- **Mata Kuliah:** II2240 Sistem Multimedia
- **Teknik Utama:** Robust LSB, DCT-based JPEG Simulation, Majority Voting.
- **Pustaka Utama:** OpenCV, NumPy, Matplotlib, SciPy.

---
*Dibuat untuk tujuan edukasi dalam memahami konsep Digital Watermarking dan Kompresi Citra.*
