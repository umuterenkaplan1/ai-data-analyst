import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google import genai

st.set_page_config(page_title="AI Veri Analisti", page_icon="📊", layout="wide")
st.title("📊 AI Destekli Akıllı Veri Analisti")
st.write("CSV veya Excel dosyanızı yükleyin, verilerinizle sohbet ederek anında analiz ve grafikler oluşturun.")

# Yan menü ayarları
api_key = st.sidebar.text_input("Google Gemini API Anahtarınız:", type="password")
st.sidebar.markdown("[Ücretsiz API Anahtarı Al](https://google.com)")

uploaded_file = st.file_uploader("Veri Setinizi Yükleyin (CSV veya XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    # Dosyayı Pandas DataFrame olarak okuma
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Veri Önizlemesi (İlk 5 Satır)")
    st.dataframe(df.head())

    user_question = st.text_input("Veriniz hakkında ne öğrenmek istersiniz? (Örn: Şehirlere göre toplam tutarı hesapla ve bar grafiği çiz)")

    if st.button("Analiz Et ve Çalıştır"):
        if not api_key:
            st.warning("Lütfen sol menüden Gemini API anahtarınızı girin.")
        elif not user_question:
            st.warning("Lütfen bir soru yazın.")
        else:
            try:
                with st.spinner("Yapay zeka Python kodunu yazıyor ve çalıştırıyor..."):
                    client = genai.Client(api_key=api_key)
                    
                    columns_info = str(df.dtypes.to_dict())
                    sample_data = str(df.head(3).to_dict())

                    prompt = f"""
                    Sen uzman bir Python Veri Bilimcisisin. Elimde 'df' adında bir pandas DataFrame var.
                    Sütunlar ve veri tipleri: {columns_info}
                    Örnek veri: {sample_data}

                    Kullanıcının sorusu: "{user_question}"

                    Bana SADECE çalıştırılabilir saf Python kodu ver (markdown ```python etiketleri olmadan).
                    Kurallar:
                    1. Sonucu mutlaka 'result' adlı bir değişkene ata (metin, sayı veya tablo olabilir).
                    2. Eğer kullanıcı grafik isterse matplotlib.pyplot (plt) kullan, figürü oluştur ve 'fig = plt.gcf()' değişkenine ata. Grafik yoksa 'fig = None' yap.
                    3. Kodun içinde 'df' zaten tanımlı, tekrar dosya okuma.
                    """

                    # Resmi güncel hızlı modeller (Önce en hızlısı, yoğunlukta ana model)
                    models_to_try = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
                    response = None
                    used_model = ""
                    last_error = None

                    for model_name in models_to_try:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                            )
                            used_model = model_name
                            break
                        except Exception as model_err:
                            last_error = model_err
                            continue

                    if response is None:
                        st.error(f"Modellerden yanıt alınamadı. Son hata: {last_error}")
                    else:
                        generated_code = response.text.replace("```python", "").replace("```", "").strip()
                        
                        local_vars = {"df": df, "pd": pd, "plt": plt, "result": None, "fig": None}
                        exec(generated_code, {}, local_vars)

                        st.success(f"Analiz Sonucu (Kullanılan Model: {used_model}):")
                        if local_vars["result"] is not None:
                            st.write(local_vars["result"])
                        
                        if local_vars["fig"] is not None:
                            st.pyplot(local_vars["fig"])

                        with st.expander("Arka Planda Üretilen Python Kodunu Gör"):
                            st.code(generated_code, language="python")

            except Exception as e:
                st.error(f"Kod çalıştırılırken bir hata oluştu: {e}")
