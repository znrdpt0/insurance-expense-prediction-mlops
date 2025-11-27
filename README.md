# 🏥 Insurance Cost Prediction | End-to-End MLOps Project

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)

## 📖 Proje Özeti (Executive Summary)

Bu proje, makine öğrenmesi modellerini (Machine Learning) sadece geliştirmekle kalmayıp, bu modelleri **üretim ortamına (Production)** taşımak, ölçeklenebilir hale getirmek ve sürdürülebilir bir **CI/CD (Sürekli Entegrasyon/Dağıtım)** hattı kurmak amacıyla geliştirilmiştir.

**Temel Problem:** Sigorta şirketleri için müşteri risk analizini ve poliçe maliyet tahminlerini manuel hesaplamak yavaş ve hataya açıktır.
**Çözüm:** Kullanıcının demografik verilerine (yaş, cinsiyet, VKİ, sigara kullanımı vb.) dayanarak saniyeler içinde sigorta maliyetini tahmin eden, Dockerize edilmiş ve tam otomatik bir MLOps mimarisine sahip web uygulaması.

---

## 🏗️ Mimari ve Teknoloji Yığını (Architecture & Tech Stack)

Proje, modern MLOps prensiplerine uygun olarak **mikroservis mimarisine** benzer, izole bir yapıda geliştirilmiştir.

```mermaid
graph LR
    User[Kullanıcı] -- Web Tarayıcısı --> Streamlit[Streamlit Web Arayüzü]
    Streamlit -- Girdi Verisi --> Model["ML Model (Scikit-Learn)"]
    Model -- Tahmin Sonucu --> Streamlit
    
    subgraph MLOps Pipeline
    Code[Kod Push] --> Actions[GitHub Actions CI]
    Actions -- "Linting & Test" --> Build[Docker Buildx]
    Build -- "Multi-Platform Image" --> DockerHub[Docker Hub Registry]
    end