import streamlit as st
from datetime import datetime, date
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(
    page_title="Mehmet Ali Turan | KPSS 2026 Koçluk Paneli",
    page_icon="🎯",
    layout="wide"
)

# Özel CSS Tasarımı
st.markdown("""
    <style>
    .main { background-color: #050505; color: #e5e5e5; }
    .stApp { background-color: #050505; }
    .metric-card { background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); padding: 20px; border-radius: 20px; text-align: center; }
    .timer-box { font-size: 48px; font-weight: 900; color: #e11d48; text-align: center; background: rgba(225, 29, 72, 0.05); border: 2px solid rgba(225, 29, 72, 0.2); padding: 20px; border-radius: 20px; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# Oturum Hafızası
if 'soru_gecmisi' not in st.session_state:
    st.session_state.soru_gecmisi = []

if 'gunluk_aktiviteler' not in st.session_state:
    st.session_state.gunluk_aktiviteler = {}

if 'zincir_gun' not in st.session_state:
    st.session_state.zincir_gun = 1

# Sınav Tarihi: 25 Ekim 2026
sinav_tarihi = date(2026, 10, 25)
bugun = date.today()
kalan_gun = (sinav_tarihi - bugun).days

# Haftalık Ders Programı Dağılımı (Pazartesi - Cuma)
haftalik_program = {
    "Monday": ("Türkçe", "Tarih"),
    "Tuesday": ("Matematik", "Coğrafya"),
    "Wednesday": ("Türkçe", "Vatandaşlık"),
    "Thursday": ("Matematik", "Tarih"),
    "Friday": ("Coğrafya", "Vatandaşlık"),
    "Saturday": ("Dinlenme / Genel Tekrar", "Deneme Sınavı"),
    "Sunday": ("Dinlenme / Serbest Çalışma", "Eksik Kapatma")
}

bugun_isim = bugun.strftime("%A")
ders1, ders2 = haftalik_program.get(bugun_isim, ("Özel Ders", "Özel Ders"))

# Üst Bilgi & Sayaçlar
st.title("🎯 Mehmet Ali Turan | KPSS 2026 Kişisel Koçluk Paneli")
st.markdown("> *Canım istemese bile masaya oturacağım. Çünkü başarı motivasyonla değil, disiplinle gelir.* 🧠")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="🔥 Sınava Kalan Gün (25 Ekim)", value=f"{kalan_gun} Gün")
with col2:
    toplam_cozulen = sum([item['Toplam'] for item in st.session_state.soru_gecmisi]) if st.session_state.soru_gecmisi else 0
    st.metric(label="📚 Toplam Çözülen Soru", value=f"{toplam_cozulen} Soru")
with col3:
    st.metric(label="⭐ Günlük Zincir", value=f"{st.session_state.zincir_gun}. Gün")
with col4:
    st.metric(label="🎯 Bugünün Dersleri", value=f"{ders1} & {ders2}")

st.divider()

# Sekmeler
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📅 Günlük Program", 
    "🗓️ Haftalık Ders Programı",
    "📊 Soru & Net Takibi", 
    "👤 Profil & Geçmiş Raporu",
    "🔥 75 Günlük Zincir", 
    "🍅 Pomodoro Sayaç", 
    "🧠 Motivasyon"
])

with tab1:
    st.subheader(f"⏰ Günlük Ders Akışı ({bugun_isim} - Bugünün Dersleri: {ders1} & {ders2})")
    st.info("Bugün ne çalışacağını düşünmeyeceksin. Programın aşağıda hazır, tik attıkça profiline işlenecek.")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(f"### 📝 Bugünün Planı")
        t1 = st.checkbox(f"12.30 - {ders1} 1. Konu Videosu + Soru Çözümü", key="v1")
        t2 = st.checkbox(f"14.00 - 20 dk Mola", key="m1")
        t3 = st.checkbox(f"14.20 - {ders2} 1. Konu Videosu + Soru Çözümü", key="v2")
        t4 = st.checkbox(f"15.50 - 20 dk Mola", key="m2")
        t5 = st.checkbox(f"16.10 - 20 Paragraf Çözümü", key="para")
        t6 = st.checkbox(f"17.00 - Günlük Genel Tekrar", key="genel_tekrar")
        
        if st.button("💾 Bugünkü Çalışmaları Kaydet ve Profile İşle"):
            yapilanlar = []
            if t1: yapilanlar.append(f"{ders1} Çalışması")
            if t2: yapilanlar.append("1. Mola")
            if t3: yapilanlar.append(f"{ders2} Çalışması")
            if t4: yapilanlar.append("2. Mola")
            if t5: yapilanlar.append("20 Paragraf")
            if t6: yapilanlar.append("Günlük Genel Tekrar")
            
            st.session_state.gunluk_aktiviteler[str(bugun)] = yapilanlar
            st.success("✅ Bugünkü program verilerin profile başarıyla işlendi!")

    with col_r:
        st.markdown("### 🛑 Günlük Kurallar")
        st.success("✅ Ders arasında Instagram yok.")
        st.success("✅ TikTok sadece molalarda.")
        st.warning("⚠️ Bildirimler tamamen kapalı!")
        st.info("💡 Telefonu sadece mola sürelerinde eline al.")

with tab2:
    st.subheader("🗓️ Haftalık Ders Programı Genel Tablosu")
    hafta_data = [
        {"Gün": "Pazartesi", "1. Ders": "Türkçe", "2. Ders": "Tarih", "Rutin": "20 Paragraf + Genel Tekrar"},
        {"Gün": "Salı", "1. Ders": "Matematik", "2. Ders": "Coğrafya", "Rutin": "20 Paragraf + Genel Tekrar"},
        {"Gün": "Çarşamba", "1. Ders": "Türkçe", "2. Ders": "Vatandaşlık", "Rutin": "20 Paragraf + Genel Tekrar"},
        {"Gün": "Perşembe", "1. Ders": "Matematik", "2. Ders": "Tarih", "Rutin": "20 Paragraf + Genel Tekrar"},
        {"Gün": "Cuma", "1. Ders": "Coğrafya", "2. Ders": "Vatandaşlık", "Rutin": "20 Paragraf + Genel Tekrar"},
        {"Gün": "Cumartesi", "1. Ders": "Dinlenme / Genel Tekrar", "2. Ders": "Deneme Sınavı", "Rutin": "Serbest Analiz"},
        {"Gün": "Pazar", "1. Ders": "Dinlenme", "2. Ders": "Eksik Kapatma", "Rutin": "Haftalık Değerlendirme"}
    ]
    st.table(pd.DataFrame(hafta_data))

with tab3:
    st.subheader("📊 Ders Bazlı Soru, Doğru, Yanlış ve Net Takibi")
    st.write("Doğru ve yanlış sayılarını girdiğinde netlerin anında kusursuz hesaplanacaktır.")

    dersler_liste = ["Matematik", "Türkçe", "Coğrafya", "Tarih", "Vatandaşlık"]
    girilen_veriler = {}
    
    col_d1, col_d2 = st.columns(2)
    for i, d_adi in enumerate(dersler_liste):
        target_col = col_d1 if i < 3 else col_d2
        with target_col:
            st.markdown(f"**📚 {d_adi}**")
            d = st.number_input(f"{d_adi} Doğru", min_value=0, max_value=200, key=f"{d_adi}_d", step=1)
            y = st.number_input(f"{d_adi} Yanlış", min_value=0, max_value=200, key=f"{d_adi}_y", step=1)
            
            net = float(d) - (float(y) * 0.25)
            st.markdown(f"👉 **Net: {net:.2f}**")
            girilen_veriler[d_adi] = {"Doğru": int(d), "Yanlış": int(y), "Net": net, "Toplam": int(d) + int(y)}
            st.markdown("---")
    
    if st.button("🚀 Bugünkü Soru Sonuçlarını Kaydet", type="primary"):
        toplam_gunluk_soru = sum([v["Toplam"] for v in girilen_veriler.values()])
        st.session_state.soru_gecmisi.append({"Tarih": str(bugun), "Veri": girilen_veriler, "Toplam": toplam_gunluk_soru})
        st.success("✅ Bugünkü soruların kaydedildi ve profiline işlendi!")

with tab4:
    st.subheader("👤 Profil & Tüm Zamanların Gelişim Raporu")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("### 📈 Genel İstatistiklerin")
        toplam_yanlis = 0
        toplam_dogru = 0
        if st.session_state.soru_gecmisi:
            for kayit in st.session_state.soru_gecmisi:
                for d_adi, detay in kayit["Veri"].items():
                    toplam_dogru += detay["Doğru"]
                    toplam_yanlis += detay["Yanlış"]
        
        st.info(f"📚 **Toplam Çözülen Soru:** {toplam_cozulen}")
        st.success(f"✅ **Toplam Doğru:** {toplam_dogru}")
        st.warning(f"❌ **Toplam Yanlış:** {toplam_yanlis}")
        
    with col_p2:
        st.markdown("### 📅 Günlük Tamamlanan Programlar")
        if st.session_state.gunluk_aktiviteler:
            for tarih, gorevler in st.session_state.gunluk_aktiviteler.items():
                st.write(f"**Tarih: {tarih}**")
                if gorevler:
                    st.write("✔ " + ", ".join(gorevler))
                else:
                    st.write("Görev işaretlenmemiş.")
                st.markdown("---")
        else:
            st.write("Henüz kaydedilmiş günlük program aktiviten yok.")

    if st.session_state.soru_gecmisi:
        st.markdown("### 📊 Soru ve Net Detay Tablosu")
        tablo_listesi = []
        for kayit in st.session_state.soru_gecmisi:
            tarih = kayit["Tarih"]
            for d_adi, detay in kayit["Veri"].items():
                tablo_listesi.append({
                    "Tarih": tarih, 
                    "Ders": d_adi, 
                    "Doğru": detay["Doğru"], 
                    "Yanlış": detay["Yanlış"], 
                    "Net": round(detay["Net"], 2), 
                    "Toplam Soru": detay["Toplam"]
                })
        st.dataframe(pd.DataFrame(tablo_listesi), use_container_width=True)

with tab5:
    st.subheader("🔥 75 Günlük Zinciri Kırma Takvimi")
    col_z1, col_z2 = st.columns([2, 1])
    with col_z1:
        st.markdown(f"**Şu anki zincir durumun: {st.session_state.zincir_gun}. Gün**")
        kutular_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px;'>"
        for g in range(1, 76):
            if g <= st.session_state.zincir_gun:
                kutular_html += f"<div style='width: 35px; height: 35px; background: #e11d48; color: white; display: flex; align-items: center; justify-content: center; border-radius: 6px; font-weight: bold; font-size: 12px;'>{g}</div>"
            else:
                kutular_html += f"<div style='width: 35px; height: 35px; background: #1f2937; color: #9ca3af; display: flex; align-items: center; justify-content: center; border-radius: 6px; font-weight: bold; font-size: 12px;'>{g}</div>"
        kutular_html += "</div>"
        st.markdown(kutular_html, unsafe_allow_html=True)
    
    with col_z2:
        st.markdown("### ⚙️ Zincir Yönetimi")
        if st.button("🔥 Bugün Çalıştım, Zinciri İlerlet"):
            if st.session_state.zincir_gun < 75:
                st.session_state.zincir_gun += 1
                st.success("Tebrikler! Zincire yeni bir halka eklendi.")
                st.rerun()
            else:
                st.balloons()
                st.success("Mükemmel! 75 günlük zinciri tamamladın!")

with tab6:
    st.subheader("🍅 Çalışan Geri Sayımlı Pomodoro Sayaç")
    
    dakika = st.slider("Çalışma Süresi (Dakika)", min_value=1, max_value=60, value=25)
    
    if 'zaman' not in st.session_state:
        st.session_state.zaman =ika * 60 if 'zaman' not in st.session_state else st.session_state.zaman

    col_b, col_s = st.columns(2)
    with col_b:
        baslat_p = st.button("▶️ Geri Sayımı Başlat")
    with col_s:
        sifirla_p = st.button("🔄 Süreyi Sıfırla")

    if sifirla_p:
        st.session_state.zaman = dakika * 60

    if baslat_p:
        placeholder = st.empty()
        toplam_saniye = dakika * 60
        for s in range(toplam_saniye, -1, -1):
            m = s // 60
            sn = s % 60
            placeholder.markdown(f'<div class="timer-box">⏳ {m:02d}:{sn:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
        st.balloons()
        st.success("🎉 Tebrikler! Odak seansı başarıyla tamamlandı, mola verme vakti!")

with tab7:
    st.subheader("🧠 Günün Motivasyon Sözü")
    st.info("“Canım istemese bile masaya oturacağım. Çünkü başarı motivasyonla değil, disiplinle gelir.”")