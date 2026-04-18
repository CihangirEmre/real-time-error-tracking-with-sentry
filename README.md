# Sentry + Django Demo

Bu demo, Sentry'nin Django uygulamalarında nasıl entegre edildiğini ve gerçek zamanlı hata izleme özelliklerini göstermek için hazırlanmıştır.

## 🎯 Demo Amacı

Canlı bir Django uygulamasında kasıtlı olarak farklı tipte hatalar tetikleyip Sentry dashboard'da nasıl göründüklerini sunum sırasında göstermek.

---

## 📋 Ön Gereksinimler

- Python 3.9+
- pip
- Sentry hesabı (ücretsiz): https://sentry.io/signup/

---

## 🚀 Kurulum (5 Adım)

### 1. Sentry Projesi Oluştur
1. https://sentry.io adresinde hesap aç
2. **Create Project** → **Django** seç
3. Proje adı ver (örn. `django-demo`)
4. Sana verilen **DSN** linkini kopyala (şu formatta: `https://xxxxx@o0.ingest.sentry.io/0`)

### 2. Sanal Ortam + Bağımlılıklar

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. DSN'i Ayarla

```bash
export SENTRY_DSN="https://xxxxx@o0.ingest.sentry.io/0"
# Windows PowerShell: $env:SENTRY_DSN="..."
```

Alternatif: `demo_project/settings.py` içinde doğrudan yazabilirsin (demo için).

### 4. Migrate + Çalıştır

```bash
python manage.py migrate
python manage.py runserver
```

### 5. Tarayıcıda Aç

`http://127.0.0.1:8000/`

---

## 🎬 Sunum Akışı (Canlı Demo)

Her endpoint Sentry'de farklı bir özelliği gösterir:

| Endpoint | Ne Tetikler | Sentry'de Göstereceğin |
|---|---|---|
| `/` | Ana sayfa | — |
| `/zero-division/` | `ZeroDivisionError` | Stack trace, local variables, breadcrumbs |
| `/key-error/` | `KeyError` | Hata gruplama (aynı hata X kez) |
| `/db-error/` | Var olmayan kullanıcı sorgusu | Database query context |
| `/slow/` | 3 saniye bekleyen endpoint | **Performance monitoring** (transaction) |
| `/custom-error/` | `capture_message()` | Manuel log gönderimi |
| `/user-context/` | Kullanıcı bilgisi ile hata | User context attachment |

### Önerilen Demo Sırası (~5 dakika)

1. **`/zero-division/`** → Sentry dashboard'a geç, hatanın detayını aç. Şunları göster:
   - Tam stack trace
   - Her frame'deki local variable değerleri
   - Request bilgisi (URL, headers, user agent)
   - Breadcrumbs (kullanıcının ne yaptığı)

2. **`/key-error/`** → Sayfayı 3-4 kez yenile. Sentry'de aynı hatanın **gruplandığını** ve event sayısının arttığını göster.

3. **`/user-context/?user_id=42`** → Sentry'de hatanın hangi kullanıcıda oluştuğunu göster (Issues → Tags → user).

4. **`/slow/`** → **Performance** sekmesine geç, transaction'ı göster (3 saniyelik gecikme).

5. **Release tracking** → Terminalde `git commit` yapıp `SENTRY_RELEASE` değiştirince hataların release'e bağlandığını göster.

---

## 📁 Dosya Yapısı

```
sentry-demo/
├── README.md              ← bu dosya
├── requirements.txt
├── manage.py
├── demo_project/
│   ├── __init__.py
│   ├── settings.py        ← Sentry entegrasyonu burada
│   ├── urls.py
│   └── wsgi.py
└── demo_app/
    ├── __init__.py
    ├── apps.py
    ├── views.py           ← Demo endpoint'leri
    └── urls.py
```

---

## 🔑 Kritik Kod Parçaları (Sunumda Gösterilecek)

### Entegrasyon (`settings.py`)
Sadece **6 satır** — Sentry'nin en büyük avantajlarından biri bu basitlik:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,       # Performance monitoring
    send_default_pii=True,         # Kullanıcı bilgisi gönder
)
```

Bu kadar! Hiçbir view'da `try/except` yazmadan tüm unhandled exception'lar otomatik yakalanır.

---

## 💡 Sunumda Vurgulanacak Noktalar

- **Sıfır kod değişikliği**: Mevcut view'lara dokunmadan tüm hatalar yakalanıyor
- **Context zenginliği**: Stack trace + local vars + request + user = reproduce etmeden debug
- **Gruplama**: Aynı hata 1000 kez olsa 1 issue, sağdaki counter artar
- **Performans**: `traces_sample_rate` ile sampling, production'da maliyet kontrolü
- **Privacy**: `send_default_pii=False` ile KVKK/GDPR uyumu — self-hosted seçeneği de mevcut

---

## 🛠 Sorun Giderme

- **Sentry'de event görünmüyor:** DSN doğru mu? `sentry_sdk.capture_message("test")` ile test et.
- **Import hatası:** `pip install -r requirements.txt` tekrar çalıştır.
- **Port çakışması:** `python manage.py runserver 8080`
