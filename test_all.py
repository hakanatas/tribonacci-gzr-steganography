"""
Ana Test Scripti - GZR Steganografi Sistemi

Bu script, tüm sistemi test eder ve raporlama yapar.
"""

import os
import cv2
import numpy as np
from encoder import GZREncoder
from decoder import GZRDecoder
from quality_metrics import analyze_quality, plot_comparison
from tribonacci import text_to_gzr, calculate_bit_density, verify_no_111_pattern


def create_test_images():
    """Test için örnek görüntüler oluşturur."""
    print("→ Test görüntüleri oluşturuluyor...\n")
    
    # Lena benzeri düşük frekanslı görüntü
    lena_like = np.zeros((512, 512), dtype=np.uint8)
    for i in range(512):
        for j in range(512):
            lena_like[i, j] = int(128 + 50 * np.sin(i/50) * np.cos(j/50))
    
    cv2.imwrite("test_lena.png", lena_like)
    print("✓ test_lena.png oluşturuldu (düşük frekanslı)")
    
    # Baboon benzeri yüksek frekanslı görüntü
    baboon_like = np.random.randint(50, 200, (512, 512), dtype=np.uint8)
    cv2.imwrite("test_baboon.png", baboon_like)
    print("✓ test_baboon.png oluşturuldu (yüksek frekanslı)\n")


def test_basic_functionality():
    """Temel kodlama-çözme işlevselliğini test eder."""
    print("="*60)
    print("TEST 1: TEMEL KODLAMA-ÇÖZME")
    print("="*60 + "\n")
    
    # Test mesajları
    messages = [
        "Merhaba Dünya!",
        "Bu bir GZR steganografi testidir.",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 3
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"--- Test {i}: {len(message)} karakter ---")
        print(f"Mesaj: '{message[:50]}{'...' if len(message) > 50 else ''}'")
        
        # Encode
        encoder = GZREncoder("test_lena.png")
        stats = encoder.encode_message(message, f"stego_test_{i}.png")
        
        # Decode
        decoder = GZRDecoder(f"stego_test_{i}.png")
        decoded = decoder.decode_message()
        
        # Doğrulama
        if decoded == message:
            print("✓ BAŞARILI: Mesaj doğru çözümlendi!")
        else:
            print("✗ HATA: Mesaj eşleşmiyor!")
            print(f"  Beklenen: {message[:100]}")
            print(f"  Bulunan:  {decoded[:100]}")
        
        print()


def test_quality_comparison():
    """Görüntü kalitesini test eder."""
    print("="*60)
    print("TEST 2: GÖRÜNTÜ KALİTESİ ANALİZİ")
    print("="*60 + "\n")
    
    test_message = "Bu bir kalite testi için örnek mesajdır. " * 10
    
    for img_name in ["test_lena.png", "test_baboon.png"]:
        print(f"--- {img_name} ---")
        
        # Orijinal görüntüyü yükle
        original = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
        
        # Encode
        encoder = GZREncoder(img_name)
        encoder.encode_message(test_message, f"stego_{img_name}")
        
        # Stego görüntüyü yükle
        stego = cv2.imread(f"stego_{img_name}", cv2.IMREAD_GRAYSCALE)
        
        # Kalite analizi
        results = analyze_quality(original, stego, verbose=True)
        
        print()


def test_gzr_vs_binary():
    """GZR ve Binary kodlama karşılaştırması yapar."""
    print("="*60)
    print("TEST 3: GZR vs BINARY KARŞILAŞTIRMA")
    print("="*60 + "\n")
    
    test_texts = [
        "A",
        "Hello World!",
        "The quick brown fox jumps over the lazy dog.",
        "?" * 10  # '111' pattern yaratma ihtimali yüksek
    ]
    
    print(f"{'Metin':<50} | {'GZR Bits':<10} | {'Bin Bits':<10} | "
          f"{'GZR 111':<10} | {'Bin 111':<10} | {'GZR Yoğ.':<10}")
    print("-" * 110)
    
    for text in test_texts:
        # GZR kodlama
        gzr_bits = text_to_gzr(text)
        gzr_density = calculate_bit_density(gzr_bits)
        _, gzr_111 = verify_no_111_pattern(gzr_bits)
        
        # Binary kodlama
        binary_bits = ''.join(format(ord(c), '08b') for c in text)
        binary_density = calculate_bit_density(binary_bits)
        _, binary_111 = verify_no_111_pattern(binary_bits)
        
        display_text = text[:47] + "..." if len(text) > 50 else text
        
        print(f"{display_text:<50} | {len(gzr_bits):<10} | {len(binary_bits):<10} | "
              f"{gzr_111:<10} | {binary_111:<10} | {gzr_density:.3f}")
    
    print()


