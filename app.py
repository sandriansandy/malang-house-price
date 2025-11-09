import streamlit as st
from utils import predict_price

# =========================
# KONFIGURASI HALAMAN & STYLING
# =========================
st.set_page_config(
    page_title="Prediksi Harga Properti",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk mempercantik tampilan
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .section-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        text-align: center;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Input field styling */
    .stSelectbox, .stTextInput, .stNumberInput {
        margin-bottom: 1rem;
    }
    
    /* Custom divider */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        margin: 1.5rem 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER APLIKASI
# =========================
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size:2.5rem;">🏠 PREDIKSI HARGA PROPERTI</h1>
    <p style="margin:0.5rem 0 0 0; font-size:1.1rem; opacity:0.9;">
        Prediksi harga properti akurat dengan teknologi machine learning
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# PILIHAN TIPE PROPERTI
# =========================
st.markdown('<div class="section-header"><h3 style="margin:0;">📋 TIPE PROPERTI</h3></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    tipe_properti = st.selectbox(
        "Pilih jenis properti yang ingin diprediksi:",
        ["Properti Bangunan (Rumah, Ruko, Kost, Hotel, dll)", "Tanah"],
        key="tipe_properti"
    )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# =========================
# INPUT FORM BERDASARKAN TIPE
# =========================
st.markdown('<div class="section-header"><h3 style="margin:0;">📝 DATA PROPERTI</h3></div>', unsafe_allow_html=True)

if "Bangunan" in tipe_properti:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kecamatan = st.selectbox(
            "Kecamatan", 
            ["Lowokwaru", "Kedungkandang", "Sukun", "Klojen", "Blimbing"],
            key="kecamatan_bangunan"
        )
        bulan = st.selectbox(
            "Bulan Transaksi",
            ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", 
             "Agustus", "September", "Oktober", "November", "Desember"],
            key="bulan_bangunan"
        )
        kamar_tidur = st.number_input(
            "Kamar Tidur", 
            0, 20, 3,
            help="Jumlah kamar tidur"
        )
    
    with col2:
        luas_bangunan = st.number_input(
            "Luas Bangunan (m²)", 
            0.0, 10000.0, 60.0, 1.0,
            help="Masukkan luas bangunan dalam meter persegi"
        )
        luas_tanah = st.number_input(
            "Luas Tanah (m²)", 
            0.0, 10000.0, 72.0, 1.0,
            help="Masukkan luas tanah dalam meter persegi"
        )
        kondisi_properti = st.selectbox(
            "Kondisi Properti", 
            ["Bagus", "Baru", "Butuh Renovasi", "Renovasi Minimum", "Renovasi Total", "Sudah Renovasi", "Tanah"],
            key="kondisi_properti"
        )
    
    with col3:
        kamar_mandi = st.number_input(
            "Kamar Mandi", 
            0, 20, 2,
            help="Jumlah kamar mandi"
        )
        jumlah_lantai = st.number_input(
            "Jumlah Lantai", 
            0, 100, 1,
            help="Jumlah lantai bangunan"
        )
    category = "Bangunan"

else:  # Tanah
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kecamatan = st.selectbox(
            "Kecamatan", 
            ["Lowokwaru", "Kedungkandang", "Sukun", "Klojen", "Blimbing"],
            key="kecamatan_bangunan"
        )
    
    with col2:
        luas_bangunan = 0
        bulan = st.selectbox(
            "Bulan Transaksi",
            ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", 
             "Agustus", "September", "Oktober", "November", "Desember"],
            key="bulan_bangunan"
        )
        kamar_tidur = 0
    
    with col3:
        luas_tanah = st.number_input(
            "Luas Tanah (m²)", 
            0.0, 10000.0, 72.0, 1.0,
            help="Masukkan luas tanah dalam meter persegi"
        )
        kamar_mandi = 0
        jumlah_lantai = 0
    
    category = "Tanah"

# =========================
# TOMBOL PREDIKSI
# =========================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3>🎯 Siap untuk Prediksi?</h3>
        <p>Klik tombol di bawah untuk memprediksi harga properti Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    start_predict = st.button("🔮 MULAI PREDIKSI HARGA", use_container_width=True)

# =========================
# HASIL PREDIKSI
# =========================
if start_predict:
    with st.spinner("🔄 Sedang menganalisis dan memprediksi harga properti..."):
        # Simulasi proses loading
        import time
        time.sleep(2)
        
        hasil_prediksi = predict_price({
            "luas_tanah": luas_tanah,
            "luas_bangunan": luas_bangunan,
            "kamar_mandi": kamar_mandi,
            "kamar_tidur": kamar_tidur,
            "kondisi_properti": kondisi_properti if "Bangunan" in tipe_properti else "Tanah",
            "kecamatan": kecamatan,
            "bulan": bulan,
            "jumlah_lantai": jumlah_lantai
        }, category=category)
        
        st.success("✅ Prediksi berhasil diselesaikan!")
        
        st.markdown(
            f"""
            <div class="prediction-card">
                <h3 style="margin:0 0 1rem 0; font-size:1.5rem;">💰 HASIL PREDIKSI HARGA PROPERTI</h3>
                <h1 style="margin:0; font-size:2.5rem; font-weight:bold;">Rp {hasil_prediksi:,.0f}</h1>
                <p style="margin:1rem 0 0 0; opacity:0.9;">
                    Harga prediksi berdasarkan data yang dimasukkan
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Informasi tambahan
        if "Bangunan" in tipe_properti:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tipe Properti", "Bangunan" if "Bangunan" in tipe_properti else "Tanah")
                st.metric("Kamar Tidur", f"{kamar_tidur} Kamar")
                st.metric("Bulan", bulan)
            with col2:
                st.metric("Luas Tanah", f"{luas_tanah:,.0f} m²")
                st.metric("Kamar Mandi", f"{kamar_mandi} Kamar")
                st.metric("Kecamatan", kecamatan)
            with col3:
                if "Bangunan" in tipe_properti:
                    st.metric("Luas Bangunan", f"{luas_bangunan:,.0f} m²")
                st.metric("Jumlah Lantai", f"{jumlah_lantai} Lantai")
                st.metric("Kondisi Properti", f"{kondisi_properti}")
        
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tipe Properti", "Tanah")
            with col2:
                st.metric("Luas Tanah", f"{luas_tanah:,.0f} m²")


# =========================
# FOOTER & EMBED INFO
# =========================
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding:1.5rem; background-color:#f8f9fa; border-radius:10px;">
    <h4 style="color:#667eea; margin-bottom:0.5rem;">🌐 Bagikan Prediksi Anda</h4>
    <p style="margin:0; color:#666; font-size:0.9rem;">
        Gunakan iframe untuk menampilkan prediksi di website atau artikel Anda
    </p>
</div>
""", unsafe_allow_html=True)

# st.code di tengah dengan styling yang sesuai
st.code("""
            <iframe
            src="https://malang-house-price-mefnzjebqfop7rpjb3486i.streamlit.app/?embed=true"
            style="height: 450px; width: 100%;"
            ></iframe>
        """, language="html")
