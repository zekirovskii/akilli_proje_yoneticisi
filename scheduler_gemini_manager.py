"""
Problem Tanımı: 
    - Bir proje dökümanını okuyarak ekip üyelerine gerçek zamanlı olarak görev hatırlatmaları yapan bir yapay zeka sistemi olacak
    - Yapay zeka yöneticisi:
        1. Bir proje planı oluştur (ne yapacağımız, takvim, ekip) ve yapay zeka yöneticisine ver
        2. dosyada/dosyalarda bulunan görev zamanına göre ai yöneticimiz ekip üyelerine görevleri/taskları sorar
            - örn: ui işi ne oldu, bugün bitirmen gerekiyordu
        3. Çalışan doğal dilde cevap verir ve ai yöneticisi bunu analiz eder
            - örn: yaptım ama biraz daha zamana ihtiyacım var
        4. Eğer görev tamamlandıysa devam, yoksa bir daha sorar
        5. Tüm sorular ai yönetici tarafından ekip üyelerinin geçmiş cevaplarına göre kişiselleştirilerek tekrar sorulur veya yeni soru sorulur
    - Simülasyon ortamı: 10 saniyede 1 dk ilerleyen bir sümülasyon saati
        örn: 
            kaan: 12.01 saat --> ui design
            kaan: 12.02 saat --> ui test
    
Veri seti: projeyle ilgili dökümanlar, teknik şartname, proje takvimi, proje sözleşmesi ve      ekleri, literatür taraması, yazılım gereksinim özellikleri dökümanı, yazılım tasarım tanımı, yazılım test tanımı, fabrika kabul testleri, müşteri kabul testleri, kullanıcı el kitabı 

araçlar ve teknolojiler: gemini 2.5 flash, rich (terminalde renkli çıktı)

plan/program:
    1. proje dökümanı oluşturma ve sonrasında pdf reader
    2. gemini agent:
        1. taskların sorulması
        2. taskların tamamlanıp tamamlanmadığının anlaşılması
    3. simülasyon ile parçaların birleştirilmesi

pip install google-generativeai python-dotenv rich PyPDF2
"""

import time 
from datetime import datetime, timedelta
from pdf_reader import extract_tasks_from_pdf
from rich import print # renkli terminal cıktısı
from gemini_agent import generate_foolowup_question, is_task_completed

task_memory = {} # taskların hepsini hafızaya atalım

def normalize_status(status):
    return (
        status.strip()
        .lower()
        .replace("ı", "i")
        .replace("ğ", "g")
        .replace("ü", "u")
        .replace("ş", "s")
        .replace("ö", "o")
        .replace("ç", "c")
    )

def run_scheduler(pdf_path="proje_dokumani.pdf",delay_sec=10):

    # belirtilen pdf dosyasından görevleri cıkart
    tasks = extract_tasks_from_pdf(pdf_path)

    sim_time = datetime(2025, 8, 25, 11, 59)

    print(f"[bold green] Simülasyon başladı [/bold green] -> Başlangıç: {sim_time.strftime("%d.%m.%Y %H:%M")}")

    while True: # 1dk yi 10 saniyede ilerletir
        sim_time += timedelta(minutes=1)
        sim_time_str = sim_time.strftime("%d.%m.%Y %H:%M")
        print(f"\n[bold white on black]Simülasyon Saati: {sim_time_str}[/bold white on black]")

        # her görev için kontrol yapılır
        for task in tasks:

            ts = task["timestamp"]
            kisi = task["person"]
            gorev = task["task"]
            key = f"{ts}_{kisi}" # uniq anahtar

            if ts <= sim_time:
                # daha önce verilen cevapları bellekten alalım
                onceki_cevaplar = task_memory.get(key, [])

                if onceki_cevaplar: # önceki cevap varsa tamamlanma durumunu sorgular
                    tamam_durum = is_task_completed(kisi, gorev, onceki_cevaplar, sim_time_str)

                    if normalize_status(tamam_durum) == "tamamlandi":
                        continue
                    else:
                        print(f"[yellow]{kisi} gorevini henuz tamamlamadi. Tekrar soruluyor ... [/yellow]")
                
                # gemini ile soru sorma
                soru = generate_foolowup_question(
                    person = kisi,
                    task = gorev,
                    current_time=sim_time_str,
                    previous_responses=onceki_cevaplar
                )

                print(f"[bold red]{kisi}[/bold red] kişisine AI yöneticisi tarafından olışturulan soru: ")
                print(f"[bold blue]{soru}[/bold blue]")

                cevap = input("Cevap: ").strip()

                task_memory.setdefault(key, []).append({
                    "time": sim_time.strftime("%H:%M"),
                    "response": cevap
                })

        time.sleep(delay_sec)

if __name__ == "__main__":
    run_scheduler()
