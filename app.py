import streamlit as st
import datetime
import time
import pandas as pd
import random
from io import BytesIO

st.set_page_config(page_title="Aplikasi Motivasi Positif 💡", layout="centered")

# Daftar warna tenang (soft gradients)
gradients = [
    ("#fceabb", "#f8b500"),
    ("#a1c4fd", "#c2e9fb"),
    ("#fbc2eb", "#a6c1ee"),
    ("#d4fc79", "#96e6a1"),
    ("#84fab0", "#8fd3f4"),
    ("#ffecd2", "#fcb69f"),
    ("#cfd9df", "#e2ebf0"),
    ("#d299c2", "#fef9d7")
]
warna1, warna2 = random.choice(gradients)

# CSS dinamis
st.markdown(f"""
<style>
body {{ background: linear-gradient(135deg, {warna1}, {warna2}); }}
.title-box {{
    background: white; padding: 20px; border-radius: 12px;
    text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}}
.motivation-box {{
    background: #fff9c4; padding: 20px; margin-top: 20px;
    border-radius: 12px; text-align: center;
}}
.center-button {{ display: flex; justify-content: center; }}
.stButton>button {{
    background-color: #003b46 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 20px;
}}
</style>
""", unsafe_allow_html=True)

# 🔊 Gunakan musik dari GitHub (RAW URL)
st.audio("https://raw.githubusercontent.com/DickySaragih/Animasiku/main/chillsong.mp3", format="audio/mp3")

# Fungsi zodiak
def tentukan_zodiak(tgl):
    zodiaks = [
        ("Capricorn", (12, 22), (1, 19)), ("Aquarius", (1, 20), (2, 18)), ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)), ("Taurus", (4, 20), (5, 20)), ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)), ("Leo", (7, 23), (8, 22)), ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)), ("Scorpio", (10, 23), (11, 21)), ("Sagittarius", (11, 22), (12, 21)),
    ]
    for nama, (b1, d1), (b2, d2) in zodiaks:
        if (tgl.month == b1 and tgl.day >= d1) or (tgl.month == b2 and tgl.day <= d2):
            return nama
    return "Capricorn"

# Motivasi berdasarkan zodiak
def motivasi(z, nama, hobi):
    m = {
        "Aries": f"{nama}, Aries penuh energi! Teruslah aktif dalam {hobi}!",
        "Taurus": f"{nama}, Taurus itu tangguh. Dalam {hobi}, kamu pasti unggul!",
        "Gemini": f"{nama}, Gemini pandai bicara! {hobi} bisa jadi kekuatanmu!",
        "Cancer": f"{nama}, Cancer penuh kasih. {hobi} adalah cermin jiwamu!",
        "Leo": f"{nama}, Leo lahir untuk bersinar. Tunjukkan dirimu dalam {hobi}!",
        "Virgo": f"{nama}, Virgo teliti. Hasil karyamu dalam {hobi} akan luar biasa!",
        "Libra": f"{nama}, Libra seimbang. Jadikan {hobi} jalan damai batinmu!",
        "Scorpio": f"{nama}, Scorpio itu fokus. Dalam {hobi}, kamu tak terkalahkan!",
        "Sagittarius": f"{nama}, Sagitarius suka tantangan. Jelajahi dunia lewat {hobi}!",
        "Capricorn": f"{nama}, Capricorn rajin. Dengan {hobi}, sukses tinggal selangkah!",
        "Aquarius": f"{nama}, Aquarius kreatif. Bawa warna baru lewat {hobi}!",
        "Pisces": f"{nama}, Pisces penuh imajinasi. Jadikan {hobi} tempatmu berkhayal bebas!"
    }
    return m.get(z, f"{nama}, teruslah berjuang dalam {hobi}!")

# State
if 'data' not in st.session_state:
    st.session_state.data = []
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Sidebar riwayat
st.sidebar.title("📜 Riwayat")
if st.session_state.data:
    daftar = [f"{i+1}. {d['nama']}" for i, d in enumerate(st.session_state.data)]
    pilih = st.sidebar.selectbox("Pilih:", ["-- Pilih --"] + daftar)
    if pilih != "-- Pilih --":
        idx = int(pilih.split(".")[0]) - 1
        u = st.session_state.data[idx]
        for k in ['nama', 'gender', 'umur', 'tgl_lahir', 'zodiak', 'hobi']:
            st.sidebar.write(f"**{k.title().replace('_',' ')}**: {u[k]}")
        if st.sidebar.button("🗑️ Hapus"):
            st.session_state.data.pop(idx)
            st.rerun()

# Judul
st.markdown("<div class='title-box'><h1>💡 Aplikasi Motivasi Positif</h1></div>", unsafe_allow_html=True)

# Form pendaftaran
if not st.session_state.is_logged_in:
    st.subheader("📝 Form Pendaftaran")
    nama = st.text_input("Nama")
    gender = st.radio("Gender", ["Laki-laki", "Perempuan"], horizontal=True)
    umur = st.number_input("Umur", 5, 100)
    tgl = st.date_input("Tanggal Lahir", value=datetime.date(2000, 1, 1))
    hobi = st.text_input("Hobi")
    zodiak = tentukan_zodiak(tgl)

    if st.button("✅ Daftar"):
        if nama and hobi:
            user = {
                'nama': nama.title(), 'gender': gender, 'umur': int(umur),
                'tgl_lahir': str(tgl), 'zodiak': zodiak, 'hobi': hobi.capitalize()
            }
            st.session_state.data.append(user)
            st.session_state.user = user
            st.session_state.is_logged_in = True
            st.success(f"Selamat datang {user['nama']}!")
            time.sleep(1)
            st.rerun()
else:
    user = st.session_state.user
    st.markdown(f"### Halo, {user['nama']}!")
    st.write(f"Zodiak: {user['zodiak']} | Hobi: {user['hobi']}")
    if st.button("💌 Tampilkan Motivasi"):
        st.markdown(f"<div class='motivation-box'><h3>{motivasi(user['zodiak'], user['nama'], user['hobi'])}</h3></div>", unsafe_allow_html=True)

    if st.button("🔙 Logout"):
        st.session_state.is_logged_in = False
        st.session_state.user = None
        st.rerun()

# Unduh data
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.download_button("⬇️ Unduh CSV", data=df.to_csv(index=False), file_name="riwayat.csv", mime="text/csv")

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Riwayat')
    output.seek(0)
    st.download_button(
        label="⬇️ Unduh Excel",
        data=output,
        file_name="riwayat.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
