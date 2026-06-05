import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model tanımı
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_foolowup_question(person, task, current_time, previous_responses = None):
    """
    Gemini kişi, görev, zaman ve geçmiş yanıtları alarak en uygun soruyu üretir

    person: ekip üyesi örn: can
    task: 
    current_time: 
    previous_responces: kişinin göreve daha önce verdiği yanıtlar
    """

    history = ""
    if previous_responses:
        for item in previous_responses:
            history += f"Saat {item["time"]}: {item["responce"]}\n" # 2025-08-25 12:04:00 : "merhaba yaptım ya da yapmadım"

    # gemini prompt

    prompt = f"""
                Şu anda saat {current_time}.
                Sen bir proje yöneticisisin.

                Görev : {task}
                Kişi : {person}

                Bu kişiye bu görev daha önce verildi.
                Şimdiye kadar verdiği cevaplar:
                {history if history else "Henüz cevap yok."}

                Lütfen {person}'a doğrudan hitap ederek görevle ilgili ne durumda olduğunu soran net ve kısa bir soru yaz.

                Soru şunları içermeli:
                - Kişinin ismi ile hitap et
                - Görevin ne olduğu açıkça tekrar geçsin
                - Görevin tamamlanma durumu ya da üzerinden çalışılıp çalışılmadığı sorgulansın
                - Sadece doğrudan bir soru cümlesi döndür, başka açıklama yazma

    """

    response = model.generate_content(prompt, generation_config={"temperature": 0.7})
    return response.text.strip()

def is_task_completed(person, task, responces, current_time): # cevaba göre taskların kararını verir ok mu nok mu
    """
    AI yöneticimiz görevin tamamlanıp tamamlanmadığını anlar
    yalnızca 3 cevaptan birini return eder, tamamlandı / devam ediyor / yapılmadı
    """

    history = ""

    for item in responces:
        history += f"Saat: {item["time"]}: {item["responce"]}\n"

    
    prompt = f"""
            Saat : {current_time}
            Kişi : {person}
            Görev: {task}

            Bu görevle ilgili şimdiye kadar {person} tarafından verilen cevaplar:
            {history}

            Lütfen sadece tek bir kelime ile cevap ver:
            - tamamlandı
            - devam ediyor
            - yapılmadı

            Yalnızca bu üç kelimeden birini döndür. Açıklama yapma.
    
    """

    responce = model.generate_content(prompt, generation_config= {"temperature":0})
    return responce.text.strip().lower()


if __name__ == "__main__":

    example_history = [
        {"time": "12.02" , "responce":"Başladım ama eksik bir şeyler var."},
        {"time": "12.04" , "responce":"Veritabanı bağlantısını henüz kurmadım."},
        {"time": "12.06" , "responce":"Tüm taskları temizledim."},
    ]

    soru = generate_foolowup_question(
        person="Yusuf",
        task = "İkon setlerini belirle ve renk paletini uygula.",
        current_time= "25.08.2025 12.08",
        previous_responses=example_history
    )

    print(f"AI Proje yöneticisinin sorusu: {soru}")
    
    durum = is_task_completed(
        person= "Yusuf",
        task="İkon setlerini belirle ve renk paletini uygula.",
        responces=[{"time":"12.02","responce":"verilen görev uzundu hala bitmedi"}],
        current_time="25.08.2025 12:04"
    )
    print(f"AI Proje yöneticisi durum değerlendirmesi. Task: {durum}")
