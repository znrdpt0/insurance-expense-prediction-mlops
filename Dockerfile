
FROM python:3.12-slim


WORKDIR /app


COPY requirements.txt .


# (--no-cache-dir ile imaj boyutunu şişirmemeyi hedefliyoruz)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit'in kullandığı 8501 portunu dış dünyaya açıyoruz
EXPOSE 8501

# 7. Container başlatıldığında çalışacak komut

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]