"""
Görüntü Kalitesi Metrikleri - PSNR, MSE, Histogram Analizi

Bu modül, orijinal ve stego görüntüler arasındaki kalite farkını hesaplar.
"""

import cv2
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def calculate_mse(img1, img2):
    """
    İki görüntü arasındaki Ortalama Kare Hata (MSE) hesaplar.
    
    MSE = (1/MN) × Σ[I(i,j) - I'(i,j)]²
    
    Args:
        img1 (numpy.ndarray): İlk görüntü
        img2 (numpy.ndarray): İkinci görüntü
        
    Returns:
        float: MSE değeri
    """
    if img1.shape != img2.shape:
        raise ValueError("Görüntüler aynı boyutta olmalı!")
    
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    return mse


def calculate_psnr(img1, img2, max_pixel=255.0):
    """
    İki görüntü arasındaki Tepe Sinyal-Gürültü Oranı (PSNR) hesaplar.
    
    PSNR = 10 × log₁₀(MAX² / MSE) dB
    
    Args:
        img1 (numpy.ndarray): Orijinal görüntü
        img2 (numpy.ndarray): Stego görüntü
        max_pixel (float): Maksimum piksel değeri (8-bit için 255)
        
    Returns:
        float: PSNR değeri (dB)
    """
    mse = calculate_mse(img1, img2)
    
    if mse == 0:
        return float('inf')  # Görüntüler özdeş
    
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr


def calculate_histogram_correlation(img1, img2):
    """
    İki görüntünün histogramları arasındaki Pearson korelasyonunu hesaplar.
    
    Args:
        img1 (numpy.ndarray): İlk görüntü
        img2 (numpy.ndarray): İkinci görüntü
        
    Returns:
        float: Korelasyon katsayısı (-1 ile 1 arası)
    """
    # Histogramları hesapla
    hist1, _ = np.histogram(img1.flatten(), bins=256, range=(0, 256))
    hist2, _ = np.histogram(img2.flatten(), bins=256, range=(0, 256))
    
    # Pearson korelasyonu
    correlation, _ = stats.pearsonr(hist1, hist2)
    
    return correlation


def analyze_quality(original_img, stego_img, verbose=True):
    """
    Orijinal ve stego görüntü arasında kapsamlı kalite analizi yapar.
    
    Args:
        original_img (numpy.ndarray): Orijinal görüntü
        stego_img (numpy.ndarray): Stego görüntü
        verbose (bool): Detaylı çıktı göster
        
    Returns:
        dict: Kalite metrikleri
    """
    mse = calculate_mse(original_img, stego_img)
    psnr = calculate_psnr(original_img, stego_img)
    hist_corr = calculate_histogram_correlation(original_img, stego_img)
    
    # Piksel değişim analizi
    diff = np.abs(original_img.astype(float) - stego_img.astype(float))
    changed_pixels = np.count_nonzero(diff)
    total_pixels = original_img.size
    change_rate = (changed_pixels / total_pixels) * 100
    
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    
    results = {
        'mse': mse,
        'psnr': psnr,
        'histogram_correlation': hist_corr,
        'changed_pixels': changed_pixels,
        'total_pixels': total_pixels,
        'change_rate': change_rate,
        'max_pixel_diff': max_diff,
        'mean_pixel_diff': mean_diff
    }
    
    if verbose:
        print("=== GÖRÜNTÜ KALİTESİ ANALİZİ ===")
        print(f"MSE (Ortalama Kare Hata):         {mse:.6f}")
        print(f"PSNR (Tepe Sinyal-Gürültü Oranı): {psnr:.2f} dB")
        print(f"Histogram Korelasyonu:            {hist_corr:.6f}")
        print(f"\nPiksel Değişimleri:")
        print(f"  Değişen piksel sayısı:          {changed_pixels:,}")
        print(f"  Toplam piksel:                  {total_pixels:,}")
        print(f"  Değişim oranı:                  {change_rate:.4f}%")
        print(f"  Maksimum fark:                  {max_diff:.1f}")
        print(f"  Ortalama fark:                  {mean_diff:.6f}")
        
        # Kalite değerlendirmesi
        if psnr > 40:
            quality = "Mükemmel - insan gözüyle fark edilemez"
        elif psnr > 30:
            quality = "İyi - minimal bozulma"
        elif psnr > 20:
            quality = "Orta - fark edilir bozulma"
        else:
            quality = "Düşük - belirgin bozulma"
        
        print(f"\nKalite Değerlendirmesi: {quality}")
    
    return results


def plot_comparison(original_img, stego_img, save_path=None):
    """
    Orijinal ve stego görüntülerin karşılaştırmalı görselleştirmesini yapar.
    
    Args:
        original_img (numpy.ndarray): Orijinal görüntü
        stego_img (numpy.ndarray): Stego görüntü
        save_path (str, optional): Grafiğin kaydedileceği yol
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 1. Orijinal görüntü
    axes[0, 0].imshow(original_img, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title('Orijinal Görüntü')
    axes[0, 0].axis('off')
    
    # 2. Stego görüntü
    axes[0, 1].imshow(stego_img, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title('Stego Görüntü')
    axes[0, 1].axis('off')
    
    # 3. Fark görüntüsü
    diff = np.abs(original_img.astype(float) - stego_img.astype(float))
    axes[0, 2].imshow(diff, cmap='hot')
    axes[0, 2].set_title('Piksel Farkları (Büyütülmüş)')
    axes[0, 2].axis('off')
    
    # 4. Orijinal histogram
    axes[1, 0].hist(original_img.flatten(), bins=256, range=(0, 256), 
                    color='blue', alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('Orijinal Histogram')
    axes[1, 0].set_xlabel('Piksel Değeri')
    axes[1, 0].set_ylabel('Frekans')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 5. Stego histogram
    axes[1, 1].hist(stego_img.flatten(), bins=256, range=(0, 256), 
                    color='red', alpha=0.7, edgecolor='black')
    axes[1, 1].set_title('Stego Histogram')
    axes[1, 1].set_xlabel('Piksel Değeri')
    axes[1, 1].set_ylabel('Frekans')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 6. Histogram karşılaştırması
    axes[1, 2].hist(original_img.flatten(), bins=256, range=(0, 256), 
                    color='blue', alpha=0.5, label='Orijinal', edgecolor='black')
    axes[1, 2].hist(stego_img.flatten(), bins=256, range=(0, 256), 
                    color='red', alpha=0.5, label='Stego', edgecolor='black')
    axes[1, 2].set_title('Histogram Karşılaştırması')
    axes[1, 2].set_xlabel('Piksel Değeri')
    axes[1, 2].set_ylabel('Frekans')
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Karşılaştırma grafiği kaydedildi: {save_path}")
    
    plt.show()


# Test
if __name__ == "__main__":
    print("=== KALİTE METRİKLERİ TEST ===\n")
    
    # Test görüntüleri oluştur
    original = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
    
    # Stego görüntü simülasyonu (her piksele %50 olasılıkla ±1)
    stego = original.copy()
    mask = np.random.random((512, 512)) < 0.5
    stego[mask] = np.clip(stego[mask] + np.random.choice([-1, 1], size=np.sum(mask)), 0, 255)
    
    # Analiz
    results = analyze_quality(original, stego, verbose=True)
    
    print(f"\n{'='*50}")
    print("NOT: Bu test, random görüntüler kullanmaktadır.")
    print("Gerçek sonuçlar için encoder.py ile oluşturulan")
    print("stego görüntüleri kullanın.")
