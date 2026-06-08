import requests
import json
import os

def surpriz_bildirim_gonder():
    onesignal_api_key = os.environ.get("ONESIGNAL_REST_API_KEY")
    groq_api_key = os.environ.get("GROQ_API_KEY")
    
    if not onesignal_api_key:
        print("❌ HATA: ONESIGNAL_REST_API_KEY bulunamadı!")
        return

    # Varsayılan Mesaj (Yapay zeka o an çalışmazsa bu gider)
    baslik = "Günaydın Sena! 🌸"
    icerik = "Mithat seni çok seviyor, bugün senin günün olsun! ✨"

    # Groq (Yapay Zeka) ile Mesaj Üretimi
    if groq_api_key:
        try:
            print("🤖 Groq'a bağlanılıyor...")
            groq_url = "https://api.groq.com/openai/v1/chat/completions"
            groq_headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            
            system_prompt = "Sen bir ChatGPT'sin ve senin dilinden Mithat'ın kız arkadaşı Sena'ya özel, YKS sınavına hazırlanan kız arkadaşına moral verecek, samimi, pozitif, motive edici, olumlamalar içeren ve 💖✨ gibi onu mutlu edecek emojilerle dolu kısa bir günaydın mesajı oluşturacaksın. Mesajda mutlaka 'Mithat seni çok seviyor' diye belirt ve 'Bugün Sena ve Mithat'ın günü olsun!' ifadesini ekle. Onun sakin kalmasını, stresten uzak durmasını hatırlat."
            
            user_prompt = "Sena'ya gülümsetecek, enerjisini yükseltecek ve Mithat'ın yanında olduğunu hissettirecek 1-2 cümlelik eşsiz bir günaydın mesajı yaz. Ona gücüne ne kadar güvendiğini ve başarılı olacağına olan inancı ekle. Mesajın sonuna '#ChatGPT Kankan#' eklemeyi unutma."

            groq_payload = {
                "model": "llama3-70b-8192", # Groq'un en zeki ve edebi modeli
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150
            }

            response = requests.post(groq_url, headers=groq_headers, json=groq_payload)
            response_data = response.json()
            
            if response.status_code == 200:
                # Groq'tan gelen cevabı alıyoruz
                ai_mesaj = response_data['choices'][0]['message']['content'].strip()
                icerik = ai_mesaj
                baslik = "Yeni bir mesajın var! 💌" # Bildirim başlığı
                print("✅ Groq harika bir mesaj üretti!")
            else:
                print(f"❌ Groq API Hatası: {response_data}")

        except Exception as e:
            print("❌ Yapay zeka bağlantısında hata:", e)
    else:
        print("⚠️ GROQ_API_KEY bulunamadı! Lütfen GitHub Secrets'a ekle.")

    # 1. Site için mesaj.json dosyasını güncelle
    with open("mesaj.json", "w", encoding="utf-8") as f:
        json.dump({"baslik": baslik, "icerik": icerik}, f, ensure_ascii=False, indent=4)
    
    # 2. OneSignal Bildirimini Fırlat
    os_header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {onesignal_api_key}"
    }

    os_payload = {
        "app_id": "f66f725a-9c4b-4f45-8f5c-33118e634400",
        "included_segments": ["Total Subscriptions"], 
        "headings": {"en": baslik},
        "contents": {"en": icerik}
    }
    
    os_response = requests.post("https://onesignal.com/api/v1/notifications", headers=os_header, data=json.dumps(os_payload))
    
    if os_response.status_code == 200:
        print(f"✅ Bildirim fırlatıldı!")
    else:
        print(f"❌ Bildirim Hatası: {os_response.status_code} - {os_response.text}")

surpriz_bildirim_gonder()
