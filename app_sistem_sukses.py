import datetime
import json
import os
import streamlit as st
import streamlit.components.v1 as components

# Set Page Config
st.set_page_config(
    page_title="Sistem Sukses Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .active-card {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .sop-box {
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .quote-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        font-family: monospace;
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

# --- INITIALIZE DATA & BANK BAHAN ---
DATA_FILE = "bank_bahan.json"

def load_bank_bahan():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
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

# --- SIDEBAR & TIME SIMULATION / CONFIG ---
st.sidebar.header("⚙️ Pengaturan & Simulasi")

# Zona Waktu Selection
tz_option = st.sidebar.selectbox(
    "Zona Waktu Anda:",
    ["WIB (Asia/Jakarta)", "WITA (Asia/Makassar)", "WIT (Asia/Jayapura)"],
    index=0
)

if "WITA" in tz_option:
    current_tz = TIMEZONE_WITA
    tz_iana = "Asia/Makassar"
    tz_label = "WITA"
elif "WIT" in tz_option:
    current_tz = TIMEZONE_WIT
    tz_iana = "Asia/Jayapura"
    tz_label = "WIT"
else:
    current_tz = TIMEZONE_WIB
    tz_iana = "Asia/Jakarta"
    tz_label = "WIB"

# Dapatkan Waktu Sekarang Sesuai Timezone
now_real = datetime.datetime.now(current_tz)

use_sim = st.sidebar.checkbox("Gunakan Simulasi Waktu Manual")

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

# Auto Refresh untuk memperbarui Blok Aktif setiap 60 detik (jika tidak dalam mode simulasi)
auto_refresh = st.sidebar.checkbox("Auto Refresh Blok (Setiap 60 dtk)", value=True)

# --- HEADER APP ---
st.markdown("<div class='main-header'>🚀 Personal System Assistant</div>", unsafe_allow_html=True)

# Widget Jam Digital Realtime (Ticking Seconds via JavaScript)
if not use_sim:
    js_clock_html = f"""
    <div style="font-family: system-ui, -apple-system, sans-serif; background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%); border: 1px solid #BFDBFE; padding: 12px 20px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.1rem;">⏰</span>
            <span style="font-size: 0.95rem; color: #1E40AF; font-weight: 600;">Waktu Realtime ({tz_label}):</span>
            <span id="live-clock" style="font-size: 1.35rem; font-weight: 800; color: #1D4ED8; font-family: monospace; letter-spacing: 1px; margin-left: 6px;">--:--:--</span>
        </div>
        <div style="font-size: 1rem; color: #1E293B; font-weight: 600;">
            📅 Hari: <span style="color: #2563EB;">{day_name}</span>
        </div>
    </div>

    <script>
    function updateClock() {{
        try {{
            const options = {{ timeZone: '{tz_iana}', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }};
            const now = new Date();
            const formatter = new Intl.DateTimeFormat('en-US', options);
            document.getElementById('live-clock').textContent = formatter.format(now);
        }} catch(e) {{
            const now = new Date();
            document.getElementById('live-clock').textContent = now.toTimeString().split(' ')[0];
        }}
    }}
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """
    components.html(js_clock_html, height=65)
else:
    st.markdown(f"<div class='sub-header'>⚠️ <b>MODAL SIMULASI MANUAL</b> | Hari: <b>{day_name}</b> | Jam Simulasi: <b>{now_time.strftime('%H:%M:%S')}</b> ({tz_label})</div>", unsafe_allow_html=True)

# Optional Client-side Auto Reload every 60 seconds to refresh active blocks automatically
if auto_refresh and not use_sim:
    components.html("""
    <script>
    setTimeout(function(){
        window.parent.postMessage({type: 'streamlit:render'}, '*');
    }, 60000);
    </script>
    """, height=0)

# --- DEFINISI BLOK JADWAL ---
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
            return "coding", "Deep Work: Coding & Tugas Sistem Informasi", "08.30 - 11.30"
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
        return "coding", "Blok Practice Coding & Logika Pemrograman", "16.00 - 17.30"
    elif 1170 <= t_val < 1230: # 19.30 - 20.30
        return "softskills", "Blok Soft Skills (Inggris, Public Speaking, Persuasi)", "19.30 - 20.30"
    elif t_val >= 1260 or t_val < 300: # 21.00 - 05.00
        return "istirahat", "Blok Istirahat & Fast Recovery (Tidur)", "21.00 - 05.00"
        
    return "free", "Blok Fleksibel / Istirahat Mandiri", "-"

block_type, block_title, block_time = get_current_block(day_name, now_time)

# --- DISPLAY BLOK AKTIF & CONTEXTUAL MATERIAL ---
st.markdown(f"""
<div class='active-card'>
    <h3>📍 Aktivitas Aktif Saat Ini</h3>
    <h2>{block_title}</h2>
    <p><b>Durasi Blok:</b> {block_time}</p>
</div>
""", unsafe_allow_html=True)

st.subheader("💡 Panduan & Bahan Otomatis Untuk Jam Ini")

if block_type == "capcut_quote":
    st.success("🎯 **Tugas**: Buat 6 Template Quote CapCut. Gunakan stok quote di bawah ini!")
    st.markdown("<b>Stok 6 Quote Bahasa Inggris Hari Ini:</b>", unsafe_allow_html=True)
    quotes = bank_data.get("quotes", [])[:6]
    for idx, q in enumerate(quotes, 1):
        st.markdown(f"<div class='quote-box'><b>Quote {idx}:</b> {q}</div>", unsafe_allow_html=True)
    st.info("💡 *Tips Batching*: Copy teks quote di atas, paste ke layout preset CapCut Anda, ganti audio, lalu export sekaligus.")

elif block_type == "capcut_vlog":
    st.success("🎬 **Tugas**: Buat 1 Template Vlog CapCut.")
    st.markdown("""
    <div class='sop-box'>
        <h4>Formula Video Vlog 15 Detik:</h4>
        <ul>
            <li><b>0 - 3 Detik (Hook)</b>: Cuplikan aktivitas menarik (misal: membuka laptop / mushaf).</li>
            <li><b>3 - 13 Detik (Body)</b>: Process shot (suasana belajar / suasana perkuliahan).</li>
            <li><b>13 - 15 Detik (CTA)</b>: Penutup dengan pertanyaan atau pesan positif.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "alquran":
    st.markdown("""
    <div class='sop-box'>
        <h4>📖 SOP 3 Tahap Menghafal Al-Qur'an:</h4>
        <ol>
            <li><b>Tahap 1 (15 Mnt) - Muroja'ah</b>: Ulangi 2-3 halaman hafalan lama agar tetap lancar.</li>
            <li><b>Tahap 2 (20 Mnt) - Ziyadah</b>: Baca ayat baru 5x dengan mushaf, 5x tanpa mushaf. Sambungkan per baris.</li>
            <li><b>Tahap 3 (5 Mnt) - Penanda</b>: Tes hafalan baru tanpa salah, lalu tandai halaman untuk besok.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "coding":
    st.markdown("""
    <div class='sop-box'>
        <h4>💻 SOP Belajar Coding (Metode 20/80):</h4>
        <ol>
            <li><b>20% Waktu (12 Mnt)</b>: Baca konsep/modul (misal: Algoritma, Python syntax, Struktur Data).</li>
            <li><b>80% Waktu (48 Mnt)</b>: Hands-on Coding! Ketik kode secara langsung di IDE/Editor.</li>
            <li><b>Catat Error</b>: Dokumentasikan pesan error dan cara penyelesaiannya di catatan ringkas.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "softskills":
    st.markdown("""
    <div class='sop-box'>
        <h4>🗣️ SOP Integrasi Soft Skills 3-in-1:</h4>
        <ol>
            <li><b>Langkah 1 (Inggris & Persuasi)</b>: Baca 1 artikel/bab tentang teknik komunikasi/persuasi Bahasa Inggris (15 mnt).</li>
            <li><b>Langkah 2 (Public Speaking)</b>: Lakukan <i>Shadowing</i> - baca nyaring artikel tersebut di depan cermin/kamera (15 mnt).</li>
            <li><b>Langkah 3 (Content Extraction)</b>: Ambil 1 quote paling menginspirasi dari artikel tersebut & tambahkan ke Bank Bahan CapCut!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif block_type == "kuliah":
    st.info("📚 **Fokus Perkuliahan**: Catat poin-poin utama materi kuliah dan pahami tugas yang diberikan dosen.")

elif block_type == "istirahat":
    st.warning("🌙 **Waktu Istirahat**: Jauhkan layar HP/Laptop. Tidur berkualitas untuk menjaga energi & kesehatan harian.")

else:
    st.info("☕ **Waktu Fleksibel**: Gunakan untuk makan, ibadah, bersosialisasi, atau evaluasi harian.")

st.divider()

# --- CHECKLIST HABIT HARIAN ---
st.subheader("✅ Habit Checklist Harian")
c1, c2, c3 = st.columns(3)

with c1:
    h1 = st.checkbox("Menghafal Al-Qur'an (Ziyadah + Muroja'ah)")
    h2 = st.checkbox("CapCut Batching Quote (6 Template)")

with c2:
    h3 = st.checkbox("CapCut Vlog (1 Template)")
    h4 = st.checkbox("Kuliah / Tugas Sistem Informasi")

with c3:
    h5 = st.checkbox("Belajar Coding / Algoritma (1 Jam)")
    h6 = st.checkbox("Soft Skills (Inggris / Persuasi / Speaking)")

completed = sum([h1, h2, h3, h4, h5, h6])
st.progress(completed / 6)
st.caption(f"Capaian Harian: {completed} dari 6 Habit Selesai ({int(completed/6*100)}%)")

st.divider()

# --- KELOLA BANK BAHAN CAPCUT ---
st.subheader("📦 Pengelola Bank Bahan Quote CapCut")

with st.expander("➕ Tambah Quote Baru ke Bank Bahan"):
    new_quote = st.text_area("Tulis Quote Bahasa Inggris Baru:")
    if st.button("Simpan Quote"):
        if new_quote.strip():
            bank_data["quotes"].append(new_quote.strip())
            save_bank_bahan(bank_data)
            st.success("Quote baru berhasil disimpan!")
            st.rerun()
