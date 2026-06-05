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
    
Veri seti: projeyle ilgili dökümanlar, teknik şartname, proje takvimi, proje sözleşmesi ve      ekleri, literatür taraması, yazılım gereksinim özellikleri dökümanı, yazılım tasarım tanımı, yazılım test tanımı, fabrika kabul testleri, müşteri kabul testleri ...

araçlar ve teknolojiler: gemini 2.5 flash, rich (terminalde renkli çıktı)

plan/program:
    1. proje dökümanı oluşturma ve sonrasında pdf reader
    2. gemini agent:
        1. taskların sorulması
        2. taskların tamamlanıp tamamlanmadığının anlaşılması
    3. simülasyon ile parçaların birleştirilmesi

pip install google-generativeai python-dotenv rich PyPDF2
"""