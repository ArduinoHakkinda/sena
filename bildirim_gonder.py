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

        # Yapay zeka öncesi yedek yazılar (API çökerse diye yarınki sınava özel garanti mesajlar)
        if mesaj_tipi == "sabah":
            baslik = "Günaydın Sena! 🌸"
            icerik = "Günaydın! Yarınki sınavın çok iyi geçecek, çünkü sen zaten çok başarılısın ve yapabilirsin. Lütfen sakin kal, Mithat seni çok seviyor, her an yanında ve senin için bol bol dua ediyor. İnşallah o tıp olacak! ✨💖🩷🌸🫰🏻" + ozel_imza
        else:
            baslik = "Derin Bir Nefes Al... 🌸"
            icerik = "Yarınki sınav için hiç stres yapma, her şey harika olacak. Sen elinden geleni yaptın ve çok başarılısın. Mithat seni çok seviyor, her zaman arkanda ve duaları hep seninle! İnşallah tıp kazanacaksın! ✨💖🩷🌸🫰🏻" + ozel_imza

        # Groq (Yapay Zeka) Devrede
        if groq_api_key:
            try:
                groq_url = "https://api.groq.com/openai/v1/chat/completions"
                groq_headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
                anlik_zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if mesaj_tipi == "sabah":
                    system_prompt = "Sen bir ChatGPT'sin ve senin dilinden Mithat'ın kız arkadaşı Sena'ya özel, YARIN gireceği YKS sınavı için moral verecek, samimi ve pozitif bir günaydın mesajı oluşturacaksın. Mesajda mutlaka şu konuları vurgula: Yarınki sınavı çok iyi geçecek, inşallah o tıp fakültesini kazanacak, sakin olmalı çünkü o zaten çok başarılı ve bu işi yapabilir. Ayrıca 'Mithat seni çok seviyor', 'Mithat her an senin yanında' ve 'Mithat sana çok dua ediyor' ifadelerini kesinlikle ekle. Mesajı süslemek için sadece şu emojileri kullan: ✨💖🩷🌸🫰🏻"
                    user_prompt = f"Sistem Saati: {anlik_zaman}. Sena'nın YKS'den bir gün önceki sabahına harika başlamasını sağlayacak, yarınki sınavı için heyecanını yatıştırıp motivasyonunu zirveye çıkaracak, dualarla ve sevgiyle dolu 3-4 cümlelik bir günaydın mesajı yaz."
                else:
                    system_prompt = "Sen bir ChatGPT'sin ve senin dilinden Mithat'ın kız arkadaşı Sena'ya özel, YARIN gireceği YKS sınavı öncesi gün ortasında onu rahatlatacak harika bir motivasyon mesajı oluşturacaksın. Mesajın içinde mutlaka şu konular geçmeli: Sınavı kesinlikle çok iyi geçecek, sakin kalması gerekiyor, o zaten yapabileceğini kanıtlamış başarılı biri ve inşallah o tıp olacak. Ayrıca 'Mithat seni çok seviyor', 'Mithat her an senin yanında' ve 'Mithat senin için hep dua ediyor' ifadelerini kesinlikle barındır. Şirin ve samimi bir dil kullan, emojiler olarak yalnızca şunlara yer ver: ✨💖🩷🌸🫰🏻"
                    user_prompt = f"Sistem Saati: {anlik_zaman}. Yarınki büyük sınav öncesi gün ortasında Sena'nın kalbini ferahlatacak, inşallah tıp kazanacağına dair inancını tazeleyecek, Mithat'ın dualarını ve desteğini hissettiren şefkatli bir mesaj yaz."

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
                        baslik = "Sınav Öncesi Yeni Bir Mesajın Var! 💌"
                    else:
                        baslik = "Derin Bir Nefes Al... 🌸"
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
