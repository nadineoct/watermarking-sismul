import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fftpack import dct, idct

# --- KONFIGURASI ---
BIT_POSITION = 3  # Bit ke-3 (0, 1, 2, [3], 4, 5, 6, 7)
IMAGE_PATH     = "data/face.jpeg"
WATERMARK_PATH = "data/logo_watermark.png"
WM_SIZE        = (64, 64)
LOCATION       = 'top-left'
QUALITY_FACTORS = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

# Standard JPEG Luminance Quantization Table
Q_TABLE = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
], dtype=np.float32)

def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')

def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')

def load_image(path, mode='color'):
    if mode == 'gray':
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {path}")
    return img

def load_watermark(path, size):
    wm = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if wm is None:
        raise FileNotFoundError(f"Watermark tidak ditemukan: {path}")
    wm = cv2.resize(wm, size, interpolation=cv2.INTER_NEAREST)
    _, wm_binary = cv2.threshold(wm, 127, 1, cv2.THRESH_BINARY)
    return wm_binary

def _get_location(location, img_h, img_w, wm_h, wm_w):
    if location == 'top-left': return 0, 0
    elif location == 'center': return (img_h - wm_h) // 2, (img_w - wm_w) // 2
    elif location == 'bottom-right': return img_h - wm_h, img_w - wm_w
    elif location == 'top-right': return 0, img_w - wm_w
    elif location == 'bottom-left': return img_h - wm_h, 0
    return 0, 0

def embed_lsb(image, watermark_binary, location='center'):
    img = image.copy()
    wm_h, wm_w = watermark_binary.shape
    img_h, img_w = img.shape[:2]
    block_size = 3
    row_start, col_start = _get_location(location, img_h, img_w, wm_h * block_size, wm_w * block_size)
    mask = ~(1 << BIT_POSITION) & 0xFF
    for r in range(wm_h):
        for c in range(wm_w):
            bit = int(watermark_binary[r, c])
            r_img = row_start + (r * block_size)
            c_img = col_start + (c * block_size)
            if r_img + block_size <= img_h and c_img + block_size <= img_w:
                if len(img.shape) == 3:
                    region = img[r_img:r_img+block_size, c_img:c_img+block_size, 1]
                    img[r_img:r_img+block_size, c_img:c_img+block_size, 1] = (region & mask) | (bit << BIT_POSITION)
                else:
                    region = img[r_img:r_img+block_size, c_img:c_img+block_size]
                    img[r_img:r_img+block_size, c_img:c_img+block_size] = (region & mask) | (bit << BIT_POSITION)
    return img

def extract_lsb(watermarked_image, wm_size, location='center'):
    img = watermarked_image.copy()
    wm_w, wm_h = wm_size
    img_h, img_w = img.shape[:2]
    block_size = 3
    row_start, col_start = _get_location(location, img_h, img_w, wm_h * block_size, wm_w * block_size)
    extracted = np.zeros((wm_h, wm_w), dtype=np.uint8)
    for r in range(wm_h):
        for c in range(wm_w):
            r_img = row_start + (r * block_size)
            c_img = col_start + (c * block_size)
            if r_img + block_size <= img_h and c_img + block_size <= img_w:
                if len(img.shape) == 3:
                    region = img[r_img:r_img+block_size, c_img:c_img+block_size, 1]
                else:
                    region = img[r_img:r_img+block_size, c_img:c_img+block_size]
                bits_in_block = (region >> BIT_POSITION) & 1
                if np.mean(bits_in_block) >= 0.5:
                    extracted[r, c] = 1
                else:
                    extracted[r, c] = 0
    return extracted

def apply_manual_jpeg(img, quality):
    if quality <= 0: quality = 1
    if quality < 50:
        s = 5000 / quality
    else:
        s = 200 - 2 * quality
    q_scaled = np.floor((s * Q_TABLE + 50) / 100)
    q_scaled[q_scaled < 1] = 1
    q_scaled[q_scaled > 255] = 255
    h, w = img.shape[:2]
    h_new, w_new = (h // 8) * 8, (w // 8) * 8
    result = img.copy().astype(np.float32)
    for ch in range(img.shape[2] if len(img.shape) == 3 else 1):
        for i in range(0, h_new, 8):
            for j in range(0, w_new, 8):
                if len(img.shape) == 3:
                    block = result[i:i+8, j:j+8, ch] - 128
                    coeffs = dct2(block)
                    quantized = np.round(coeffs / q_scaled)
                    dequantized = quantized * q_scaled
                    result[i:i+8, j:j+8, ch] = idct2(dequantized) + 128
                else:
                    block = result[i:i+8, j:j+8] - 128
                    coeffs = dct2(block)
                    quantized = np.round(coeffs / q_scaled)
                    dequantized = quantized * q_scaled
                    result[i:i+8, j:j+8] = idct2(dequantized) + 128
    return np.clip(result, 0, 255).astype(np.uint8)

def calculate_psnr(original, compressed):
    mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)
    if mse == 0: return float('inf')
    return round(20 * np.log10(255.0 / np.sqrt(mse)), 2)

def calculate_ber(original_wm, extracted_wm):
    return round(np.sum(original_wm != extracted_wm) / original_wm.size, 4)

def run_experiment():
    os.makedirs('hasil_deliverable', exist_ok=True)
    print("Memulai Eksperimen Watermarking...")
    
    try:
        image = load_image(IMAGE_PATH, mode='color')
        watermark = load_watermark(WATERMARK_PATH, WM_SIZE)
    except Exception as e:
        print(f"Error: {e}")
        print("Pastikan file 'face.jpeg' dan 'logo_watermark.png' ada di folder 'data/'")
        return

    watermarked = embed_lsb(image, watermark, location=LOCATION)
    cv2.imwrite('hasil_deliverable/watermarked_original.png', watermarked)

    print(f"{'QF':>5} | {'PSNR':>10} | {'BER':>8} | Status")
    print("-" * 40)

    for qf in QUALITY_FACTORS:
        compressed = apply_manual_jpeg(watermarked, quality=qf)
        extracted = extract_lsb(compressed, WM_SIZE, location=LOCATION)
        
        psnr = calculate_psnr(watermarked, compressed)
        ber = calculate_ber(watermark, extracted)
        
        output_path = f'hasil_deliverable/extracted_qf{qf}.png'
        cv2.imwrite(output_path, (extracted * 255).astype(np.uint8))
        
        status = "OK" if ber < 0.2 else "FAIL"
        print(f"{qf:>5} | {psnr:>10} | {ber:>8} | {status}")

    print("\nEksperimen Selesai. Hasil ada di folder 'hasil_deliverable/'")

if __name__ == "__main__":
    run_experiment()
