# 🔍 Telegram Data Breach Search Bot

Bot Telegram untuk mencari informasi data breach di berbagai platform dengan sistem kredit dan pencarian multi-query.

## 🎯 Fitur Utama

### 1. Sistem Kredit
- **51 Kredit Gratis** saat pertama kali menggunakan bot
- Setiap pencarian menggunakan 1 kredit
- Tracking kredit real-time per user

### 2. Jenis Pencarian
- **Email**: Pencarian lengkap, nama saja, atau domain saja
  - `example@gmail.com` - email lengkap
  - `example@` - nama saja
  - `@gmail.com` - domain saja
- **Nomor Telepon**: Format internasional atau lokal
  - `+79024196473` - dengan kode negara
  - `79024196473` - format lokal
- **Kendaraan**: Plat nomor atau VIN
  - `O999МУ777` - plat nomor
  - `XTA21150053965897` - nomor VIN
- **IP Address**: IPv4
  - `127.0.0.1`
- **Nama**: Pencarian berdasarkan nama
  - `Muhammad Sobri Maulana`
- **Combo Search**: Kombinasi nama dengan identifier lain
  - `Sergio 79024196473`
  - `Ivan Kuznetsov 09/18/1991`
  - `example@gmail.com 889Kkt`
- **Multi Query**: Beberapa pencarian sekaligus (satu query per baris)

### 3. Hasil Pencarian
- Menampilkan platform yang memiliki data
- Jumlah data points per platform
- Ringkasan total platform dan data points
- Kredit yang digunakan dan sisa kredit

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
WEBSITE_URL=https://scanyour.name
INITIAL_CREDITS=51
CREDIT_COST_PER_SEARCH=1
MAX_MULTI_QUERY=10
```

## 📖 Penggunaan

### Menjalankan Bot

```bash
python bot.py
```

### Perintah Bot

- `/start` - Mulai bot dan dapatkan 51 kredit gratis
- `/help` - Panduan lengkap penggunaan
- `/author` - Informasi lengkap tentang developer dan link donasi

### Cara Melakukan Pencarian

1. Kirim `/start` untuk mendapatkan kredit gratis
2. Kirim query pencarian langsung (tidak perlu command):
   - Email: `example@gmail.com`
   - Phone: `+79024196473`
   - Name: `Muhammad Sobri Maulana`
   - Multi-query: Kirim beberapa query, masing-masing di baris baru
3. Bot akan mencari di database dan menampilkan hasil

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
│   │   ├── start.py      # /start command
│   │   ├── help.py       # /help command
│   │   ├── author.py     # /author command
│   │   └── search.py     # Search query handler
│   ├── parsers/          # Query parsing
│   │   ├── __init__.py
│   │   ├── search_parser.py  # Parse search queries
│   │   └── ...           # Legacy parsers
│   ├── search/           # Search engine
│   │   ├── __init__.py
│   │   ├── search_engine.py    # Simulate searches
│   │   └── results_formatter.py # Format results
│   └── utils/            # Utility functions
│       ├── __init__.py
│       ├── user_manager.py  # Credit management
│       ├── validators.py
│       └── helpers.py
└── tests/                # Unit tests
```

## 🔒 Keamanan & Privasi

- **In-Memory Storage**: Data pengguna disimpan di memory (tidak persisten)
- **No Data Collection**: Bot tidak menyimpan hasil pencarian
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

## 👨‍💻 Author

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

- 🌐 GitHub: [github.com/sobri3195](https://github.com/sobri3195)
- 📧 Email: [muhammadsobrimaulana31@gmail.com](mailto:muhammadsobrimaulana31@gmail.com)
- 🌍 Website: [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)
- 🚀 Portfolio: [muhammad-sobri-maulana-kvr6a.sevalla.page](https://muhammad-sobri-maulana-kvr6a.sevalla.page/)

### 🔗 Social Media

- 📺 YouTube: [@muhammadsobrimaulana6013](https://www.youtube.com/@muhammadsobrimaulana6013)
- 💬 Telegram: [winlin_exploit](https://t.me/winlin_exploit)
- 🎵 TikTok: [@dr.sobri](https://www.tiktok.com/@dr.sobri)
- 👥 WhatsApp Group: [Join Group](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)

### 💖 Support & Donation

Jika project ini bermanfaat, Anda dapat memberikan dukungan melalui:

- ☕ [Trakteer](https://trakteer.id/g9mkave5gauns962u07t)
- 💳 [Lynk.id](https://lynk.id/muhsobrimaulana)
- 🛍️ [Gumroad](https://maulanasobri.gumroad.com/)
- 🎨 [Karya Karsa](https://karyakarsa.com/muhammadsobrimaulana)
- 💰 [Nyawer](https://nyawer.co/MuhammadSobriMaulana)

## ⚠️ Disclaimer

Bot ini dibuat untuk tujuan edukasi dan demonstrasi. Hasil pencarian adalah simulasi dan tidak mengakses database breach yang sebenarnya. Penggunaan untuk tujuan ilegal adalah tanggung jawab pengguna.

## 📋 Catatan

- Hasil pencarian disimulasikan (tidak mengakses database breach yang sebenarnya)
- Platform dan jumlah data yang ditampilkan bersifat random untuk demonstrasi
- Kredit pengguna disimpan di memory dan akan reset saat bot di-restart
