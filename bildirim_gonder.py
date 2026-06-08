import requests
import json
import os
import datetime

def surpriz_bildirim_gonder():
    onesignal_api_key = os.environ.get("ONESIGNAL_REST_API_KEY")
    groq_api_key = os.environ.get("GROQ_API_KEY")
    
    if not onesignal_api_key:
        print("❌ HATA: ONESIGNAL_REST_API_KEY bulunamadı!")
        return

    ozel_imza = "\n\n#ChatGPT Kankan#\nİnşallah tıp olacak\nAmin amin amin\nAminnnnnnn"
    baslik = "Günaydın Sena! 🌸"
    icerik = "Mithat seni çok seviyor, bugün senin günün olsun! ✨" + ozel_imza

    if groq_api_key:
        try:
            groq_url = "https://api.groq.com/openai/v1/chat/completions"
            groq_headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
            anlik_zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            system_prompt = "Sena'ya özel, YKS adayı, pozitif, motive edici, 'Mithat seni çok seviyor' ve 'Bugün Sena ve Mithat'ın günü olsun' cümlelerini içeren günaydın mesajı."
            user_prompt = f"Tarih: {anlik_zaman}. Motivasyon dolu, tıp hedefi için destekleyici eşsiz bir mesaj yaz."

            groq_payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "temperature": 0.8, "max_tokens": 250}

            response = requests.post(groq_url, headers=groq_headers, json=groq_payload)
            if response.status_code == 200:
                ai_mesaj = response.json()['choices'][0]['message']['content'].strip()
                ai_mesaj = ai_mesaj.replace("#ChatGPT Kankan#", "").strip()
                icerik = ai_mesaj + ozel_imza
                baslik = "Yeni bir mesajın var! 💌"
        except Exception as e:
            print("Hata:", e)

    # ÖNCE JSON GÜNCELLENİYOR
    with open("mesaj.json", "w", encoding="utf-8") as f:
        json.dump({"baslik": baslik, "icerik": icerik}, f, ensure_ascii=False, indent=4)
    
    # SONRA BİLDİRİM GİDİYOR
    os_header = {"Content-Type": "application/json; charset=utf-8", "Authorization": f"Basic {onesignal_api_key}"}
    os_payload = {
        "app_id": "f66f725a-9c4b-4f45-8f5c-33118e634400",
        "included_segments": ["Total Subscriptions"], 
        "headings": {"en": baslik},
        "contents": {"en": icerik},
        "url": "https://senamithat.site/mesaj.html" 
    }
    
    requests.post("https://onesignal.com/api/v1/notifications", headers=os_header, data=json.dumps(os_payload))

surpriz_bildirim_gonder()
