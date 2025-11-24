# 🛡️ Telegram Data Breach Analyzer Bot

Bot Telegram canggih untuk menganalisis dokumen pelanggaran data (data breach) dan profiling pengguna dengan kemampuan ekstraksi data otomatis, analisis risiko, dan pelaporan terstruktur.

## 🎯 Fitur Utama

### 1. Ekstraksi Data Otomatis
- **Input Multiformat**: PDF, TXT, atau teks mentah
- **Parsing Cerdas**:
  - Nama Lengkap
  - Email (validasi regex)
  - Nomor Telepon (format internasional)
  - Alamat (dengan geolokasi)
  - Tanggal Lahir (multi-format)
  - Password Hash (MD5, bcrypt, SHA-256, Argon2)
  - Data Sensitif (Passport, ID Telegram, Channel)

### 2. Analisis Mendalam
- **Konsistensi Data**: Cross-reference data dari berbagai sumber
- **Assessment Risiko**: 
  - Password storage security
  - Eksposur data sensitif
  - Pola perilaku anomali
- **Geolokasi**: Deteksi inkonsistensi lokasi

### 3. Pelaporan Terstruktur
- Format Markdown yang mudah dibaca
- Data masking untuk privasi
- Rekomendasi tindakan keamanan

## 🚀 Instalasi

```bash
# Clone repository
git clone <repository-url>
cd project

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env dan tambahkan TELEGRAM_BOT_TOKEN
```

## ⚙️ Konfigurasi

Buat file `.env` dengan konfigurasi berikut:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
LOG_LEVEL=INFO
MAX_FILE_SIZE=20971520  # 20MB
ALLOWED_EXTENSIONS=pdf,txt
```

## 📖 Penggunaan

### Menjalankan Bot

```bash
python bot.py
```

### Perintah Bot

- `/start` - Memulai bot dan menampilkan panduan
- `/help` - Menampilkan bantuan
- `/analyze` - Menganalisis dokumen atau teks
- `/status` - Melihat status analisis

### Cara Menganalisis Data

1. Kirim perintah `/analyze`
2. Upload dokumen (PDF/TXT) atau kirim teks mentah
3. Bot akan memproses dan menghasilkan laporan lengkap

## 🏗️ Struktur Project

```
.
├── bot.py                 # Entry point aplikasi
├── config.py              # Konfigurasi aplikasi
├── requirements.txt       # Dependencies
├── .env.example          # Template environment variables
├── .gitignore            # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── handlers/         # Telegram bot handlers
│   │   ├── __init__.py
│   │   ├── start.py
│   │   ├── analyze.py
│   │   └── help.py
│   ├── parsers/          # Data extraction parsers
│   │   ├── __init__.py
│   │   ├── document_parser.py
│   │   ├── data_extractor.py
│   │   └── patterns.py
│   ├── analyzers/        # Data analysis modules
│   │   ├── __init__.py
│   │   ├── risk_assessor.py
│   │   ├── consistency_checker.py
│   │   └── behavior_analyzer.py
│   ├── reporters/        # Report generation
│   │   ├── __init__.py
│   │   ├── report_generator.py
│   │   └── data_masker.py
│   └── utils/            # Utility functions
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
└── tests/                # Unit tests
    ├── __init__.py
    ├── test_parsers.py
    ├── test_analyzers.py
    └── test_reporters.py
```

## 🔒 Keamanan & Privasi

- **Data Masking**: Semua PII (Personally Identifiable Information) di-mask dalam laporan
- **Temporary Storage**: Data diproses di memory, tidak disimpan permanen
- **Logging**: Hanya metadata yang di-log, bukan data sensitif

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_parsers.py

# Run with coverage
pytest --cov=src tests/
```

## 📝 Lisensi

MIT License

## 🤝 Kontribusi

Pull requests are welcome! Untuk perubahan besar, silakan buka issue terlebih dahulu.

## ⚠️ Disclaimer

Bot ini dibuat untuk tujuan edukasi dan penelitian keamanan. Penggunaan untuk tujuan ilegal adalah tanggung jawab pengguna.
