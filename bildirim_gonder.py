import requests
import json
import os

def surpriz_bildirim_gonder():
    # Şifreyi GitHub Secrets üzerinden çekiyoruz (Güvenli Yol)
    api_key = os.environ.get("ONESIGNAL_REST_API_KEY")
    
    if not api_key:
        print("❌ HATA: API Anahtarı bulunamadı!")
        return

    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {api_key}"
    }

    payload = {
        "app_id": "f66f725a-9c4b-4f45-8f5c-33118e634400",
        # Artık çalıştığını bildiğimiz doğru kitle adı:
        "included_segments": ["Total Subscriptions"], 
        "headings": {"en": "Sürpriz! ✨"},
        "contents": {"en": "Kaplumbağan bugün de seni çok düşünüyor... 🐢"}
    }
    
    response = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    
    if response.status_code == 200:
        print("✅ Bildirim başarıyla fırlatıldı!")
    else:
        print(f"❌ Hata oluştu: {response.status_code} - {response.text}")

surpriz_bildirim_gonder()
