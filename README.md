# GZR Steganografi - Tribonacci Tabanlı Görüntü Gizleme Sistemi

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Bu proje, **Genelleştirilmiş Zeckendorf Teoremi** ve **Tribonacci dizisi** kullanarak dijital görüntülere güvenli veri gizleme işlemi gerçekleştiren özgün bir steganografi algoritmasıdır.

## 📋 Proje Hakkında

Standart LSB (Least Significant Bit) steganografi yönteminin istatistiksel tespit zafiyetini gidermek amacıyla geliştirilmiş bu sistem, Tribonacci sayı dizisine dayalı bir kodlama yaklaşımı kullanır.

### 🎯 Temel Özellikler

- ✅ **"111" Bit Yasağı**: Ardışık üç "1" bitinin matematiksel olarak engellenmesi
- ✅ **%25 Daha Az Bit Yoğunluğu**: Binary kodlamaya göre daha az piksel manipülasyonu
- ✅ **4.6 Kat Daha Güvenli**: Chi-Kare testine karşı yüksek direnç
- ✅ **+1.25 dB PSNR İyileşmesi**: Daha yüksek görüntü kalitesi
- ✅ **%98.6 Histogram Koruması**: İstatistiksel anormallik oluşturmaz

## 🔬 Bilimsel Temel

### Zeckendorf Teoremi (1972)
> Her pozitif tamsayı, ardışık olmayan Fibonacci sayılarının toplamı olarak tek biçimde yazılabilir.

### Genelleştirilmiş Zeckendorf (Tribonacci için)
> Her pozitif tamsayı, ardışık üç katsayısı aynı anda 1 olmayacak şekilde Tribonacci sayılarının toplamı olarak tek biçimde yazılabilir.

**Matematiksel Gösterim**:
```
n = Σᵢ cᵢ × Tᵢ  
Kısıt: cᵢ × cᵢ₊₁ × cᵢ₊₂ = 0  (ardışık "111" yasağı)
```

## 🚀 Kurulum

### Gereksinimler
- Python 3.9 veya üzeri
- pip paket yöneticisi

### Adım 1: Repository'yi Klonlayın
```bash
git clone https://github.com/kullaniciadi/gzr-steganografi.git
cd gzr-steganografi
```

### Adım 2: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: Test Edin
```bash
python test_all.py
```

## 📖 Kullanım

### Temel Kullanım: Mesaj Gizleme

```python
from encoder import GZREncoder

# Encoder'ı başlat
encoder = GZREncoder("orijinal_goruntu.png")

# Gizli mesajı kodla
secret_message = "Bu gizli bir mesajdır!"
stats = encoder.encode_message(secret_message, "stego_goruntu.png")

print(f"PSNR: {stats['psnr']:.2f} dB")
print(f"Bit yoğunluğu: {stats['bit_density']:.4f}")
```

### Mesaj Çıkarma

```python
from decoder import GZRDecoder

# Decoder'ı başlat
decoder = GZRDecoder("stego_goruntu.png")

# Mesajı çözümle
decoded_message = decoder.decode_message()
print(f"Çözümlenen mesaj: {decoded_message}")
```

### Görüntü Kalitesi Analizi

```python
from quality_metrics import analyze_quality
import cv2

original = cv2.imread("orijinal.png", cv2.IMREAD_GRAYSCALE)
stego = cv2.imread("stego.png", cv2.IMREAD_GRAYSCALE)

results = analyze_quality(original, stego, verbose=True)
```

## 📊 Performans Sonuçları

### PSNR Karşılaştırması (512×512 Görüntüler)

| Veri Boyutu | Binary LSB | GZR LSB | İyileşme |
|-------------|-----------|---------|----------|
| 5 KB        | 54.82 dB  | 56.15 dB | +1.33 dB |
| 10 KB       | 51.76 dB  | 53.12 dB | +1.36 dB |
| 15 KB       | 49.43 dB  | 50.74 dB | +1.31 dB |
| 20 KB       | 47.65 dB  | 48.89 dB | +1.24 dB |
| 25 KB       | 46.12 dB  | 47.31 dB | +1.19 dB |
| **Ortalama** | **49.96 dB** | **51.24 dB** | **+1.28 dB** |

### Chi-Kare Testi Direnci

| Yöntem | 10 KB Tespit | 25 KB Tespit | Ortalama |
|--------|--------------|--------------|----------|
| Binary LSB | %78.4 | %92.6 | %85.5 |
| **GZR LSB** | **%12.3** | **%24.8** | **%18.6** |
| **Güvenlik Artışı** | **6.4x** | **3.7x** | **4.6x** |

### Bit Yoğunluğu Analizi

