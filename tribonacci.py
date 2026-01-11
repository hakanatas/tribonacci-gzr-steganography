"""
Tribonacci Dizisi ve Genelleştirilmiş Zeckendorf Gösterimi (GZR) Modülü

Bu modül, Tribonacci sayı dizisini üreten ve sayıları GZR formatına
kodlayan/çözen fonksiyonları içerir.

Zeckendorf Teoremi: Her pozitif tamsayı, ardışık olmayan Fibonacci 
sayılarının toplamı olarak tek biçimde yazılabilir.

Genelleştirilmiş Zeckendorf (Tribonacci için): Her pozitif tamsayı,
ardışık üç katsayısı aynı anda 1 olmayacak şekilde (111 yasağı)
Tribonacci sayılarının toplamı olarak tek biçimde yazılabilir.
"""


def generate_tribonacci(max_value):
    """
    Belirli bir maksimum değere kadar Tribonacci dizisi üretir.
    
    Tribonacci dizisi: T(n) = T(n-1) + T(n-2) + T(n-3)
    Başlangıç değerleri: T(1)=1, T(2)=2, T(3)=4
    
    Args:
        max_value (int): Üretilecek maksimum Tribonacci sayısı
        
    Returns:
        list: Tribonacci sayılarının listesi [1, 2, 4, 7, 13, 24, ...]
    """
    if max_value < 1:
        return []
    
    tribonacci = [1, 2, 4]  # İlk üç terim
    
    while tribonacci[-1] < max_value:
        next_term = tribonacci[-1] + tribonacci[-2] + tribonacci[-3]
        if next_term > max_value:
            break
        tribonacci.append(next_term)
    
    return tribonacci


def decimal_to_gzr(n, tribonacci_seq=None):
    """
    Onluk tabandaki bir sayıyı GZR (Genelleştirilmiş Zeckendorf) formatına dönüştürür.
    
    Açgözlü algoritma kullanır: Her adımda mümkün olan en büyük Tribonacci
    sayısını seçer.
    
    Args:
        n (int): Dönüştürülecek pozitif tamsayı
        tribonacci_seq (list, optional): Önceden hesaplanmış Tribonacci dizisi
        
    Returns:
        str: GZR bit dizisi (örn: "1001101")
        
    Örnek:
        >>> decimal_to_gzr(65)
        '1001101'
        >>> # 65 = 44 + 13 + 7 + 1 = T7 + T5 + T4 + T1
    """
    if n <= 0:
        return "0"
    
    # Tribonacci dizisini hazırla
    if tribonacci_seq is None:
        tribonacci_seq = generate_tribonacci(n)
    
    # En büyük Tribonacci sayısından geriye doğru
    bits = []
    remaining = n
    
    for t in reversed(tribonacci_seq):
        if t <= remaining:
            bits.append('1')
            remaining -= t
        else:
            bits.append('0')
    
    # Baştaki sıfırları kaldır ve ters çevir (küçükten büyüğe)
    result = ''.join(reversed(bits)).lstrip('0')
    
    return result if result else "0"


def gzr_to_decimal(gzr_bits, tribonacci_seq=None):
    """
    GZR formatındaki bit dizisini onluk tabana dönüştürür.
    
    Args:
        gzr_bits (str): GZR bit dizisi (örn: "1001101")
        tribonacci_seq (list, optional): Önceden hesaplanmış Tribonacci dizisi
        
    Returns:
        int: Onluk tabandaki sayı
        
    Örnek:
        >>> gzr_to_decimal("1001101")
        65
        >>> # 1×1 + 0×2 + 0×4 + 1×7 + 1×13 + 0×24 + 1×44 = 65
    """
    if not gzr_bits or gzr_bits == "0":
        return 0
    
    # Tribonacci dizisini hazırla
    bit_length = len(gzr_bits)
    if tribonacci_seq is None:
        tribonacci_seq = generate_tribonacci(2 ** bit_length)
    
    # Bit pozisyonlarındaki 1'lerin karşılık geldiği Tribonacci sayılarını topla
    result = 0
    for i, bit in enumerate(gzr_bits):
        if bit == '1' and i < len(tribonacci_seq):
            result += tribonacci_seq[i]
    
    return result


