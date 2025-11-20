# 1. Base Image olarak Python 3.10 slim versiyonunu kullanıyoruz
# (Slim versiyonlar daha az yer kaplar ve daha güvenlidir)
FROM python:3.12-slim

# 2. Container içindeki çalışma dizinini ayarlıyoruz
WORKDIR /app

# 3. Önce sadece requirements dosyasını kopyalıyoruz
# (Bu, Docker'ın önbellekleme (caching) mekanizmasını verimli kullanmasını sağlar)
COPY requirements.txt .

# 4. Bağımlılıkları yüklüyoruz
# (--no-cache-dir ile imaj boyutunu şişirmemeyi hedefliyoruz)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kalan tüm proje dosyalarını (app.py ve models klasörü dahil) kopyalıyoruz
COPY . .

# 6. Streamlit'in kullandığı 8501 portunu dış dünyaya açıyoruz
EXPOSE 8501

# 7. Container başlatıldığında çalışacak komut
# (address=0.0.0.0 komutu Docker içinde çalışması için kritiktir)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]