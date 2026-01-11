"""
GZR Tabanlı LSB Steganografi - Encoder Modülü

Bu modül, Genelleştirilmiş Zeckendorf Gösterimi (GZR) kullanarak
görüntülere veri gizleme işlemini gerçekleştirir.
"""

import cv2
import numpy as np
from tribonacci import text_to_gzr, verify_no_111_pattern, calculate_bit_density


class GZREncoder:
    """
    GZR tabanlı LSB steganografi kodlayıcı.
    """
    
    def __init__(self, image_path):
        """
        Encoder'ı başlatır ve görüntüyü yükler.
        
        Args:
            image_path (str): Giriş görüntüsünün yolu
        """
        self.image_path = image_path
        self.image = None
        self.stego_image = None
        self.encoded_bits = None
        
        self._load_image()
    
    def _load_image(self):
        """Görüntüyü yükler ve gri tonlamaya çevirir."""
        img = cv2.imread(self.image_path)
        if img is None:
            raise FileNotFoundError(f"Görüntü bulunamadı: {self.image_path}")
        
        # Gri tonlamaya çevir
        self.image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"✓ Görüntü yüklendi: {self.image.shape}")
    
    def get_capacity(self):
        """
        Görüntünün maksimum gizleme kapasitesini hesaplar.
        
        Returns:
            int: Maksimum gizlenebilecek bayt sayısı
        """
        height, width = self.image.shape
        capacity_bits = height * width  # Her piksele 1 bit
        capacity_bytes = capacity_bits // 8
        
        return capacity_bytes
    
    def encode_message(self, message, output_path=None):
        """
        Mesajı GZR formatına kodlayıp görüntüye gizler.
        
        Args:
            message (str): Gizlenecek metin mesajı
            output_path (str, optional): Çıktı görüntüsünün kaydedileceği yol
            
        Returns:
            dict: Kodlama istatistikleri
        """
        # 1. Mesajı GZR formatına kodla
        print("→ Mesaj GZR formatına kodlanıyor...")
        self.encoded_bits = text_to_gzr(message)
        
        # 2. Kapasite kontrolü
        capacity = self.get_capacity()
        required = len(self.encoded_bits) // 8 + 1
        
        if required > capacity:
            raise ValueError(
                f"Mesaj çok büyük! Gerekli: {required} bayt, Kapasite: {capacity} bayt"
            )
        
        print(f"✓ Kodlama tamamlandı: {len(self.encoded_bits)} bit")
        
        # 3. GZR doğrulaması
        valid, count_111 = verify_no_111_pattern(self.encoded_bits)
        density = calculate_bit_density(self.encoded_bits)
        
        print(f"  - '111' pattern sayısı: {count_111} {'✓' if valid else '✗ HATA!'}")
        print(f"  - '1' bit yoğunluğu: {density:.4f} ({density*100:.2f}%)")
        
        # 4. Mesaj uzunluğunu başa ekle (32 bit = 4 bayt)
        length_bits = format(len(self.encoded_bits), '032b')
        full_bits = length_bits + self.encoded_bits
        
        # 5. LSB gizleme
        print("→ Görüntüye gizleniyor...")
        self.stego_image = self._embed_bits(full_bits)
        
        # 6. Kaydetme
        if output_path:
            cv2.imwrite(output_path, self.stego_image)
            print(f"✓ Stego görüntü kaydedildi: {output_path}")
        
        # İstatistikler
        stats = {
            'message_length': len(message),
            'encoded_bits': len(self.encoded_bits),
            'bit_density': density,
            'valid_gzr': valid,
            'pattern_111_count': count_111,
            'capacity_used': f"{required}/{capacity} bayt ({required/capacity*100:.2f}%)"
        }
        
        return stats
    
    def _embed_bits(self, bits):
        """
        Bit dizisini görüntüye LSB yöntemiyle gömür.
        
        Args:
            bits (str): Gömülecek bit dizisi
            
        Returns:
            numpy.ndarray: Stego görüntü
        """
        stego = self.image.copy()
        height, width = stego.shape
        
        bit_index = 0
        embedded_count = 0
        
        # Satır satır, piksel piksel ilerle
        for i in range(height):
            for j in range(width):
                if bit_index >= len(bits):
                    return stego
                
                # Pikselin LSB'sini değiştir
                pixel_value = int(stego[i, j])
                bit_to_embed = int(bits[bit_index])
                
                # LSB değiştirme: (pixel & 0xFE) | bit
                new_pixel = (pixel_value & 0xFE) | bit_to_embed
                stego[i, j] = new_pixel
                
                bit_index += 1
                embedded_count += 1
        
        print(f"✓ {embedded_count} bit gömüldü")
        return stego
    
    def compare_with_binary(self, message):
        """
        GZR ve Binary kodlama karşılaştırması yapar.
        
        Args:
            message (str): Test mesajı
            
        Returns:
            dict: Karşılaştırma sonuçları
        """
        # GZR kodlama
        gzr_bits = text_to_gzr(message)
        gzr_density = calculate_bit_density(gzr_bits)
        gzr_valid, gzr_111 = verify_no_111_pattern(gzr_bits)
        
        # Binary kodlama
        binary_bits = ''.join(format(ord(c), '08b') for c in message)
        binary_density = calculate_bit_density(binary_bits)
        binary_valid, binary_111 = verify_no_111_pattern(binary_bits)
        
        # Karşılaştırma
        comparison = {
            'message_length': len(message),
            'gzr': {
                'bits': len(gzr_bits),
                'density': gzr_density,
                'pattern_111': gzr_111,
                'valid': gzr_valid
            },
            'binary': {
                'bits': len(binary_bits),
                'density': binary_density,
                'pattern_111': binary_111,
                'valid': binary_valid
            },
            'difference': {
                'bits': len(gzr_bits) - len(binary_bits),
                'density_reduction': binary_density - gzr_density,
                'pattern_111_reduction': binary_111 - gzr_111
            }
        }
        
        return comparison


