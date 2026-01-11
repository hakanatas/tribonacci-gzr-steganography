"""
Örnek Kullanım - Hızlı Başlangıç

Bu script, GZR steganografi sisteminin temel kullanımını gösterir.
"""

from encoder import GZREncoder
from decoder import GZRDecoder
from quality_metrics import analyze_quality
import cv2


def main():
    print("="*60)
    print("GZR STEGANOGRAFİ - HIZLI BAŞLANGIÇ ÖRNEĞİ")
    print("="*60 + "\n")
    
    # ADIM 1: Görüntü Bilgisi
    image_path = "test_lena.png"
    print(f"1. Kullanılacak görüntü: {image_path}")
    
    # Görüntü yoksa oluştur
    import os
    import numpy as np
    if not os.path.exists(image_path):
        print("   → Görüntü bulunamadı, test görüntüsü oluşturuluyor...")
        test_img = np.zeros((512, 512), dtype=np.uint8)
        for i in range(512):
            for j in range(512):
                test_img[i, j] = int(128 + 50 * np.sin(i/50) * np.cos(j/50))
        cv2.imwrite(image_path, test_img)
        print("   ✓ Test görüntüsü oluşturuldu\n")
    else:
        print("   ✓ Görüntü bulundu\n")
    
    # ADIM 2: Gizlenecek Mesaj
    secret_message = input("2. Gizlemek istediğiniz mesajı yazın (veya Enter'a basın): ").strip()
    
    if not secret_message:
        secret_message = "Bu gizli bir mesajdır! GZR steganografi çalışıyor. 🔒"
        print(f"   → Varsayılan mesaj kullanılıyor: '{secret_message}'\n")
    else:
        print(f"   ✓ Mesaj alındı: '{secret_message}'\n")
    
    # ADIM 3: Encoder - Mesajı Gizle
    print("3. Mesaj gizleniyor...")
    encoder = GZREncoder(image_path)
    
    # Kapasite kontrolü
    capacity = encoder.get_capacity()
    print(f"   → Görüntü kapasitesi: {capacity} bayt (~{capacity//1024} KB)")
    
    # Kodlama
    output_path = "stego_output.png"
    stats = encoder.encode_message(secret_message, output_path)
    
    print(f"   ✓ Mesaj gizlendi: {output_path}")
    print(f"   → Bit yoğunluğu: {stats['bit_density']:.4f}")
    print(f"   → '111' pattern sayısı: {stats['pattern_111_count']} (olmalı: 0)")
    print()
    
    # ADIM 4: Decoder - Mesajı Çıkar
    print("4. Mesaj çözümleniyor...")
    decoder = GZRDecoder(output_path)
    decoded_message = decoder.decode_message()
    
    print(f"   ✓ Mesaj çözümlendi: '{decoded_message}'\n")
    
    # ADIM 5: Doğrulama
    print("5. Doğrulama:")
    if decoded_message == secret_message:
        print("   ✓ BAŞARILI! Orijinal ve çözümlenen mesaj özdeş.")
    else:
        print("   ✗ HATA! Mesajlar uyuşmuyor!")
        print(f"   Orijinal : {secret_message}")
        print(f"   Çözümlenen: {decoded_message}")
    print()
    
    # ADIM 6: Kalite Analizi
    print("6. Görüntü kalitesi analizi:")
    original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    stego = cv2.imread(output_path, cv2.IMREAD_GRAYSCALE)
    
    results = analyze_quality(original, stego, verbose=False)
    
    print(f"   → PSNR: {results['psnr']:.2f} dB")
    print(f"   → Histogram Korelasyon: {results['histogram_correlation']:.6f}")
    print(f"   → Değişen piksel oranı: {results['change_rate']:.4f}%")
    
    if results['psnr'] > 40:
        print("   ✓ KALİTE: Mükemmel (>40 dB)")
    elif results['psnr'] > 30:
        print("   ✓ KALİTE: İyi (30-40 dB)")
    else:
        print("   ⚠ KALİTE: Orta (<30 dB)")
    
    print("\n" + "="*60)
    print("İŞLEM TAMAMLANDI!")
    print("="*60)
    print(f"\nOluşturulan dosya: {output_path}")
    print("Bu görüntüyü istediğiniz yere gönderebilir ve")
    print("alıcı decoder.py ile gizli mesajı çıkarabilir.")


if __name__ == "__main__":
    main()
