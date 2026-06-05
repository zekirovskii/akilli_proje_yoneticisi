from PyPDF2 import PdfReader
import re # regular expression ile metin içerisinden desen arama
from datetime import datetime

# pdf içerisinden görevleri çıkartan fonk
def extract_tasks_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() for page in reader.pages)

    # print(text)

    # örnek desen: 25.08.2025 12:09 - Yusuf, Can, Samet - Hızlı bir smoke test yap 

    pattern = r"(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})\s*-\s*(.*?)\s*-\s*(.*)"
    matches = re.findall(pattern, text)

    # print(matches)
    """
    ('25.08.2025 12:00', 'Yusuf', 'Ana ekran ve butonlar için UI taslağını oluştur.  '), 
    ('25.08.2025 12:01', 'Can', 'UI taslağına uygun temel component yapısını kur.  ')
    """

    tasks = []
    for match in matches:
        tarih_str, kisi, gorev = match # match 3 parcaya ayrılıyor
        tarih = datetime.strptime(tarih_str, "%d.%m.%Y %H:%M")
        tasks.append({
            "timestamp": tarih,
            "person": kisi.strip(),
            "task": gorev.strip()
        })

    return tasks
     

if __name__ == "__main__":
    path = "proje_dokumani.pdf"

    try:
        tasks = extract_tasks_from_pdf(path)
        for task in tasks:
            print(f"{task["timestamp"]} -- {task["person"]}: {task["task"]}")
    except FileNotFoundError:
        print(f"{path} dosyası bulunamadı.")