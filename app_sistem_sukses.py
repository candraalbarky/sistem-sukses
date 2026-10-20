import datetime
import json
import os
import streamlit as st

# Set Page Config
st.set_page_config(
    page_title="Sistem Sukses Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (CSS)
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# --- INITIALIZE DATA & BANK BAHAN ---
DATA_FILE = "bank_bahan.json"


def load_bank_bahan():
    default_data = {
        "quotes": [
            "Persuasion is not about convincing people, it's about connecting with their existing desires.",
            "Clear communication is the bridge between confusion and clarity.",
            "Consistency in small actions builds unstoppable momentum over time.",
            "Speak with intention, listen with empathy, and lead with clarity.",
            "Your systems determine your success, not your willpower alone.",
            "Mastering interpersonal communication starts with understanding yourself first.",
        ],
        "vlog_script": {
            "Hook (3s)": "Cuplikan 3 detik aktivitas terpenting hari ini (misal: buka laptop/mushaf).",
            "Body (10s)": "Proses pengerjaan tugas Sistem Informasi & sesi fokus coding.",
            "CTA (2s)": "Pertanyaan interaktif untuk penonton: 'Sistem apa yang kamu bangun hari ini?'",
        },
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return default_data
    return default_data


def save_bank_bahan(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


bank_data = load_bank_bahan()

# --- JADWAL & TIME BLOCKING DATABASE ---
SCHEDULE_DB = {
    "Senin": [
        {
            "start": "05:00",
            "end": "06:00",
            "activity": "🟢 Blok Al-Qur'an (Menghafal & Muroja'ah)",
            "type": "quran",
        },
        {
            "start": "06:00",
            "end": "07:00",
            "activity": "🎬 CapCut Quote Batching (6 Template)",
            "type": "capcut_quote",
        },
        {
            "start": "08:30",
            "end": "10:10",
            "activity": "📚 Kuliah: Pengantar Organisasi",
            "type": "kuliah",
        },
        {
            "start": "10:30",
            "end": "11:30",
            "activity": "📹 CapCut Vlog Template (1 Template)",
            "type": "capcut_vlog",
        },
        {
            "start": "13:00",
            "end": "14:40",
            "activity": "📚 Kuliah: Keterampilan Komunikasi",
            "type": "kuliah",
        },
        {
            "start": "16:00",
            "end": "17:30",
            "activity": "💻 Blok Coding & Tugas Sistem Informasi",
            "type": "coding",
        },
        {
            "start": "19:30",
            "end": "20:30",
            "activity": "🗣️ Soft Skills 3-in-1 (Inggris, Speaking, Persuasi)",
            "type": "softskills",
        },
    ],
    "Selasa": [
        {
            "start": "05:00",
            "end": "06:00",
            "activity": "🟢 Blok Al-Qur'an (Menghafal & Muroja'ah)",
            "type": "quran",
        },
        {
            "start": "06:00",
            "end": "07:00",
            "activity": "🎬 CapCut Quote Batching (6 Template)",
            "type": "capcut_quote",
        },
        {
            "start": "09:30",
            "end": "11:10",
            "activity": "📚 Kuliah: Kalkulus",
            "type": "kuliah",
        },
        {
            "start": "13:00",
            "end": "14:00",
            "activity": "📹 CapCut Vlog Template (1 Template)",
            "type": "capcut_vlog",
        },
        {
            "start": "16:00",
            "end": "17:30",
            "activity": "💻 Blok Coding (Latihan Python/Algoritma)",
            "type": "coding",
        },
        {
            "start": "19:30",
            "end": "20:30",
            "activity": "🗣️ Soft Skills & Latihan Bahasa Inggris",
            "type": "softskills",
        },
    ],
    "Rabu": [
        {
            "start": "05:00",
            "end": "06:00",
            "activity": "🟢 Blok Al-Qur'an (Menghafal & Muroja'ah)",
            "type": "quran",
        },
        {
            "start": "06:00",
            "end": "07:00",
            "activity": "🎬 CapCut Quote Batching (6 Template)",
            "type": "capcut_quote",
        },
        {
            "start": "10:20",
            "end": "12:00",
            "activity": "🌐 Kuliah Online: Bahasa Indonesia",
            "type": "kuliah",
        },
        {
            "start": "13:00",
            "end": "14:40",
            "activity": "🌐 Kuliah Online: Agama Islam",
            "type": "kuliah",
        },
        {
            "start": "14:40",
            "end": "16:20",
            "activity": "🌐 Kuliah Online: Pancasila",
            "type": "kuliah",
        },
        {
            "start": "19:30",
            "end": "20:30",
            "activity": "📹 CapCut Vlog & Review Mandiri",
            "type": "capcut_vlog",
        },
    ],
    "Kamis": [
        {
            "start": "05:00",
            "end": "06:00",
            "activity": "🟢 Blok Al-Qur'an (Menghafal & Muroja'ah)",
            "type": "quran",
        },
        {
            "start": "06:00",
            "end": "07:00",
            "activity": "🎬 CapCut Quote Batching (6 Template)",
            "type": "capcut_quote",
        },
        {
            "start": "08:30",
            "end": "11:30",
            "activity": "⚡ Deep Work Day: Projek Coding & Praktik SI",
            "type": "coding",
        },
        {
            "start": "13:00",
            "end": "14:00",
            "activity": "📹 CapCut Vlog & Stock Materials Prep",
            "type": "capcut_vlog",
        },
        {
            "start": "16:00",
            "end": "17:30",
            "activity": "💻 Latihan Pemrograman & Problem Solving",
            "type": "coding",
        },
        {
            "start": "19:30",
            "end": "20:30",
            "activity": "🗣️ Soft Skills & Bank Bahan Expansion",
            "type": "softskills",
        },
    ],
    "Jumat": [
        {
            "start": "05:00",
            "end": "06:00",
            "activity": "🟢 Blok Al-Qur'an (Menghafal & Muroja'ah)",
            "type": "quran",
        },
        {
            "start": "06:00",
            "end": "07:00",
            "activity": "🎬 CapCut Quote Batching (6 Template)",
            "type": "capcut_quote",
        },
        {
            "start": "08:00",
            "end": "10:00",
            "activity": "📚 Kuliah: Algoritma dan Pemrograman",
            "type": "kuliah",
        },
        {
            "start": "10:00",
            "end": "11:00",
            "activity": "📹 CapCut Vlog Template (1 Template)",
            "type": "capcut_vlog",
        },
        {
            "start": "13:00",
            "end": "14:40",
            "activity": "📚 Kuliah: Konsep Sistem Informasi",
            "type": "kuliah",
        },
        {
            "start": "16:00",
            "end": "17:30",
            "activity": "💻 Blok Coding Mandiri (Review Materi Jumat)",
            "type": "coding",
        },
        {
            "start": "19:30",
            "end": "20:30",
            "activity": "🗣️ Soft Skills 3-in-1",
            "type": "softskills",
        },
    ],
    "Sabtu": [
        {
            "start": "05:00",
            "end": "06:00",
            "activity": "🟢 Blok Al-Qur'an (Menghafal & Muroja'ah)",
            "type": "quran",
        },
        {
            "start": "08:00",
            "end": "10:00",
            "activity": "🎬 CapCut Quote & Vlog Weekend Batching",
            "type": "capcut_quote",
        },
        {
            "start": "15:00",
            "end": "17:00",
            "activity": "💻 Personal Project Coding & Experiment",
            "type": "coding",
        },
    ],
    "Minggu": [
        {
            "start": "05:00",
            "end": "06:00",
            "activity": "🟢 Blok Al-Qur'an (Muroja'ah Pekanan)",
            "type": "quran",
        },
        {
            "start": "09:00",
            "end": "10:00",
            "activity": "📊 Weekly Review & Evaluation (Sistem Check)",
            "type": "review",
        },
        {
            "start": "16:00",
            "end": "17:30",
            "activity": "🗣️ Latihan Public Speaking & Relaxed Learning",
            "type": "softskills",
        },
    ],
}

# --- SIDEBAR CONTROL & SIMULATION ---
st.sidebar.title("🎛️ Control Panel")
mode = st.sidebar.radio(
    "Modus Penentuan Waktu:", ["Waktu Real-time", "Simulasi Waktu Manual"]
)

days_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

if mode == "Waktu Real-time":
    now = datetime.datetime.now()
    day_idx = now.weekday()  # 0 = Monday
    selected_day = days_list[day_idx]
    current_time_str = now.strftime("%H:%M")
else:
    selected_day = st.sidebar.selectbox("Pilih Hari Simulasi:", days_list)
    sim_time = st.sidebar.time_input("Pilih Jam Simulasi:", datetime.time(6, 15))
    current_time_str = sim_time.strftime("%H:%M")

st.sidebar.markdown("---")
st.sidebar.write("📌 **Pemicu Jangkar Hari Ini:**")
st.sidebar.info("• Selesai Subuh ➔ Hafalan Al-Qur'an\n• 06.00 Pagi ➔ Batching CapCut Quote\n• Selesai Kuliah ➔ CapCut Vlog\n• Jam 16.00 ➔ Blok Coding\n• Jam 19.30 ➔ Soft Skills & Inggris")

# --- MAIN CONTENT ---
st.markdown("<div class='main-header'>🚀 Personal System Assistant</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>Hari: <b>{selected_day}</b> | Jam Aktif: <b>{current_time_str}</b></div>", unsafe_allow_html=True)

# Find active schedule block
day_schedule = SCHEDULE_DB.get(selected_day, [])
active_block = None

for block in day_schedule:
    if block["start"] <= current_time_str <= block["end"]:
        active_block = block
        break

# DISPLAY ACTIVE BLOCK OR NEXT BLOCK
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("⏱️ Blok Waktu & Fokus Saat Ini")
    if active_block:
        st.markdown(
            f"""
        <div class='active-card'>
            <h3 style='margin:0; color:#1E3A8A;'>{active_block['activity']}</h3>
            <p style='margin:5px 0 0 0; color:#3B82F6;'><b>Waktu: {active_block['start']} - {active_block['end']}</b></p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        block_type = active_block["type"]
    else:
        st.info("🕒 Tidak ada jadwal blok khusus yang aktif saat ini. Anda berada di luar jam blok utama atau waktu istirahat.")
        block_type = "general"

    # CONTEXTUAL POP-UP MATERIALS
    st.markdown("### 📋 Panduan & Bahan Otomatis")
    
    if block_type == "capcut_quote" or (active_block is None and st.checkbox("Tampilkan Bahan CapCut Quote")):
        st.warning("🎬 **MODE CAPCUT QUOTE ACTIVE**: Berikut 6 Stok Quote Bahasa Inggris Hari Ini:")
        quotes = bank_data.get("quotes", [])[:6]
        for idx, q in enumerate(quotes, 1):
            st.markdown(f"<div class='quote-box'><b>Quote #{idx}:</b> {q}</div>", unsafe_allow_html=True)
        st.caption("💡 *Tips: Tinggal copy quote di atas dan paste ke template CapCut Anda!*")

    elif block_type == "capcut_vlog":
        st.success("📹 **MODE CAPCUT VLOG ACTIVE**: Formula Struktur Video Vlog 15 Detik:")
        vlog_formula = bank_data.get("vlog_script", {})
        for k, v in vlog_formula.items():
            st.write(f"• **{k}**: {v}")

    elif block_type == "quran":
        st.success("🟢 **MODE AL-QUR'AN ACTIVE**: SOP 3 Tahap Hafalan Harian:")
        st.markdown("""
        <div class='sop-box'>
        1. <b>Muroja'ah (15 Mnt)</b>: Ulangi 2–3 halaman hafalan lama.<br>
        2. <b>Ziyadah (20 Mnt)</b>: Baca ayat baru 5x lihat mushaf + 5x tanpa lihat, sambungkan per baris.<br>
        3. <b>Penanda (5 Mnt)</b>: Tes kelancaran & tandai batas untuk esok hari.
        </div>
        """, unsafe_allow_html=True)

    elif block_type == "coding":
        st.info("💻 **MODE CODING & SISTEM INFORMASI ACTIVE**: Metode 20/80 Pemrograman:")
        st.markdown("""
        <div class='sop-box'>
        1. <b>20% Teori (12 Mnt)</b>: Pahami konsep/sintaks modul Python / Algoritma.<br>
        2. <b>80% Praktik (48 Mnt)</b>: Langsung ketik kode & jalankan di IDE (Hands-on).<br>
        3. <b>Catatan Error</b>: Jika ada bug, catat pesan error dan solusinya.
        </div>
        """, unsafe_allow_html=True)

    elif block_type == "softskills":
        st.info("🗣️ **MODE SOFT SKILLS 3-IN-1 ACTIVE**: Integrasi Komunikasi & Bahasa:")
        st.markdown("""
        <div class='sop-box'>
        1. <b>Membaca (15 Mnt)</b>: Baca 1 artikel/buku persuasi/komunikasi berbahasa Inggris.<br>
        2. <b>Shadowing (10 Mnt)</b>: Baca nyaring di depan cermin/kamera untuk melatih artikulasi.<br>
        3. <b>Quotes Extraction</b>: Ambil 1 kalimat terbaik untuk ditambahkan ke Bank Bahan CapCut.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.write("Pilih salah satu jadwal di samping atau gunakan tombol simulasi waktu di sebelah kiri untuk melihat bahan otomatis.")

with col_right:
    st.subheader("📅 Jadwal Lengkap Hari Ini")
    for b in day_schedule:
        is_current = (b["start"] <= current_time_str <= b["end"])
        prefix = "👉 " if is_current else "• "
        time_text = f"**{b['start']} - {b['end']}**"
        if is_current:
            st.success(f"{prefix}{time_text}: {b['activity']}")
        else:
            st.write(f"{prefix}{time_text}: {b['activity']}")

    st.markdown("---")
    st.subheader("✅ Habit Checklist Hari Ini")
    c1 = st.checkbox("Hafalan Al-Qur'an & Muroja'ah")
    c2 = st.checkbox("CapCut 6 Template Quote")
    c3 = st.checkbox("CapCut 1 Template Vlog")
    c4 = st.checkbox("Perkuliahan Sistem Informasi")
    c5 = st.checkbox("Belajar / Praktik Coding")
    c6 = st.checkbox("Latihan Soft Skills / Inggris")
    
    completed_count = sum([c1, c2, c3, c4, c5, c6])
    st.progress(completed_count / 6.0)
    st.caption(f"Capaian Harian: {completed_count}/6 Target Selesai")

# --- BANK BAHAN MANAGEMENT TAB ---
st.markdown("---")
with st.expander("📂 Pengelola Bank Bahan Quotes CapCut (Tambah & Edit)"):
    st.write("Anda bisa menambahkan quote baru di sini. Quote ini akan tersimpan dan muncul saat blok CapCut Quote aktif.")
    new_quote = st.text_input("Input Quote Bahasa Inggris Baru:")
    if st.button("Simpan Quote Baru"):
        if new_quote.strip():
            bank_data["quotes"].append(new_quote.strip())
            save_bank_bahan(bank_data)
            st.success("Quote baru berhasil disimpan!")
            st.rerun()

    st.write("**Daftar Quote Terseimpan Saat Ini:**")
    for i, q in enumerate(bank_data.get("quotes", []), 1):
        st.write(f"{i}. {q}")
