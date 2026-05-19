# LAPORAN PROYEK: IMPLEMENTASI DAN ANALISIS KETAHANAN DIGITAL WATERMARKING LSB TERHADAP KOMPRESI JPEG

**Mata Kuliah:** Sistem Multimedia  
**Tanggal:** 19 Mei 2026  
**Disusun Oleh:**  
- **Nama:** Nadine Arindy Octavia  
- **NIM:** 18224012  

---

## 1. ABSTRAK
Laporan ini membahas implementasi teknik *digital watermarking* menggunakan metode *Least Significant Bit* (LSB) yang dioptimasi untuk menghadapi tantangan kompresi JPEG. Fokus utama eksperimen ini adalah menguji ketahanan watermark terhadap penurunan *Quality Factor* (QF) pada proses kompresi JPEG yang disimulasikan secara manual menggunakan *Discrete Cosine Transform* (DCT). Hasil eksperimen menunjukkan bahwa dengan penggunaan redundansi blok (3x3) dan sistem *voting*, watermark tetap dapat diekstraksi dengan baik hingga tingkat kompresi menengah.

---

## 2. PENDAHULUAN
### 2.1. Latar Belakang
Dalam era digital, perlindungan hak cipta konten multimedia menjadi krusial. *Digital watermarking* hadir sebagai solusi untuk menyisipkan informasi identitas ke dalam media digital. Namun, tantangan utama bagi metode spasial seperti LSB adalah kerentanannya terhadap manipulasi gambar, terutama kompresi *lossy* seperti JPEG.

### 2.2. Tujuan
1. Mengimplementasikan algoritma LSB dengan optimasi posisi bit dan redundansi.
2. Menganalisis korelasi antara *Quality Factor* JPEG dengan kualitas visual gambar (*PSNR*) dan integritas watermark (*Bit Error Rate* - BER).

---

## 3. LANDASAN TEORI
### 3.1. Least Significant Bit (LSB)
Metode LSB menyisipkan informasi pada bit-bit yang paling tidak signifikan dalam representasi biner piksel. Secara teori, mengubah LSB tidak akan memberikan perbedaan visual yang signifikan bagi mata manusia.

### 3.2. Kompresi JPEG dan DCT
JPEG menggunakan *Discrete Cosine Transform* (DCT) untuk mengubah representasi spasial piksel menjadi domain frekuensi. Informasi frekuensi tinggi (detail halus) kemudian dikurangi melalui proses kuantisasi berdasarkan tabel kuantisasi standar dan *Quality Factor*.

---

## 4. METODOLOGI IMPLEMENTASI
### 4.1. Optimasi Posisi Bit (Bit-3)
Berbeda dengan LSB konvensional yang menggunakan bit ke-0, sistem ini menggunakan **Bit ke-3**. Hal ini dilakukan karena bit yang terlalu rendah (0-2) sangat mudah hancur bahkan oleh kompresi JPEG ringan, sementara bit yang terlalu tinggi (4-7) akan merusak estetika visual gambar secara drastis.

### 4.2. Sistem Redundansi Blok (3x3)
Setiap 1 bit dari logo watermark disebarkan secara redundan ke dalam satu blok berukuran **3x3 piksel** pada gambar induk. Strategi ini meningkatkan peluang bit selamat dari proses kuantisasi frekuensi.

### 4.3. Mekanisme Voting (Majority Vote)
Pada tahap ekstraksi, bit ditentukan berdasarkan mayoritas nilai pada blok 3x3 tersebut. Jika rata-rata bit pada blok >= 0.5, maka bit dianggap 1, dan sebaliknya. Ini berfungsi sebagai mekanisme *error correction* sederhana namun efektif.

### 4.4. Simulasi Manual JPEG
Untuk pengujian yang akurat, digunakan simulasi JPEG manual yang melibatkan:
- Pemecahan gambar menjadi blok 8x8.
- Aplikasi Forward DCT.
- Kuantisasi menggunakan Tabel Luminansi Standar yang di-skala sesuai QF.
- Aplikasi Inverse DCT.

---

## 5. HASIL DAN PEMBAHASAN
*(Catatan: Bagian ini merujuk pada grafik yang dihasilkan oleh file `run_experiment.py` atau notebook `watermarking_analysis.ipynb`)*

### 5.1. Analisis Kuantitatif
Berdasarkan pengujian terhadap variasi QF (100, 90, 80, 70, 50, 30, 10), didapatkan tren sebagai berikut:
- **QF 100-70:** Menghasilkan BER 0.0 (Sempurna). PSNR berada pada level tinggi (>40 dB), menunjukkan kualitas gambar yang sangat baik.
- **QF 50-30:** Muncul sedikit bintik pada watermark hasil ekstraksi, namun logo masih sangat terbaca jelas. PSNR menurun namun tetap di atas batas toleransi visual.
- **QF 10:** Terjadi degradasi signifikan. Bit Error Rate (BER) meningkat tajam karena tabel kuantisasi membuang hampir seluruh informasi pada bit ke-3.

### 5.2. Visualisasi
| Quality Factor (QF) | Kondisi Visual Watermark | Interpretasi |
|---------------------|--------------------------|--------------|
| 100 | Sempurna | Tanpa Distorsi |
| 70 | Sangat Baik | Ketahanan Optimal |
| 50 | Terbaca | Batas Aman Kompresi |
| 10 | Noise Tinggi | Batas Kegagalan |

---

## 6. KESIMPULAN
Optimasi LSB menggunakan Bit-3 dan redundansi blok 3x3 terbukti efektif memberikan ketahanan (*robustness*) terhadap kompresi JPEG hingga tingkat menengah (QF 50). Meskipun metode domain frekuensi (seperti DWT/DCT watermarking) secara teori lebih kuat, pendekatan LSB yang dioptimasi ini menawarkan keseimbangan yang baik antara kemudahan implementasi dan performa untuk kebutuhan identifikasi standar.

---

## 7. DAFTAR PUSTAKA
1. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing*. Pearson.
2. Pennebaker, W. B., & Mitchell, J. L. (1992). *JPEG: Still Image Data Compression Standard*. Springer Science & Business Media.
