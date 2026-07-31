import streamlit as st
from datetime import datetime, date
import pandas as pd
import time
from supabase import create_client, Client

# Sayfa Ayarları
st.set_page_config(
    page_title="Mehmet Ali Turan | KPSS 2026 Koçluk Paneli",
    page_icon="🎯",
    layout="wide"
)

# Supabase Bağlantısı
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Supabase bağlantısı kurulamadı. Lütfen Secrets ayarlarınızı kontrol edin.")

# Özel CSS Tasarımı
st.markdown("""
    <style>
    .main { background-color: #050505; color: #e5e5e5; }
    .stApp { background-color: #050505; }
    .metric-card { background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); padding: 20px; border-radius: 20px; text-align: center; }
    .timer-box { font-size: 48px; font-weight: 900; color: #e11d48; text-align: center; background: rgba(225, 29, 72, 0.05); border: 2px solid rgba(225, 29, 72, 0.2); padding: 20px; border-radius: 20px; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# Veritabanından Verileri Çekme Fonksiyonları
def veri_getir_sorular():
    try:
        res = supabase.table("kpss_soru_gecmisi").select("*").execute()
        return res.data if res.data else []
    except:
        return []

def veri_getir_konular():
    try:
        res = supabase.table("kpss_biten_konular").select("*").execute()
        return res.data if res.data else []
    except:
        return []

def veri_getir_zincir():
    try:
        res = supabase.table("kpss_zincir").select("zincir_gun").eq("id", 1).execute()
        return res.data[0]["zincir_gun"] if res.data else 1
    except:
        return 1

# Sınav Tarihi: 25 Ekim 2026
sinav_tarihi = date(2026, 10, 25)
bugun = date.today()
kalan_gun = (sinav_tarihi - bugun).days

# Veritabanı Verileri
soru_gecmisi = veri_getir_sorular()
biten_konular = veri_getir_konular()
zincir_gun = veri_getir_zincir()

# Haftalık Ders Programı Dağılımı
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

toplam_cozulen_soru = sum([item["toplam"] for item in soru_gecmisi]) if soru_gecmisi else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="🔥 Sınava Kalan Gün (25 Ekim)", value=f"{kalan_gun} Gün")
with col2:
    st.metric(label="📚 Toplam Çözülen Soru", value=f"{toplam_cozulen_soru} Soru")
with col3:
    st.metric(label="⭐ Günlük Zincir", value=f"{zincir_gun}. Gün")
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
    st.info("💡 Geçmiş bir günün programını girmeyi unuttuysan, aşağıdaki takvimden tarihi değiştirerek o günün verilerini kaydedebilirsin.")
    secilen_tarih = st.date_input("📅 İşlem Yapılacak Tarihi Seçin:", value=bugun)
    secilen_gun_isim = secilen_tarih.strftime("%A")
    sec_ders1, sec_ders2 = haftalik_program.get(secilen_gun_isim, ("Özel Ders", "Özel Ders"))

    st.subheader(f"⏰ Günlük Ders Akışı ve Konu Girişi ({secilen_tarih.strftime('%d.%m.%Y')} - Dersler: {sec_ders1} & {sec_ders2})")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(f"### 📝 {secilen_tarih.strftime('%d.%m.%Y')} Planı ve Konu Notları")
        t1 = st.checkbox(f"12.30 - {sec_ders1} Konu Videosu + Soru Çözümü", key=f"v1_{secilen_tarih}")
        konu_1 = st.text_input(f"✍️ {sec_ders1} Çalıştığın Konu Adı:", placeholder="Örn: Sözcükte Anlam / Temel Kavramlar", key=f"k1_{secilen_tarih}")
        
        t3 = st.checkbox(f"14.20 - {sec_ders2} Konu Videosu + Soru Çözümü", key=f"v2_{secilen_tarih}")
        konu_2 = st.text_input(f"✍️ {sec_ders2} Çalıştığın Konu Adı:", placeholder="Örn: İlk Türk Devletleri / İklim Bilgisi", key=f"k2_{secilen_tarih}")
        
        t5 = st.checkbox("16.10 - 20 Paragraf Çözümü", key=f"para_{secilen_tarih}")
        t6 = st.checkbox("17.00 - Günlük Genel Tekrar", key=f"genel_tekrar_{secilen_tarih}")
        
        if st.button(f"💾 {secilen_tarih.strftime('%d.%m.%Y')} Konularını Veritabanına Kaydet"):
            if konu_1.strip():
                supabase.table("kpss_biten_konular").insert({
                    "tarih": str(secilen_tarih), "ders": sec_ders1, "konu": konu_1.strip()
                }).execute()
            if konu_2.strip():
                supabase.table("kpss_biten_konular").insert({
                    "tarih": str(secilen_tarih), "ders": sec_ders2, "konu": konu_2.strip()
                }).execute()
                
            st.success("✅ Konular Supabase bulut veritabanına kalıcı olarak kaydedildi!")
            time.sleep(1)
            st.rerun()

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
    soru_tarihi = st.date_input("📅 Soru Kaydı İçin Tarih Seçin:", value=bugun, key="soru_tarih")
    
    dersler_liste = ["Matematik", "Türkçe", "Coğrafya", "Tarih", "Vatandaşlık"]
    girilen_veriler = {}
    
    col_d1, col_d2 = st.columns(2)
    for i, d_adi in enumerate(dersler_liste):
        target_col = col_d1 if i < 3 else col_d2
        with target_col:
            st.markdown(f"**📚 {d_adi}**")
            d = st.number_input(f"{d_adi} Doğru", min_value=0, max_value=200, key=f"{d_adi}_d_{soru_tarihi}", step=1)
            y = st.number_input(f"{d_adi} Yanlış", min_value=0, max_value=200, key=f"{d_adi}_y_{soru_tarihi}", step=1)
            
            net = float(d) - (float(y) * 0.25)
            st.markdown(f"👉 **Net: {net:.2f}**")
            girilen_veriler[d_adi] = {"d": int(d), "y": int(y), "net": net, "toplam": int(d) + int(y)}
            st.markdown("---")
    
    if st.button(f"🚀 {soru_tarihi.strftime('%d.%m.%Y')} Soru Sonuçlarını Veritabanına Kaydet", type="primary"):
        for d_adi, detay in girilen_veriler.items():
            if detay["toplam"] > 0:
                supabase.table("kpss_soru_gecmisi").insert({
                    "tarih": str(soru_tarihi),
                    "ders": d_adi,
                    "dogru": detay["d"],
                    "yanlis": detay["y"],
                    "net": detay["net"],
                    "toplam": detay["toplam"]
                }).execute()
        st.success("✅ Sorular Supabase veritabanına kalıcı olarak işlendi!")
        time.sleep(1)
        st.rerun()

with tab4:
    st.subheader("👤 Profil & Bitirilen Konular Karnesi (Kalıcı Veri)")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("### 📈 Genel Soru İstatistiklerin")
        toplam_dogru = sum([item["dogru"] for item in soru_gecmisi]) if soru_gecmisi else 0
        toplam_yanlis = sum([item["yanlis"] for item in soru_gecmisi]) if soru_gecmisi else 0
        
        st.info(f"📚 **Toplam Çözülen Soru:** {toplam_cozulen_soru}")
        st.success(f"✅ **Toplam Doğru:** {toplam_dogru}")
        st.warning(f"❌ **Toplam Yanlış:** {toplam_yanlis}")
        
    with col_p2:
        st.markdown("### 🎯 Bitirdiğin Konular Listesi")
        if biten_konular:
            for k_item in biten_konular:
                st.write(f"📌 **[{k_item['tarih']}] {k_item['ders']}:** {k_item['konu']}")
        else:
            st.info("Henüz kaydedilmiş bir konu yok.")

    if soru_gecmisi:
        st.markdown("### 📊 Soru Detay Tablosu")
        df_soru = pd.DataFrame(soru_gecmisi)[["tarih", "ders", "dogru", "yanlis", "net", "toplam"]]
        st.dataframe(df_soru, use_container_width=True)

with tab5:
    st.subheader("🔥 75 Günlük Zinciri Kırma Takvimi")
    col_z1, col_z2 = st.columns([2, 1])
    with col_z1:
        st.markdown(f"**Şu anki zincir durumun: {zincir_gun}. Gün**")
        kutular_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px;'>"
        for g in range(1, 76):
            if g <= zincir_gun:
                kutular_html += f"<div style='width: 35px; height: 35px; background: #e11d48; color: white; display: flex; align-items: center; justify-content: center; border-radius: 6px; font-weight: bold; font-size: 12px;'>{g}</div>"
            else:
                kutular_html += f"<div style='width: 35px; height: 35px; background: #1f2937; color: #9ca3af; display: flex; align-items: center; justify-content: center; border-radius: 6px; font-weight: bold; font-size: 12px;'>{g}</div>"
        kutular_html += "</div>"
        st.markdown(kutular_html, unsafe_allow_html=True)
    
    with col_z2:
        st.markdown("### ⚙️ Zincir Yönetimi")
        if st.button("🔥 Bugün Çalıştım, Zinciri İlerlet"):
            yeni_zincir = zincir_gun + 1
            supabase.table("kpss_zincir").update({"zincir_gun": yeni_zincir}).eq("id", 1).execute()
            st.success("Zincir güncellendi!")
            time.sleep(1)
            st.rerun()

with tab6:
    st.subheader("🍅 Çalışan Geri Sayımlı Pomodoro Sayaç")
    dakika = st.slider("Çalışma Süresi (Dakika)", min_value=1, max_value=60, value=25)
    
    col_b, col_s = st.columns(2)
    with col_b:
        baslat_p = st.button("▶️ Geri Sayımı Başlat")
    
    if baslat_p:
        placeholder = st.empty()
        toplam_saniye = dakika * 60
        for s in range(toplam_saniye, -1, -1):
            m = s // 60
            sn = s % 60
            placeholder.markdown(f'<div class="timer-box">⏳ {m:02d}:{sn:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
        st.balloons()
        st.success("🎉 Tebrikler! Odak seansı başarıyla tamamlandı!")

with tab7:
    st.subheader("🧠 Günün Motivasyon Sözü")
    st.info("“Canım istemese bile masaya oturacağım. Çünkü başarı motivasyonla değil, disiplinle gelir.”")
