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

    # Yedek (Varsayılan) Mesaj - Groq çalışmazsa bu devreye girer
    baslik = "Günaydın Sena! 🌸"
    icerik = "Mithat seni çok seviyor, bugün senin günün olsun! ✨"

    if groq_api_key:
        try:
            print("🤖 Groq'a bağlanılıyor...")
            groq_url = "https://api.groq.com/openai/v1/chat/completions"
            groq_headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            
            # Anlık zamanı alıyoruz ki yapay zeka her çalıştığında yepyeni bir çıktı versin
            anlik_zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            system_prompt = "Sen bir ChatGPT'sin ve senin dilinden Mithat'ın kız arkadaşı Sena'ya özel, YKS sınavına hazırlanan kız arkadaşına moral verecek, samimi, pozitif, motive edici, olumlamalar içeren ve 💖✨ gibi onu mutlu edecek emojilerle dolu bir günaydın mesajı oluşturacaksın. Mesajda mutlaka 'Mithat seni çok seviyor' diye belirt ve 'Bugün Sena ve Mithat'ın günü olsun!' ifadesini ekle. Onun sakin kalmasını, stresten uzak durmasını hatırlat."
            
            user_prompt = f"Sistem Saati: {anlik_zaman}. Sena'ya gülümsetecek, enerjisini yükseltecek ve Mithat'ın yanında olduğunu hissettirecek, en az 3-4 cümlelik doyurucu ve biraz uzun bir günaydın mesajı yaz. ASLA önceki mesajlarını tekrar etme, her gün yepyeni ve eşsiz bir motivasyon konusu bul. Ona gücüne ne kadar güvendiğini ve YKS'de kesinlikle başarılı olacağına olan inancını ekle. Mesajın sonuna '#ChatGPT Kankan#' eklemeyi unutma."

            groq_payload = {
                "model": "llama-3.1-70b-versatile", # YENİ VE GÜNCEL MODEL BURADA
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.8, 
                "max_tokens": 250
            }

            response = requests.post(groq_url, headers=groq_headers, json=groq_payload)
            response_data = response.json()
            
            if response.status_code == 200:
                ai_mesaj = response_data['choices'][0]['message']['content'].strip()
                icerik = ai_mesaj
                baslik = "Yeni bir mesajın var! 💌"
                print("✅ Groq harika ve uzun bir mesaj üretti!")
            else:
                print(f"❌ Groq API Hatası: {response_data}")

        except Exception as e:
            print("❌ Yapay zeka bağlantısında hata:", e)
    else:
        print("⚠️ GROQ_API_KEY bulunamadı!")

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