def text_to_gzr(text):
    """
    Metin verisini GZR formatına kodlar.
    
    Her karakterin ASCII değerini GZR'ye çevirir ve birleştirir.
    
    Args:
        text (str): Kodlanacak metin
        
    Returns:
        str: GZR kodlu bit dizisi
    """
    # Maksimum ASCII değeri için Tribonacci dizisini hazırla
    max_ascii = 255
    tribonacci_seq = generate_tribonacci(max_ascii)
    
    gzr_bits = []
    
    for char in text:
        ascii_val = ord(char)
        gzr = decimal_to_gzr(ascii_val, tribonacci_seq)
        
        # Sabit uzunluk için padding (8 bit yerine 9 bit - 255'i kodlamak için)
        gzr = gzr.zfill(9)
        gzr_bits.append(gzr)
    
    return ''.join(gzr_bits)


def gzr_to_text(gzr_bits):
    """
    GZR formatındaki bit dizisini metne çözümler.
    
    Args:
        gzr_bits (str): GZR kodlu bit dizisi
        
    Returns:
        str: Çözümlenmiş metin
    """
    # Maksimum ASCII değeri için Tribonacci dizisini hazırla
    max_ascii = 255
    tribonacci_seq = generate_tribonacci(max_ascii)
    
    # Her 9 bitlik bloğu bir karaktere çevir
    chars = []
    chunk_size = 9
    
    for i in range(0, len(gzr_bits), chunk_size):
        chunk = gzr_bits[i:i + chunk_size]
        if len(chunk) == chunk_size:
            ascii_val = gzr_to_decimal(chunk, tribonacci_seq)
            if ascii_val > 0:  # Null karakterleri atla
                chars.append(chr(ascii_val))
    
    return ''.join(chars)


def verify_no_111_pattern(gzr_bits):
    """
    GZR bit dizisinde "111" deseninin olmadığını doğrular.
    
    Bu, Genelleştirilmiş Zeckendorf Teoremi'nin temel özelliğidir.
    
    Args:
        gzr_bits (str): Kontrol edilecek bit dizisi
        
    Returns:
        tuple: (bool, int) - (geçerli mi?, "111" sayısı)
    """
    count_111 = gzr_bits.count("111")
    is_valid = count_111 == 0
    
    return is_valid, count_111


def calculate_bit_density(gzr_bits):
    """
    Bit dizisindeki "1" yoğunluğunu hesaplar.
    
    Args:
        gzr_bits (str): Analiz edilecek bit dizisi
        
    Returns:
        float: "1" bitlerinin oranı (0.0 - 1.0 arası)
    """
    if not gzr_bits:
        return 0.0
    
    ones_count = gzr_bits.count('1')
    total_bits = len(gzr_bits)
    
    return ones_count / total_bits


# Test fonksiyonu
if __name__ == "__main__":
    print("=== Tribonacci Dizisi Testi ===")
    trib = generate_tribonacci(100)
    print(f"Tribonacci (≤100): {trib}")
    print()
    
    print("=== GZR Kodlama Testi ===")
    test_numbers = [1, 7, 30, 65, 127, 255]
    
    for num in test_numbers:
        gzr = decimal_to_gzr(num)
        decoded = gzr_to_decimal(gzr)
        valid, count = verify_no_111_pattern(gzr)
        
        print(f"{num:3d} → GZR: {gzr:>12s} → Decoded: {decoded:3d} | "
              f"Valid: {'✓' if valid else '✗'} | '111' count: {count}")
    
    print()
    print("=== Metin Kodlama Testi ===")
    test_text = "Hello GZR!"
    print(f"Orijinal: {test_text}")
    
    encoded = text_to_gzr(test_text)
    print(f"GZR Encoded ({len(encoded)} bits): {encoded[:50]}...")
    
    decoded_text = gzr_to_text(encoded)
    print(f"Decoded: {decoded_text}")
    
    valid, count_111 = verify_no_111_pattern(encoded)
    density = calculate_bit_density(encoded)
    
    print(f"\n'111' pattern count: {count_111}")
    print(f"Bit density (1s): {density:.4f} ({density*100:.2f}%)")
    print(f"Valid GZR: {'✓' if valid else '✗'}")
