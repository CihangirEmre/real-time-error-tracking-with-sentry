"""
Sentry demo views.

Her view farklı bir hata senaryosu tetikler.
Sunumda her birini tarayıcıda aç, sonra Sentry dashboard'a geçip
nasıl göründüğünü canlı olarak göster.
"""

import time
import sentry_sdk
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User


def home(request):
    """Ana sayfa - tüm demo linklerini listeler."""
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="utf-8">
        <title>Sentry Django Demo</title>
        <style>
            body { font-family: -apple-system, sans-serif; max-width: 720px;
                   margin: 40px auto; padding: 20px; line-height: 1.6; }
            h1 { color: #362d59; }
            .card { background: #f6f6f8; padding: 16px 20px; margin: 12px 0;
                    border-radius: 8px; border-left: 4px solid #7553ff; }
            .card a { color: #7553ff; font-weight: 600; text-decoration: none;
                      font-size: 1.1em; }
            .card a:hover { text-decoration: underline; }
            .desc { color: #666; margin-top: 4px; font-size: 0.9em; }
            code { background: #eee; padding: 2px 6px; border-radius: 3px;
                   font-size: 0.85em; }
            .badge { display: inline-block; background: #7553ff; color: white;
                     padding: 2px 8px; border-radius: 10px; font-size: 0.75em;
                     margin-left: 8px; }
        </style>
    </head>
    <body>
        <h1>🔭 Sentry + Django Demo</h1>
        <p>Her linke tıkladığında farklı bir hata tetiklenir ve Sentry dashboard'a gönderilir.</p>

        <div class="card">
            <a href="/zero-division/">1. ZeroDivisionError tetikle</a>
            <span class="badge">Error</span>
            <div class="desc">Klasik bir Python exception — stack trace ve local variables göster.</div>
        </div>

        <div class="card">
            <a href="/key-error/">2. KeyError tetikle</a>
            <span class="badge">Error</span>
            <div class="desc">Birkaç kez yenile → Sentry'de event count'un arttığını göster.</div>
        </div>

        <div class="card">
            <a href="/db-error/">3. Database Error tetikle</a>
            <span class="badge">DB</span>
            <div class="desc">ORM hatası — Sentry query context'i otomatik ekler.</div>
        </div>

        <div class="card">
            <a href="/slow/">4. Yavaş endpoint (3sn)</a>
            <span class="badge">Performance</span>
            <div class="desc">Performance sekmesinde transaction süresini göster.</div>
        </div>

        <div class="card">
            <a href="/custom-error/">5. Manuel mesaj gönder</a>
            <span class="badge">Message</span>
            <div class="desc"><code>capture_message()</code> ile hata olmadan log gönderimi.</div>
        </div>

        <div class="card">
            <a href="/user-context/?user_id=42&email=demo@test.com">6. Kullanıcı context'i ile hata</a>
            <span class="badge">Context</span>
            <div class="desc">Sentry'de "Tags" kısmında kullanıcıyı göster.</div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def zero_division(request):
    """
    🔥 Klasik Python hatası.
    Sentry'de göster:
    - Stack trace (hangi satır)
    - Local variables (a=10, b=0 değerleri görünür)
    - Request info (URL, method, headers)
    """
    a = 10
    b = 0
    sonuc = a / b  # 💥 ZeroDivisionError
    return HttpResponse(f"Sonuç: {sonuc}")


def key_error(request):
    """
    🔥 KeyError — Sentry'de aynı hatanın gruplandığını göstermek için.
    Bu endpoint'i 3-4 kez yenile, Sentry issue count'un arttığını izle.
    """
    kullanici_verisi = {"ad": "Cihangir", "okul": "Kocaeli Üniversitesi"}
    telefon = kullanici_verisi["telefon"]  # 💥 KeyError
    return HttpResponse(f"Telefon: {telefon}")


def db_error(request):
    """
    🔥 Var olmayan kullanıcıyı sorgulama.
    Sentry'de database query context'i otomatik eklenir.
    """
    user = User.objects.get(username="bu_kullanici_yok_12345")  # 💥 DoesNotExist
    return HttpResponse(f"Kullanıcı: {user.username}")


def slow_endpoint(request):
    """
    🐢 Yavaş endpoint — Performance monitoring demosu.

    Sentry'de Performance sekmesine git:
    - Transaction: "GET /slow/"
    - Duration: ~3 saniye
    - Breakdown: hangi işlem ne kadar sürdü
    """
    with sentry_sdk.start_span(op="task", description="Simulated heavy computation"):
        time.sleep(1)

    with sentry_sdk.start_span(op="task", description="Fake DB query"):
        time.sleep(1)

    with sentry_sdk.start_span(op="task", description="External API call"):
        time.sleep(1)

    return JsonResponse({
        "status": "ok",
        "message": "3 saniyelik işlem tamamlandı",
        "note": "Sentry Performance sekmesinde transaction'ı incele"
    })


def custom_error(request):
    """
    📝 Manuel mesaj / breadcrumb gönderimi.
    Exception olmasa bile Sentry'ye bilgi gönderebilirsin.
    """
    # Breadcrumb: Sentry'ye "şu anda bu oldu" notu bırak
    sentry_sdk.add_breadcrumb(
        category="demo",
        message="Kullanıcı custom-error endpoint'ini çağırdı",
        level="info",
    )

    # Custom tag ekle
    sentry_sdk.set_tag("demo_tipi", "manuel_mesaj")

    # Extra context
    sentry_sdk.set_context("demo_bilgisi", {
        "sunum": "Bitirme Projesi",
        "konu": "Sentry Entegrasyonu",
        "ogrenci": "Cihangir",
    })

    # Mesaj gönder (hata değil, sadece log)
    sentry_sdk.capture_message(
        "Bu bir test mesajı — Sentry'ye manuel gönderildi",
        level="warning",
    )

    return JsonResponse({
        "status": "ok",
        "message": "Sentry'ye manuel mesaj gönderildi. Dashboard'u kontrol et."
    })


def user_context(request):
    """
    👤 Kullanıcı context'i ile hata.
    Hangi kullanıcının hatayı yaşadığı Sentry'de 'user' tag'i olarak görünür.
    """
    user_id = request.GET.get("user_id", "anonim")
    email = request.GET.get("email", "unknown@example.com")

    # Kullanıcı bilgisini Sentry'ye bağla
    sentry_sdk.set_user({
        "id": user_id,
        "email": email,
        "ip_address": request.META.get("REMOTE_ADDR"),
    })

    # Şimdi bir hata fırlat — Sentry'de bu kullanıcıyla ilişkili görünecek
    sayilar = [1, 2, 3]
    eleman = sayilar[99]  # 💥 IndexError
    return HttpResponse(f"Eleman: {eleman}")
