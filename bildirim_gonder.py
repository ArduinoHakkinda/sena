import requests
import json
import os
import datetime

def surpriz_bildirim_gonder():
    onesignal_api_key = os.environ.get("ONESIGNAL_REST_API_KEY")
    groq_api_key = os.environ.get("GROQ_API_KEY")
    
    # GitHub'dan gelen seçimi alıyoruz (Boşsa veya saatliyse 'otomatik' sayılır)
    mesaj_turu_secimi = os.environ.get("MESAJ_TURU", "otomatik")
    if not mesaj_turu_secimi:
        mesaj_turu_secimi = "otomatik"
        
    manuel_mesaj = os.environ.get("OZEL_MESAJ", "").strip()
    
    if not onesignal_api_key:
        print("❌ HATA: ONESIGNAL_REST_API_KEY bulunamadı!")
        return

    ozel_imza = "\n\n#ChatGPT Kankan#\nİnşallah tıp olacak\namin amin amin\naminnnnnnn"
    
    # Eğer kutuya manuel yazı yazıldıysa her şeyi ezer, onu yollar:
    if manuel_mesaj:
        baslik = "Mithat'tan Sana Bir Mesaj Var! 💝"
        icerik = manuel_mesaj + ozel_imza
        mesaj_tipi = "manuel"
    else:
        # Menüden "otomatik" seçildiyse VEYA zamanlanmış görev çalıştıysa saate bakar
        if mesaj_turu_secimi == "otomatik":
            try:
                from datetime import timezone, timedelta
                tsi_zaman = datetime.datetime.now(timezone.utc) + timedelta(hours=3)
                current_hour = tsi_zaman.hour
            except Exception:
                current_hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).hour

            if 5 <= current_hour <= 12:
                mesaj_tipi = "sabah"
            else:
                mesaj_tipi = "oglen"
        else:
            # Menüden "sabah" veya "oglen" SEÇİLDİYSE saat fark etmeksizin onu zorlar
            mesaj_tipi = mesaj_turu_secimi

        # Yapay zeka öncesi yedek yazılar (API çökerse diye garanti mesajlar)
        if mesaj_tipi == "sabah":
            baslik = "Günaydın Sena! 🌸"
            icerik = "Mithat seni çok seviyor, bugün senin günün olsun! Unutma o tıp kesinlikle olacak. ✨" + ozel_imza
        else:
            baslik = "Sana bir şarkı bıraktım... 🎶"
            icerik = "Derslerine küçük bir mola ver ve derin bir nefes al. Erkin Koray, Cem Karaca ezgileriyle günün güzelleşsin. Çok emek ediyorsun ve Mithat hep senin yanında! 🐢✨" + ozel_imza

        # Groq (Yapay Zeka) Devrede
        if groq_api_key:
            try:
                groq_url = "https://api.groq.com/openai/v1/chat/completions"
                groq_headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
                anlik_zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if mesaj_tipi == "sabah":
                    system_prompt = "Sen bir ChatGPT'sin ve senin dilinden Mithat'ın kız arkadaşı Sena'ya özel, YKS sınavına hazırlanan kız arkadaşına moral verecek, samimi, pozitif, motive edici bir günaydın mesajı oluşturacaksın. Mesajda mutlaka 'Mithat seni çok seviyor' ve 'Bugün Sena ve Mithat'ın günü olsun!' ifadelerini ekle. Onun sakin kalmasını, stresten uzak durmasını hatırlat. Mithat'ın her an onun yanında olduğunu, bugüne kadar çok büyük ve takdir edilesi bir emek verdiğini, bu emeklerin karşılığında o tıp fakültesinin kesinlikle olacağını çok güçlü ve inançlı bir şekilde vurgula."
                    user_prompt = f"Sistem Saati: {anlik_zaman}. Sena'nın güne harika başlamasını sağlayacak, tıp hedefine olan inancını körükleyecek 3-4 cümlelik duygu dolu bir günaydın motivasyonu yaz."
                else:
                    system_prompt = "Sen bir ChatGPT'sin ve senin dilinden Mithat'ın kız arkadaşı Sena'ya özel, YKS sınavına hazırlanan kız arkadaşına gün ortasında ders arası için moral verecek samimi bir mola mesajı oluşturacaksın. Mesajın içinde mutlaka Erkin Koray, Cem Karaca veya Grup Gündoğarken (özellikle 'Sen Benim Şarkılarımsın' şarkısı) ezgilerinden, şarkı sözlerinden çok tatlı alıntılar, göndermeler yapacaksın. Mesajda mutlaka 'Mithat seni çok seviyor' ve 'Bugün Sena ve Mithat'ın günü olsun!' ifadelerini ekle. Sena'nın bu süreçte ne kadar çok emek ettiğini, döktüğü her damla alın terinin onu tıp fakültesine adım adım yaklaştırdığını ve Mithat'ın her saniye onun yanında, arkasında dev bir destek olduğunu hissettir."
                    user_prompt = f"Sistem Saati: {anlik_zaman}. Ders çalışırken yorulan Sena'ya gün ortasında ilaç gibi gelecek, nostaljik şarkı esintili ve yoğun tıp motivasyonlu harika bir mola mesajı yaz."

                groq_payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                    "temperature": 0.8,
                    "max_tokens": 250
                }

                response = requests.post(groq_url, headers=groq_headers, json=groq_payload)
                if response.status_code == 200:
                    ai_mesaj = response.json()['choices'][0]['message']['content'].strip()
                    ai_mesaj = ai_mesaj.replace("#ChatGPT Kankan#", "").strip()
                    icerik = ai_mesaj + ozel_imza
                    if mesaj_tipi == "sabah":
                        baslik = "Yeni bir mesajın var! 💌"
                    else:
                        baslik = "Sana bir şarkı bıraktım... 🎶"
            except Exception as e:
                print("Yapay zeka hatası:", e)

    # Önce JSON güncelleniyor (Sitenin güncel kalması için)
    with open("mesaj.json", "w", encoding="utf-8") as f:
        json.dump({"baslik": baslik, "icerik": icerik}, f, ensure_ascii=False, indent=4)
    
    # OneSignal Bildirimi Fırlatılıyor
    os_header = {"Content-Type": "application/json; charset=utf-8", "Authorization": f"Basic {onesignal_api_key}"}
    os_payload = {
        "app_id": "f66f725a-9c4b-4f45-8f5c-33118e634400",
        "included_segments": ["Total Subscriptions"], 
        "headings": {"en": baslik},
        "contents": {"en": icerik},
        "url": "https://senamithat.site/mesaj.html" 
    }
    
    requests.post("https://onesignal.com/api/v1/notifications", headers=os_header, data=json.dumps(os_payload))
    print(f"✅ İşlem başarıyla tamamlandı! Giden mesaj türü: {mesaj_tipi}")

surpriz_bildirim_gonder()
