import streamlit as st
import pandas as pd
import joblib
import os
import requests
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="AI Sigorta Asistanı",
    page_icon="🤖",
    layout="wide"
)


def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_health = load_lottieurl("https://lottie.host/4e323352-2528-4749-8937-376b730c538c/1J2o6l7k3q.json")
lottie_money = load_lottieurl("https://lottie.host/9625743e-8c77-4e72-946e-343776d54e55/sS4sFjF9vP.json")

# CSS Tasarımı

st.markdown("""
<style>
    
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stButton>button {
        background-image: linear-gradient(to right, #00c6ff 0%, #0072ff  51%, #00c6ff  100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        text-transform: uppercase;
        text-align: center;
        transition: 0.5s;
        background-size: 200% auto;
        box-shadow: 0 0 20px #eee;
        display: block;
        width: 100%;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-position: right center;
        color: #fff;
        text-decoration: none;
    }
    
    .result-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: #333;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Model Yükleme
@st.cache_resource
def load_model():
    current_dir = os.getcwd()
    model_path = os.path.join(current_dir, 'models', 'insurance_model_pipeline.joblib')
    if not os.path.exists(model_path):
        return None
    try:
        return joblib.load(model_path)
    except:
        return None

def calculate_bmi_status(bmi_value):
    if bmi_value < 18.5: return "Zayıf", "#3498db"
    elif 18.5 <= bmi_value < 24.9: return "Normal", "#2ecc71"
    elif 25 <= bmi_value < 29.9: return "Fazla Kilolu", "#f39c12"
    else: return "Obez", "#e74c3c"


def main():
    
    
    col_left, col_center, col_right = st.columns([1, 6, 1])
    
    with col_center:
        c_head1, c_head2 = st.columns([1, 4])
        with c_head1:
             if lottie_health:
                st_lottie(lottie_health, height=120, key="health")
        with c_head2:
            st.title("Geleceğinizi Güvenceye Alın")
            st.markdown("### 🤖 Yapay Zeka Destekli Sigorta Asistanı")

    pipeline = load_model()
    if pipeline is None:
        st.error("Model dosyası yüklenemedi.")
        return

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("👤 Kişisel")
            age = st.number_input("Yaş", 18, 100, 25)
            sex = st.selectbox("Cinsiyet", ['female', 'male'], format_func=lambda x: "Kadın" if x == 'female' else "Erkek")
            
        with col2:
            st.subheader("⚖️ Fiziksel")
            bmi_method = st.radio("Giriş Yöntemi:", ["Otomatik", "Manuel"], horizontal=True, label_visibility="collapsed")
            
            if bmi_method == "Otomatik":
                col_h, col_w = st.columns(2)
                with col_w: weight = st.number_input("Kilo (kg)", 30.0, 200.0, 70.0)
                with col_h: height = st.number_input("Boy (cm)", 100, 250, 175)
                
                bmi = weight / ((height / 100) ** 2)
                status, color = calculate_bmi_status(bmi)
                st.markdown(f"<div style='background-color:{color}; color:white; padding:8px; border-radius:5px; text-align:center; font-weight:bold;'>BMI: {bmi:.1f} ({status})</div>", unsafe_allow_html=True)
            else:
                bmi = st.number_input("BMI Değeri", 10.0, 60.0, 22.5)

        with col3:
            st.subheader("📋 Yaşam Tarzı")
            children = st.slider("Çocuk Sayısı", 0, 5, 0)
            smoker = st.selectbox("Sigara Kullanımı", ['yes', 'no'], format_func=lambda x: "🚬 Evet" if x == 'yes' else "🚭 Hayır")
            region = st.selectbox("Bölge", ['southwest', 'southeast', 'northwest', 'northeast'])

    st.write("") 
    _, col_btn, _ = st.columns([1, 1, 1]) 
    
    predict_clicked = False
    with col_btn:
        predict_clicked = st.button("🚀 MALİYETİ HESAPLA")

    if predict_clicked:
        input_data = pd.DataFrame({
            'age': [age], 'sex': [sex], 'bmi': [bmi],
            'children': [children], 'smoker': [smoker], 'region': [region]
        })

        with st.spinner('Analiz ediliyor...'):
            try:
                prediction = pipeline.predict(input_data)[0]
                
                st.markdown("---")
                
                left_col, middle_col, right_col = st.columns([1, 2, 1])
                
                with middle_col:
                 
                    res_anim, res_text = st.columns([1, 2])
                    
                    with res_anim:
                        if lottie_money:
                            st_lottie(lottie_money, height=150, key="money_anim")
                    
                    with res_text:
                        st.markdown(f"""
                        <div class="result-card">
                            <h4 style="margin:0;">Yıllık Tahmini Maliyet</h4>
                            <h1 style="color: #28a745; font-size: 42px; margin: 10px 0;">${prediction:,.2f}</h1>
                            <p style="font-size:12px; color:gray;">*Tahmini değerdir.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.balloons()

            except Exception as e:
                st.error(f"Hata: {e}")

if __name__ == "__main__":
    main()