import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

ENV_FILE = Path(".env")
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_REST_API_KEY = os.getenv("ONESIGNAL_REST_API_KEY")

eksik_degiskenler = [isim for isim, deger in {
    "GROQ_API_KEY": GROQ_API_KEY,
    "ONESIGNAL_APP_ID": ONESIGNAL_APP_ID,
    "ONESIGNAL_REST_API_KEY": ONESIGNAL_REST_API_KEY,
}.items() if not deger]

if eksik_degiskenler:
    sys.exit(f"Hata: Eksik ortam değişkenleri var: {', '.join(eksik_degiskenler)}")

SYSTEM_PROMPT = "Sen Mithat'ın kız arkadaşı Sena'ya özel, gününe neşe katacak, samimi, pozitif ve 💖✨ gibi emojilerle dolu kısa bir bildirim mesajı oluşturacaksın. Sena şu anda zorlu bir sınava hazırlanıyor. Mesajında onun ne kadar çok çalıştığını, bu emeklerinin karşılığını kesinlikle alacağını ve bu başarıyı çok hak ettiğini vurgula. Ona stres yapmaması gerektiğini, derin bir nefes alıp sakin kalmasını tatlı bir dille hatırlat. Mesajda mutlaka 'Mithat seni çok seviyor' diye belirt ve 'Bugün Sena ve Mithat'ın günü olsun!' ifadesini ekle."
USER_PROMPT = "Sena'yı gülümsetecek, sınav stresini unutturup enerjisini yükseltecek ve Mithat'ın her zaman onun yanında olduğunu hissettirecek 1-2 cümlelik eşsiz bir motivasyon mesajı yaz. Emeklerinin boşa gitmeyeceğini hatırlat. Mesajın sonuna '#ChatGPT Kankan#' eklemeyi unutma."

def groq_mesaj_uret() -> str:
    print("Groq API'sine bağlanılıyor...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
        "model": "llama3-8b-8192", 
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        "temperature": 1,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get("choices") and result["choices"][0].get("message"):
            return result["choices"][0]["message"]["content"].strip()
        else:
            sys.exit(f"Beklenmeyen API formatı: {result}")
            
    except Exception as e:
        sys.exit(f"Mesaj üretilirken hata: {e}")

def bildirim_gonder(mesaj: str) -> None:
    print("OneSignal üzerinden bildirim fırlatılıyor...")
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}"
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["Subscribed Users"],
        "headings": {"en": "🌸 Günaydın Sena!", "tr": "🌸 Günaydın Sena!"},
        "contents": {"en": mesaj, "tr": mesaj}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ Bildirim başarıyla fırlatıldı!")
    except Exception as e:
        sys.exit(f"Bildirim gönderilirken hata: {e}")

if __name__ == "__main__":
    uretilen_mesaj = groq_mesaj_uret()
    print("📨 Üretilen Mesaj:", uretilen_mesaj)
    bildirim_gonder(uretilen_mesaj)