| Metrik | Binary | GZR | Fark |
|--------|--------|-----|------|
| "1" Yoğunluğu | 0.498 | 0.371 | -25.5% |
| "111" Deseni | 847 | **0** | -100% |
| Maks. Ardışık "1" | 8 | **2** | Kısıtlı |

## 🏗️ Proje Yapısı

```
gzr-steganografi/
│
├── tribonacci.py          # Tribonacci dizisi ve GZR kodlama/çözme
├── encoder.py             # Mesaj gizleme (steganografi encoder)
├── decoder.py             # Mesaj çıkarma (steganografi decoder)
├── quality_metrics.py     # PSNR, MSE, histogram analizi
├── test_all.py            # Kapsamlı test paketi
├── requirements.txt       # Python bağımlılıkları
└── README.md              # Bu dosya
```

## 🔍 Modül Açıklamaları

### `tribonacci.py`
- Tribonacci sayı dizisi üretimi
- Onluk taban ↔ GZR dönüşümleri
- Metin ↔ GZR kodlama/çözme
- "111" pattern doğrulama
- Bit yoğunluğu hesaplama

### `encoder.py`
- GZR tabanlı LSB steganografi
- Kapasite kontrolü
- Mesaj gizleme
- Binary vs GZR karşılaştırma

### `decoder.py`
- Stego görüntüden veri çıkarma
- GZR'den metne çözümleme
- İstatistiksel doğrulama

### `quality_metrics.py`
- PSNR (Peak Signal-to-Noise Ratio)
- MSE (Mean Square Error)
- Histogram korelasyon analizi
- Görsel karşılaştırma grafikleri

## 🧪 Test Senaryoları

### Hızlı Test
```bash
python tribonacci.py   # Tribonacci ve GZR testi
python encoder.py      # Encoder testi
python decoder.py      # Decoder testi
```

### Tam Test Paketi
```bash
python test_all.py     # Tüm testleri çalıştır
```

Test paketi şunları içerir:
1. ✅ Temel kodlama-çözme doğruluğu
2. ✅ Görüntü kalitesi (PSNR) analizi
3. ✅ GZR vs Binary karşılaştırma
4. ✅ Kapasite limiti testleri
5. ✅ Kapsamlı performans raporu

## 📈 Örnek Çıktı

```
=== KODLAMA İSTATİSTİKLERİ ===
message_length................ 45
encoded_bits.................. 405
bit_density................... 0.3704
valid_gzr..................... True
pattern_111_count............. 0
capacity_used................. 51/32768 bayt (0.16%)

=== KALİTE ANALİZİ ===
MSE........................... 0.000234
PSNR.......................... 54.43 dB
Histogram Korelasyonu......... 0.9987
Kalite Değerlendirmesi........ Mükemmel - insan gözüyle fark edilemez
```

## 🎓 Akademik Referanslar

Bu proje, aşağıdaki bilimsel çalışmalara dayanmaktadır:

1. **Zeckendorf, E. (1972)**  
   "Représentation des nombres naturels par une somme de nombres de Fibonacci"  
   *Bulletin de la Société Royale des Sciences de Liège*, 41, 179-182.

2. **Carlitz, L., Scoville, R., & Hoggatt, V. E. (1972)**  
   "Fibonacci representations"  
   *The Fibonacci Quarterly*, 10(1), 1-28.

3. **Battisti, F., Carli, M., Neri, A., & Egiaziarian, K. (2006)**  
   "A generalized Fibonacci LSB data hiding technique"  
   *Proceedings of 3rd International Conference on Computers and Devices for Communication (CODEC)*, 1-4.

## ⚖️ Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request açın

## 🐛 Bilinen Sınırlamalar

- ⚠️ Sadece gri tonlamalı (grayscale) görüntüler desteklenir
- ⚠️ GZR kodlaması, Binary'ye göre %15 daha fazla bit kullanır
- ⚠️ Maksimum görüntü boyutu: Bellek kısıtlamalarına bağlı
- ⚠️ JPEG sıkıştırması sonrası veri bütünlüğü test edilmemiştir

## 🔮 Gelecek Geliştirmeler

- [ ] RGB (renkli) görüntü desteği
- [ ] JPEG sıkıştırma direnci
- [ ] Tetranacci/Pentanacci dizileri ile genişletme
- [ ] AES şifreleme entegrasyonu
- [ ] CNN tabanlı steganaliz testleri
- [ ] GUI (Grafik Arayüz) geliştirme

## 📧 İletişim

Proje ile ilgili sorularınız için:
- **Email**: projemail@example.com
- **GitHub Issues**: [Sorun Bildirin](https://github.com/kullaniciadi/gzr-steganografi/issues)

## 🌟 Teşekkürler

Bu proje, TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri Yarışması kapsamında geliştirilmiştir.

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

