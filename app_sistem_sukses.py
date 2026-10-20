import datetime
import json
import os
import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG FOR MOBILE ---
st.set_page_config(
    page_title="Sistem Sukses Mobile",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MOBILE-FIRST CSS ---
st.markdown("""
<style>
    /* Container setup for mobile screen width */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 480px !important;
        margin: auto;
    }
    
    /* Header card mobile */
    .mobile-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 16px 18px;
        border-radius: 14px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.18);
    }
    .mobile-header h2 {
        color: #FFFFFF !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .mobile-header p {
        color: #E0E7FF !important;
        font-size: 0.85rem !important;
        margin-top: 4px !important;
        margin-bottom: 0 !important;
    }

    /* Active Card Mobile */
    .active-card-mobile {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .active-card-mobile .tag {
        color: #2563EB;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .active-card-mobile h3 {
        color: #1E3A8A;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.3;
    }
    .time-badge {
        display: inline-block;
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* SOP Card Mobile */
    .sop-card-mobile {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 15px;
        border-radius: 12px;
        margin-top: 6px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    .sop-card-mobile h4 {
        color: #1F2937;
        font-size: 1.05rem;
        margin-top: 0;
        margin-bottom: 10px;
        font-weight: 700;
    }
    .sop-card-mobile li {
        margin-bottom: 8px;
        font-size: 0.9rem;
        line-height: 1.45;
        color: #374151;
    }

    /* Quote Box Mobile */
    .quote-mobile-item {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 12px 14px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        line-height: 1.4;
        color: #78350F;
        font-weight: 500;
    }

    /* Habit Box Container */
    .habit-container {
        background-color: #F9FAFB;
        border: 1px solid #F3F4F6;
        padding: 12px 14px;
        border-radius: 12px;
        margin-bottom: 12px;
    }

    /* Streamlit Checkbox Custom Styling for Touch Target */
    div[data-baseweb="checkbox"] {
        padding: 5px 0px;
    }
    div[data-baseweb="checkbox"] label {
        font-size: 0.92rem !important;
        color: #1F2937 !important;
        line-height: 1.3 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- TIMEZONE HANDLING ---
try:
    from zoneinfo import ZoneInfo
    TIMEZONE_WIB = ZoneInfo("Asia/Jakarta")
    TIMEZONE_WITA = ZoneInfo("Asia/Makassar")
    TIMEZONE_WIT = ZoneInfo("Asia/Jayapura")
except Exception:
    import pytz
    TIMEZONE_WIB = pytz.timezone("Asia/Jakarta")
    TIMEZONE_WITA = pytz.timezone("Asia/Makassar")
    TIMEZONE_WIT = pytz.timezone("Asia/Jayapura")

# --- DATA INITIALIZATION ---
DATA_FILE = "bank_bahan.json"

def load_bank_bahan():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "quotes": [
            "Continuous effort - not strength or intelligence - is the key to unlocking our potential.",
            "The secret of getting ahead is getting started.",
            "Small daily improvements over time lead to stunning results.",
            "Discipline is choosing between what you want now and what you want most.",
            "You don't have to be great to start, but you have to start to be great.",
            "Communication is a skill that you can learn. It's like riding a bicycle."
        ]
    }

def save_bank_bahan(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

bank_data = load_bank_bahan()

# --- SIDEBAR PENGATURAN & SIMULASI ---
st.sidebar.header("⚙️ Pengaturan Mobile")

tz_option = st.sidebar.selectbox(
    "Pilih Zona Waktu:",
    ["WIB (Asia/Jakarta)", "WITA (Asia/Makassar)", "WIT (Asia/Jayapura)"],
    index=0
)

if "WITA" in tz_option:
    current_tz = TIMEZONE_WITA
    tz_label = "WITA"
    tz_offset_hours = 8
elif "WIT" in tz_option:
    current_tz = TIMEZONE_WIT
    tz_label = "WIT"
    tz_offset_hours = 9
else:
    current_tz = TIMEZONE_WIB
    tz_label = "WIB"
    tz_offset_hours = 7

now_real = datetime.datetime.now(current_tz)

use_sim = st.sidebar.checkbox("Fitur Simulasi Waktu Manual")

if use_sim:
    sim_days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    selected_day = st.sidebar.selectbox("Pilih Hari Simulasi:", sim_days)
    selected_time = st.sidebar.time_input("Pilih Jam Simulasi:", value=now_real.time())
    now_time = selected_time
    day_name = selected_day
else:
    now_time = now_real.time()
    days_map = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
    day_name = days_map[now_real.weekday()]

# --- HEADER MOBILE APP ---
st.markdown(f"""
<div class='mobile-header'>
    <h2>🚀 Sistem Sukses Assistant</h2>
    <p>📅 <b>{day_name}</b> | Zona: <b>{tz_label}</b></p>
</div>
""", unsafe_allow_html=True)

# Embedded Client-side JavaScript Clock (Mobile Optimized)
clock_html = f"""
<div style="background-color: #F3F4F6; padding: 8px 14px; border-radius: 10px; text-align: center; margin-bottom: 16px; border: 1px solid #E5E7EB;">
    <span style="font-size: 0.82rem; color: #4B5563; font-weight: 600;">⏱️ WAKTU REALTIME: </span>
    <span id="liveClock" style="font-size: 1.05rem; font-weight: 700; color: #1E3A8A; font-family: monospace;">--:--:--</span>
</div>

<script>
function updateClock() {{
    var now = new Date();
    var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
    var targetDate = new Date(utc + (3600000 * {tz_offset_hours}));
    
    var h = String(targetDate.getHours()).padStart(2, '0');
    var m = String(targetDate.getMinutes()).padStart(2, '0');
    var s = String(targetDate.getSeconds()).padStart(2, '0');
    
    var clockElem = document.getElementById('liveClock');
    if (clockElem) {{
        clockElem.innerText = h + ":" + m + ":" + s + " {tz_label}";
    }}
}}
setInterval(updateClock, 1000);
updateClock();
</script>
"""
components.html(clock_html, height=45)

# --- BLOK SCHEDULE ENGINE ---
def get_current_block(day, current_time):
    t_val = current_time.hour * 60 + current_time.minute
    
    # Rutin Pagi
    if 300 <= t_val < 360: # 05.00 - 06.00
        return "alquran", "Blok Spiritual & Hafalan Al-Qur'an", "05.00 - 06.00"
    elif 360 <= t_val < 420: # 06.00 - 07.00
        return "capcut_quote", "Blok CapCut Batching Quote (6 Template)", "06.00 - 07.00"
        
    # Rutin Perkuliahan SI (Senin - Jumat)
    if day == "Senin":
        if 510 <= t_val < 610: # 08.30 - 10.10
            return "kuliah", "Kuliah: Pengantar Organisasi", "08.30 - 10.10"
        elif 630 <= t_val < 690: # 10.30 - 11.30
            return "capcut_vlog", "Blok CapCut Vlog (1 Template)", "10.30 - 11.30"
        elif 780 <= t_val < 880: # 13.00 - 14.40
            return "kuliah", "Kuliah: Keterampilan Komunikasi", "13.00 - 14.40"
    elif day == "Selasa":
        if 570 <= t_val < 670: # 09.30 - 11.10
            return "kuliah", "Kuliah: Kalkulus", "09.30 - 11.10"
        elif 780 <= t_val < 840: # 13.00 - 14.00
            return "capcut_vlog", "Blok CapCut Vlog (1 Template)", "13.00 - 14.00"
    elif day == "Rabu": # Full Online
        if 620 <= t_val < 720: # 10.20 - 12.00
            return "kuliah", "Kuliah Online: Bahasa Indonesia", "10.20 - 12.00"
        elif 780 <= t_val < 880: # 13.00 - 14.40
            return "kuliah", "Kuliah Online: Agama Islam", "13.00 - 14.40"
        elif 880 <= t_val < 980: # 14.40 - 16.20
            return "kuliah", "Kuliah Online: Pancasila", "14.40 - 16.20"
    elif day == "Kamis": # Deep Work
        if 510 <= t_val < 690: # 08.30 - 11.30
            return "coding", "Deep Work: Coding & Tugas SI", "08.30 - 11.30"
        elif 780 <= t_val < 840: # 13.00 - 14.00
            return "capcut_vlog", "Blok CapCut Vlog (1 Template)", "13.00 - 14.00"
    elif day == "Jumat":
        if 480 <= t_val < 600: # 08.00 - 10.00
            return "kuliah", "Kuliah: Algoritma dan Pemrograman", "08.00 - 10.00"
        elif 600 <= t_val < 660: # 10.00 - 11.00
            return "capcut_vlog", "Blok CapCut Vlog (1 Template)", "10.00 - 11.00"
        elif 780 <= t_val < 880: # 13.00 - 14.40
            return "kuliah", "Kuliah: Konsep Sistem Informasi", "13.00 - 14.40"
            
    # Rutin Sore & Malam
    if 960 <= t_val < 1050: # 16.00 - 17.30
        return "coding", "Blok Practice Coding & Logika", "16.00 - 17.30"
    elif 1170 <= t_val < 1230: # 19.30 - 20.30
        return "softskills", "Blok Soft Skills (Inggris & Speaking)", "19.30 - 20.30"
    elif t_val >= 1260 or t_val < 300: # 21.00 - 05.00
        return "istirahat", "Blok Istirahat & Recovery (Tidur)", "21.00 - 05.00"
        
    return "free", "Blok Fleksibel / Rest Mandiri", "-"

block_type, block_title, block_time = get_current_block(day_name, now_time)

# Display Active Card Mobile
st.markdown(f"""
<div class='active-card-mobile'>
    <div class='tag'>📍 BLOK AKTIF SAAT INI</div>
    <h3>{block_title}</h3>
    <span class='time-badge'>⏰ Durasi: {block_time}</span>
</div>
""", unsafe_allow_html=True)

# --- CONTEXTUAL CONTENT DISPLAY ---
st.markdown("#### 💡 Panduan & Bahan Otomatis")

if block_type == "capcut_quote":
    st.success("🎯 **Tugas**: Buat 6 Template Quote CapCut.")
    st.markdown("<b>Stok 6 Quote Hari Ini:</b>", unsafe_allow_html=True)
    quotes = bank_data.get("quotes", [])[:6]
    for idx, q in enumerate(quotes, 1):
        st.markdown(f"<div class='quote-mobile-item'><b>#{idx}:</b> {q}</div>", unsafe_allow_html=True)
    st.info("💡 *Tips*: Copy quote di atas, paste ke template CapCut, export sekaligus!")

elif block_type == "capcut_vlog":
    st.success("🎬 **Tugas**: Buat 1 Template Vlog CapCut.")
    st.markdown("""
    <div class='sop-card-mobile'>
        <h4>Formula Vlog 15 Detik:</h4>
        <ul>
            <li><b>0 - 3 Detik (Hook)</b>: Cuplikan aktivitas menarik.</li>
            <li><b>3 - 13 Detik (Body)</b>: Process shot belajar/kuliah.</li>
            <li><b>13 - 15 Detik (CTA)</b>: Penutup dengan pesan positif.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "alquran":
    st.markdown("""
    <div class='sop-card-mobile'>
        <h4>📖 SOP 3 Tahap Menghafal Al-Qur'an:</h4>
        <ol>
            <li><b>1. Muroja'ah (15 Mnt)</b>: Ulangi 2-3 halaman hafalan lama.</li>
            <li><b>2. Ziyadah (20 Mnt)</b>: Baca ayat baru 5x mushaf, 5x tanpa mushaf.</li>
            <li><b>3. Penanda (5 Mnt)</b>: Tes hafalan & tandai halaman besok.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "coding":
    st.markdown("""
    <div class='sop-card-mobile'>
        <h4>💻 SOP Belajar Coding (Metode 20/80):</h4>
        <ol>
            <li><b>20% Waktu (12 Mnt)</b>: Pahami konsep/modul materi.</li>
            <li><b>80% Waktu (48 Mnt)</b>: Hands-on Coding di IDE/VS Code!</li>
            <li><b>Catat Error</b>: Tulis pesan error & solusinya.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "softskills":
    st.markdown("""
    <div class='sop-card-mobile'>
        <h4>🗣️ SOP Soft Skills 3-in-1:</h4>
        <ol>
            <li><b>1. Reading (15 Mnt)</b>: Baca artikel persuasi/komunikasi Bahasa Inggris.</li>
            <li><b>2. Shadowing (15 Mnt)</b>: Baca nyaring di depan cermin/kamera.</li>
            <li><b>3. Extract Quote</b>: Ambil 1 kalimat favorit ke Bank Quote CapCut!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "kuliah":
    st.info("📚 **Fokus Perkuliahan**: Catat materi kuliah & pahami tugas dosen.")

elif block_type == "istirahat":
    st.warning("🌙 **Waktu Istirahat**: Jauhkan layar HP. Istirahat yang cukup!")

else:
    st.info("☕ **Waktu Fleksibel**: Makan, ibadah, atau evaluasi harian.")

st.markdown("---")

# --- CHECKLIST HABIT HARIAN (MOBILE SINGLE COLUMN STACK) ---
st.markdown("#### ✅ Habit Checklist Harian")
st.markdown("<div class='habit-container'>", unsafe_allow_html=True)

h1 = st.checkbox("📖 Menghafal Al-Qur'an (Ziyadah + Muroja'ah)")
h2 = st.checkbox("🎨 CapCut Batching Quote (6 Template)")
h3 = st.checkbox("🎬 CapCut Vlog (1 Template)")
h4 = st.checkbox("📚 Kuliah / Tugas Sistem Informasi")
h5 = st.checkbox("💻 Belajar Coding / Algoritma (1 Jam)")
h6 = st.checkbox("🗣️ Soft Skills (Inggris / Persuasi / Speaking)")

st.markdown("</div>", unsafe_allow_html=True)

completed = sum([h1, h2, h3, h4, h5, h6])
st.progress(completed / 6)
st.caption(f"📊 Capaian: {completed} / 6 Habit Selesai ({int(completed/6*100)}%)")

st.markdown("---")

# --- EXPANDER PENGELOLA BANK BAHAN CAPCUT ---
with st.expander("📦 Bank Bahan & Tambah Quote"):
    new_quote = st.text_area("Tulis Quote Bahasa Inggris Baru:", height=70)
    if st.button("Simpan Quote Baru"):
        if new_quote.strip():
            bank_data["quotes"].append(new_quote.strip())
            save_bank_bahan(bank_data)
            st.success("Quote berhasil disimpan!")
            st.rerun()
