# LAPORAN TUGAS SISTEM MULTIMEDIA: DIGITAL WATERMARKING
**Disusun Oleh:**
- **Nama:** Nadine Arindy Octavia
- **NIM:** 18224012

---

## 1. Pendahuluan: Apa itu Watermarking?
Digital Watermarking adalah proses penyisipan informasi (disebut "watermark") ke dalam sinyal digital (seperti gambar, audio, atau video). Berbeda dengan steganografi yang bertujuan menyembunyikan keberadaan pesan, watermarking bertujuan untuk memberikan identitas, perlindungan hak cipta, atau bukti integritas pada media tersebut tanpa merusak kualitas visualnya secara signifikan.

## 2. Metode yang Digunakan: LSB (Least Significant Bit)
Dalam tugas ini, metode yang digunakan adalah **LSB (Least Significant Bit)** dengan beberapa optimasi tambahan:

### 2.1. Pemilihan Posisi Bit
Kita menggunakan **Bit ke-3** (dari 8 bit yang tersedia, yaitu 0-7). 
*   **Kenapa bukan Bit 0?** Bit 0 (paling belakang) sangat rentan hilang jika gambar dikompresi atau diubah sedikit saja.
*   **Kenapa Bit 3?** Bit 3 memberikan keseimbangan antara ketahanan (robustness) terhadap kompresi JPEG dan kualitas visual (invisibility).

### 2.2. Optimasi Redundansi & Voting System
Untuk meningkatkan ketahanan terhadap kompresi JPEG, algoritma ini tidak hanya menyimpan 1 bit watermark pada 1 piksel, melainkan:
1.  **Redundansi Blok:** Setiap 1 bit dari logo watermark disebarkan ke dalam blok piksel berukuran **3x3**.
2.  **Sistem Voting (Majority Vote):** Saat proses ekstraksi, algoritma akan melihat 9 piksel dalam blok tersebut. Jika mayoritas piksel menunjukkan bit 1, maka hasil ekstraksinya adalah 1. Ini sangat efektif untuk memperbaiki error kecil akibat kompresi.

## 3. Proses Kompresi JPEG
Tujuan dari tahap ini adalah menguji seberapa kuat watermark kita bertahan jika gambar disimpan dalam format JPEG.

### 3.1. Langkah-langkah Kompresi (Manual DCT)
Kompresi JPEG bekerja dengan cara:
1.  **DCT (Discrete Cosine Transform):** Mengubah data piksel menjadi frekuensi.
2.  **Kuantisasi:** Membuang frekuensi tinggi yang kurang terlihat oleh mata manusia. Di sinilah data watermark sering kali "rusak".
3.  **Quality Factor (QF):** Nilai dari 0 hingga 100 yang menentukan seberapa banyak data yang dibuang.

### 3.2. Tujuan Kompresi dalam Eksperimen
Eksperimen ini bertujuan untuk melihat titik hancur (breakdown point) dari algoritma LSB yang kita buat. Kita ingin tahu di QF berapa logo kita masih bisa dibaca dengan jelas oleh mata manusia.

## 4. Analisis Hasil Eksperimen
*(Bagian ini diisi setelah menjalankan script)*

*   **QF 100 - 70:** Gambar sangat jernih, watermark terkesan sempurna (BER mendekati 0).
*   **QF 50 - 30:** Mulai muncul artefak kompresi. Watermark mulai berbintik namun masih terbaca jelas berkat optimasi blok 3x3.
*   **QF 20 - 0:** Watermark mulai hancur atau sangat noise. Hal ini terjadi karena pada QF rendah, tabel kuantisasi JPEG membuang hampir seluruh detail halus, termasuk bit yang kita sisipkan.

## 5. Faktor yang Mempengaruhi Nilai QF & Keamanan
1.  **Kerumitan Foto (Texture):** Foto wajah dengan banyak detail (misal: rambut atau latar belakang ramai) memudahkan watermark "bersembunyi" secara visual, namun juga lebih rentan rusak saat kompresi frekuensi tinggi.
2.  **Algoritma Kode:** Penggunaan blok yang lebih besar (misal 5x5) akan membuat watermark lebih kuat (tahan QF rendah) tapi akan membuat gambar asli terlihat lebih kasar (pixelated).
3.  **Posisi Bit:** Semakin tinggi posisi bit yang digunakan (misal bit 4 atau 5), semakin tahan kompresi, tapi gambar akan terlihat "rusak" atau berubah warnanya secara kasat mata.

## 6. Kesimpulan
Metode LSB dengan optimasi Bit-3 dan Voting System terbukti cukup efektif untuk mempertahankan watermark pada tingkat kompresi menengah (QF 50). Namun, untuk kompresi ekstrem (di bawah QF 20), metode spasial seperti LSB tetap memiliki keterbatasan karena prinsip kerja JPEG yang memang membuang detail pada level bit tersebut. Untuk ketahanan yang lebih ekstrem, metode berbasis domain frekuensi (seperti DCT Watermarking) biasanya lebih disarankan.