# Test ve örnek kullanım
if __name__ == "__main__":
    import os
    
    # Test görüntüsü oluştur (eğer yoksa)
    if not os.path.exists("test_image.png"):
        print("Test görüntüsü oluşturuluyor...")
        test_img = np.random.randint(100, 200, (512, 512), dtype=np.uint8)
        cv2.imwrite("test_image.png", test_img)
        print("✓ Test görüntüsü oluşturuldu: test_image.png")
    
    print("\n=== GZR ENCODER TEST ===\n")
    
    # Encoder'ı başlat
    encoder = GZREncoder("test_image.png")
    
    # Kapasite bilgisi
    capacity = encoder.get_capacity()
    print(f"Görüntü kapasitesi: {capacity} bayt (~{capacity//1024} KB)\n")
    
    # Test mesajı
    secret_message = "Bu bir test mesajıdır. GZR steganografi çalışıyor! 🔒"
    print(f"Gizlenecek mesaj: '{secret_message}'")
    print(f"Mesaj uzunluğu: {len(secret_message)} karakter\n")
    
    # Kodlama
    stats = encoder.encode_message(secret_message, "stego_image.png")
    
    # İstatistikler
    print("\n=== KODLAMA İSTATİSTİKLERİ ===")
    for key, value in stats.items():
        print(f"{key:.<30} {value}")
    
    # Binary karşılaştırma
    print("\n=== GZR vs BINARY KARŞILAŞTIRMA ===")
    comparison = encoder.compare_with_binary(secret_message[:20])  # İlk 20 karakter
    
    print(f"\nGZR Kodlama:")
    print(f"  Toplam bit: {comparison['gzr']['bits']}")
    print(f"  '1' yoğunluğu: {comparison['gzr']['density']:.4f}")
    print(f"  '111' sayısı: {comparison['gzr']['pattern_111']}")
    
    print(f"\nBinary Kodlama:")
    print(f"  Toplam bit: {comparison['binary']['bits']}")
    print(f"  '1' yoğunluğu: {comparison['binary']['density']:.4f}")
    print(f"  '111' sayısı: {comparison['binary']['pattern_111']}")
    
    print(f"\nFark:")
    print(f"  Bit farkı: {comparison['difference']['bits']} "
          f"({abs(comparison['difference']['bits'])/comparison['binary']['bits']*100:.1f}%)")
    print(f"  Yoğunluk azalması: {comparison['difference']['density_reduction']:.4f} "
          f"({comparison['difference']['density_reduction']/comparison['binary']['density']*100:.1f}%)")
    print(f"  '111' azalması: {comparison['difference']['pattern_111_reduction']}")
