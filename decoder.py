"""
GZR Tabanlı LSB Steganografi - Decoder Modülü

Bu modül, GZR ile kodlanmış ve görüntüye gizlenmiş veriyi çıkarır.
"""

import cv2
import numpy as np
from tribonacci import gzr_to_text


class GZRDecoder:
    """
    GZR tabanlı LSB steganografi çözücü.
    """
    
    def __init__(self, image_path):
        """
        Decoder'ı başlatır ve stego görüntüyü yükler.
        
        Args:
            image_path (str): Stego görüntünün yolu
        """
        self.image_path = image_path
        self.stego_image = None
        self.extracted_bits = None
        self.message = None
        
        self._load_image()
    
    def _load_image(self):
        """Stego görüntüyü yükler."""
        img = cv2.imread(self.image_path)
        if img is None:
            raise FileNotFoundError(f"Görüntü bulunamadı: {self.image_path}")
        
        # Gri tonlamaya çevir
        self.stego_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"✓ Stego görüntü yüklendi: {self.stego_image.shape}")
    
    def decode_message(self):
        """
        Görüntüden gizli mesajı çıkarır ve çözümler.
        
        Returns:
            str: Çözümlenmiş metin mesajı
        """
        # 1. İlk 32 biti oku (mesaj uzunluğu)
        print("→ Mesaj uzunluğu okunuyor...")
        length_bits = self._extract_bits(0, 32)
        message_length = int(length_bits, 2)
        
        print(f"✓ Mesaj uzunluğu: {message_length} bit")
        
        # 2. Mesaj bitlerini çıkar
        print("→ Mesaj bitleri çıkarılıyor...")
        self.extracted_bits = self._extract_bits(32, message_length)
        
        print(f"✓ {len(self.extracted_bits)} bit çıkarıldı")
        
        # 3. GZR'den metne çevir
        print("→ GZR çözümleniyor...")
        self.message = gzr_to_text(self.extracted_bits)
        
        print(f"✓ Mesaj çözümlendi: {len(self.message)} karakter")
        
        return self.message
    
    def _extract_bits(self, start_bit, length):
        """
        Görüntüden belirtilen bit aralığını çıkarır.
        
        Args:
            start_bit (int): Başlangıç bit pozisyonu
            length (int): Çıkarılacak bit sayısı
            
        Returns:
            str: Çıkarılan bit dizisi
        """
        height, width = self.stego_image.shape
        bits = []
        
        bit_index = 0
        total_bits = height * width
        
        for i in range(height):
            for j in range(width):
                if bit_index >= start_bit and bit_index < start_bit + length:
                    # Pikselin LSB'sini al
                    pixel_value = int(self.stego_image[i, j])
                    lsb = pixel_value & 1  # Son biti al
                    bits.append(str(lsb))
                
                bit_index += 1
                
                if bit_index >= start_bit + length:
                    return ''.join(bits)
        
        return ''.join(bits)
    
    def get_statistics(self):
        """
        Çıkarılan verinin istatistiklerini döndürür.
        
        Returns:
            dict: İstatistik bilgileri
        """
        if self.extracted_bits is None or self.message is None:
            return None
        
        ones_count = self.extracted_bits.count('1')
        total_bits = len(self.extracted_bits)
        density = ones_count / total_bits if total_bits > 0 else 0
        
        pattern_111 = self.extracted_bits.count('111')
        
        stats = {
            'message_length': len(self.message),
            'total_bits': total_bits,
            'ones_count': ones_count,
            'bit_density': density,
            'pattern_111_count': pattern_111,
            'valid_gzr': pattern_111 == 0
        }
        
        return stats


# Test ve örnek kullanım
if __name__ == "__main__":
    import os
    
    # Önce encoder ile bir mesaj gizle (eğer stego görüntü yoksa)
    if not os.path.exists("stego_image.png"):
        print("=== ÖNCELİKLE ENCODER ÇALIŞTIRILIYOR ===\n")
        from encoder import GZREncoder
        
        # Test görüntüsü oluştur
        if not os.path.exists("test_image.png"):
            test_img = np.random.randint(100, 200, (512, 512), dtype=np.uint8)
            cv2.imwrite("test_image.png", test_img)
        
        # Mesaj gizle
        encoder = GZREncoder("test_image.png")
        secret_message = "Bu bir test mesajıdır. GZR steganografi çalışıyor! 🔒"
        encoder.encode_message(secret_message, "stego_image.png")
        print("\n" + "="*50 + "\n")
    
    print("=== GZR DECODER TEST ===\n")
    
    # Decoder'ı başlat
    decoder = GZRDecoder("stego_image.png")
    
    # Mesajı çözümle
    decoded_message = decoder.decode_message()
    
    print(f"\n✓ ÇÖZÜMLENEN MESAJ:")
    print(f"  '{decoded_message}'")
    
    # İstatistikler
    stats = decoder.get_statistics()
    if stats:
        print("\n=== ÇÖZÜMLEME İSTATİSTİKLERİ ===")
        for key, value in stats.items():
            print(f"{key:.<30} {value}")
        
        if stats['valid_gzr']:
            print("\n✓ GZR doğrulaması BAŞARILI - '111' pattern yok!")
        else:
            print(f"\n⚠ UYARI: {stats['pattern_111_count']} adet '111' pattern bulundu!")