def test_capacity_limits():
    """Kapasite limitlerini test eder."""
    print("="*60)
    print("TEST 4: KAPASİTE LİMİTLERİ")
    print("="*60 + "\n")
    
    encoder = GZREncoder("test_lena.png")
    capacity = encoder.get_capacity()
    
    print(f"Maksimum kapasite: {capacity} bayt ({capacity/1024:.2f} KB)")
    print(f"Bu yaklaşık {capacity//2} karakter metne eşittir.\n")
    
    # Farklı boyutlarda mesajlar test et
    test_sizes = [100, 1000, 5000, 10000, 20000]
    
    print(f"{'Mesaj Boyutu':<15} | {'Durum':<15} | {'Kullanılan Kapasite'}")
    print("-" * 55)
    
    for size in test_sizes:
        message = "A" * size
        
        try:
            # GZR kodlama boyutu hesapla (tahmin)
            gzr_bits = text_to_gzr(message)
            required_bytes = len(gzr_bits) // 8
            
            if required_bytes <= capacity:
                status = "✓ UYGUN"
                usage = f"{required_bytes}/{capacity} ({required_bytes/capacity*100:.1f}%)"
            else:
                status = "✗ FAZLA"
                usage = f"{required_bytes}/{capacity} ({required_bytes/capacity*100:.1f}%)"
            
            print(f"{size:<15} | {status:<15} | {usage}")
        
        except Exception as e:
            print(f"{size:<15} | ✗ HATA | {str(e)[:30]}")
    
    print()


def generate_report():
    """Kapsamlı test raporu oluşturur."""
    print("="*60)
    print("KAPSAMLI TEST RAPORU OLUŞTURULUYOR")
    print("="*60 + "\n")
    
    # Test mesajı
    test_message = """
    Bu, GZR steganografi sisteminin kapsamlı testini yapmak için 
    oluşturulmuş örnek bir metindir. Sistem, Tribonacci dizisi ve 
    Genelleştirilmiş Zeckendorf Teoremi'ni kullanarak görüntülere 
    gizli mesajlar yerleştirmektedir. Bu yöntemin temel avantajı, 
    ardışık '111' bit deseninin matematiksel olarak imkansız olması 
    ve bu sayede istatistiksel saldırılara karşı daha dirençli olmasıdır.
    """.strip()
    
    print(f"Test mesajı: {len(test_message)} karakter\n")
    
    # Her iki test görüntüsü için rapor
    results = []
    
    for img_name in ["test_lena.png", "test_baboon.png"]:
        print(f"{'='*60}")
        print(f"GÖRÜNTÜ: {img_name}")
        print(f"{'='*60}\n")
        
        # Orijinal yükle
        original = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
        
        # Encode
        encoder = GZREncoder(img_name)
        encode_stats = encoder.encode_message(test_message, f"stego_{img_name}")
        
        # Decode
        decoder = GZRDecoder(f"stego_{img_name}")
        decoded = decoder.decode_message()
        decode_stats = decoder.get_statistics()
        
        # Kalite analizi
        stego = cv2.imread(f"stego_{img_name}", cv2.IMREAD_GRAYSCALE)
        quality = analyze_quality(original, stego, verbose=False)
        
        # Karşılaştırma için binary kodlama
        binary_bits = ''.join(format(ord(c), '08b') for c in test_message)
        binary_density = calculate_bit_density(binary_bits)
        
        result = {
            'image': img_name,
            'message_correct': decoded == test_message,
            'psnr': quality['psnr'],
            'hist_corr': quality['histogram_correlation'],
            'gzr_density': encode_stats['bit_density'],
            'binary_density': binary_density,
            'pattern_111': encode_stats['pattern_111_count']
        }
        
        results.append(result)
        
        # Özet çıktı
        print(f"Mesaj doğruluğu:       {'✓ DOĞRU' if result['message_correct'] else '✗ YANLIŞ'}")
        print(f"PSNR:                  {result['psnr']:.2f} dB")
        print(f"Histogram Korelasyon:  {result['hist_corr']:.6f}")
        print(f"GZR bit yoğunluğu:     {result['gzr_density']:.4f}")
        print(f"Binary bit yoğunluğu:  {result['binary_density']:.4f}")
        print(f"Yoğunluk farkı:        {result['binary_density'] - result['gzr_density']:.4f}")
        print(f"'111' pattern sayısı:  {result['pattern_111']}")
        print()
    
    # Genel özet
    print("="*60)
    print("GENEL ÖZET")
    print("="*60 + "\n")
    
    avg_psnr = np.mean([r['psnr'] for r in results])
    avg_hist = np.mean([r['hist_corr'] for r in results])
    all_correct = all(r['message_correct'] for r in results)
    all_valid = all(r['pattern_111'] == 0 for r in results)
    
    print(f"Tüm testler başarılı:        {'✓ EVET' if all_correct else '✗ HAYIR'}")
    print(f"GZR doğrulaması (111=0):     {'✓ EVET' if all_valid else '✗ HAYIR'}")
    print(f"Ortalama PSNR:               {avg_psnr:.2f} dB")
    print(f"Ortalama Histogram Korelasyon: {avg_hist:.6f}")
    print()
    
    if avg_psnr > 40:
        print("✓ SONUÇ: Görüntü kalitesi MÜKEMMEL (>40 dB)")
    elif avg_psnr > 30:
        print("✓ SONUÇ: Görüntü kalitesi İYİ (30-40 dB)")
    else:
        print("⚠ SONUÇ: Görüntü kalitesi düşük (<30 dB)")


def main():
    """Ana test fonksiyonu."""
    print("\n" + "="*60)
    print("GZR STEGANOGRAFİ SİSTEMİ - TAM TEST PAKETİ")
    print("="*60 + "\n")
    
    # Test görüntüleri oluştur
    if not os.path.exists("test_lena.png"):
        create_test_images()
    
    # Testleri sırayla çalıştır
    try:
        test_basic_functionality()
        test_quality_comparison()
        test_gzr_vs_binary()
        test_capacity_limits()
        generate_report()
        
        print("="*60)
        print("TÜM TESTLER TAMAMLANDI!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ HATA OLUŞTU: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
