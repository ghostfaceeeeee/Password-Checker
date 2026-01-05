import streamlit as st
from zxcvbn import zxcvbn
from cryptography.fernet import Fernet
import secrets
import string
import time

st.set_page_config(page_title="PassGuard", page_icon="🔒", layout="wide")

st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    @keyframes blink {
        50% { border-color: transparent }
    }
    .fade-in { animation: fadeIn 1s ease-out; }
    .pulse-button { animation: pulse 2s infinite; }
    .typing-title {
        overflow: hidden;
        border-right: .15em solid orange;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .1em;
        animation: typing 3.5s steps(50, end), blink .75s step-end infinite;
        font-size: 2.5rem;
        max-width: 100%;
    }
    .stSpinner > div { border-top-color: #ff6b6b !important; }

    /* Footer adaptif tema */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: var(--background-color);
        color: var(--text-color);
        text-align: center;
        padding: 15px 0;
        font-size: 0.9rem;
        border-top: 1px solid var(--secondary-background-color);
        z-index: 1000;
    }
    .footer a {
        color: var(--primary-color);
        text-decoration: none;
        margin: 0 10px;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    .main-content {
        padding-bottom: 100px; /* Biar konten tidak tertutup footer */
    }
</style>
""", unsafe_allow_html=True)

theme = st.sidebar.selectbox("🌗 Tema Tampilan", ["Gelap (Dark)", "Cerah (Light)"], index=0)
if theme == "Cerah (Light)":
    st._config.set_option("theme.base", "light")
else:
    st._config.set_option("theme.base", "dark")

st.markdown('<h1 class="typing-title fade-in">🔒 PassGuard: Deteksi Password Lemah & Generator Aman</h1>', unsafe_allow_html=True)
st.markdown("Menggunakan algoritma zxcvbn (USENIX Security 2016) + enkripsi AES-256")

indo_common = [
    "password", "123456", "qwerty", "admin", "indonesia", "bismillah", "alhamdulillah",
    "sayang", "cinta", "rahasia", "jember", "ummjember", "jakarta", "surabaya", "bandung"
]

def translate_crack_time(english_time):
    translations = {
        "less than a second": "kurang dari 1 detik",
        "a second": "1 detik",
        "seconds": "detik",
        "a minute": "1 menit",
        "minutes": "menit",
        "an hour": "1 jam",
        "hours": "jam",
        "a day": "1 hari",
        "days": "hari",
        "a month": "1 bulan",
        "months": "bulan",
        "a year": "1 tahun",
        "years": "tahun",
        "century": "abad",
        "centuries": "abad",
        "forever": "selamanya (tak terhingga)"
    }
    translated = english_time.lower()
    for eng, indo in translations.items():
        translated = translated.replace(eng, indo)
    parts = translated.split()
    if parts and parts[0].isdigit():
        return " ".join(parts).capitalize()
    return translated.capitalize()

WORD_LIST = [
    "benar", "salah", "kucing", "anjing", "rumah", "mobil", "buku", "meja", "kursi", "pintu",
    "jendela", "lampu", "api", "air", "tanah", "angin", "matahari", "bulan", "bintang", "hujan",
    "gunung", "pantai", "hutan", "sungai", "danau", "pulau", "kota", "desa", "sekolah", "kampus",
    "teman", "keluarga", "ayah", "ibu", "kakak", "adik", "nasi", "ikan", "daging", "sayur",
    "buah", "kopi", "teh", "gula", "garam", "merah", "biru", "hijau", "kuning", "hitam"
]

def generate_password(mode, length=16, word_count=4, separator="-"):
    if "Berbasis Kata" in mode:
        words = [secrets.choice(WORD_LIST) for _ in range(word_count)]
        return separator.join(words) if separator else "".join(words)
    else:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        if "Random" in mode:
            return ''.join(secrets.choice(alphabet) for _ in range(length))
        else:
            pw = (
                secrets.choice(string.ascii_uppercase) +
                secrets.choice(string.ascii_lowercase) +
                secrets.choice(string.digits) +
                secrets.choice(string.punctuation) +
                ''.join(secrets.choice(alphabet) for _ in range(length - 4))
            )
            return ''.join(secrets.SystemRandom().sample(pw, len(pw)))

def encrypt_password(password):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return key.decode(), encrypted.decode()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.history = []

st.sidebar.header("🔐 Login")
username_input = st.sidebar.text_input("Username")
if st.sidebar.button("Login"):
    if username_input:
        st.session_state.logged_in = True
        st.session_state.username = username_input
        st.session_state.history = []
        st.success(f"Selamat datang, {username_input}!")

if st.session_state.logged_in:
    st.sidebar.success(f"Logged in: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.history = []
        st.rerun()

    menu = st.radio("Pilih Fitur", ["Cek Kekuatan Password", "Generate Password Kuat"])

    if menu == "Cek Kekuatan Password":
        st.header("🔍 Cek Kekuatan Password")
        password = st.text_input("Masukkan password untuk dicek", type="password")
        if password:
            with st.spinner("Menganalisis password..."):
                time.sleep(1)
            if password.lower() in indo_common:
                st.error("⚠️ Password ini sangat umum di Indonesia – segera ganti!")

            result = zxcvbn(password)
            score = result['score']
            crack_time_en = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
            crack_time_id = translate_crack_time(crack_time_en)

            st.write(f"**Skor Kekuatan (0–4)**: {score}/4")

            if score == 0:
                st.error("🛑 Sangat Lemah")
            elif score == 1:
                st.error("🛑 Lemah")
            elif score == 2:
                st.warning("⚠️ Sedang")
            elif score == 3:
                st.success("✅ Kuat")
            else:
                st.success("🛡️ Sangat Kuat!")

            st.info(f"**Estimasi zxcvbn**: {crack_time_id}")

            def gpu_crack_time(length, charset=95):
                guesses = charset ** length
                seconds = guesses / 1e9
                if seconds < 60:
                    return f"{seconds:.2f} detik"
                elif seconds < 3600:
                    return f"{seconds/60:.2f} menit"
                elif seconds < 86400:
                    return f"{seconds/3600:.2f} jam"
                elif seconds < 31536000:
                    return f"{seconds/86400:.2f} hari"
                else:
                    return f"{seconds/31536000:.2f} tahun"

            gpu_time = gpu_crack_time(len(password))
            st.warning(f"**Estimasi GPU Modern**: {gpu_time}")

            warning = result['feedback']['warning']
            suggestions = result['feedback']['suggestions']
            if warning:
                st.write(f"**Peringatan**: {warning}")
            if suggestions:
                st.write("**Saran perbaikan**:")
                for s in suggestions:
                    st.write(f"- {s}")

    else:
        st.header("🔑 Generate Password Kuat")
        generate_mode = st.selectbox("Pilih Tipe Password", [
            "Otomatis (Huruf, Angka, Simbol – Paling Aman)",
            "Benar-benar Random (Hanya Karakter Acak)",
            "Berbasis Kata (Passphrase – Mudah Diingat)"
        ])

        if "Berbasis Kata" in generate_mode:
            word_count = st.slider("Jumlah kata", 2, 8, 4)
            separator = st.text_input("Pemisah kata (kosongkan untuk tersambung)", value="-")
        else:
            length = st.slider("Panjang password", 8, 32, 16)

        if st.button("Generate Password Baru", type="primary", use_container_width=True):
            with st.spinner("Membuat password kuat..."):
                time.sleep(1.5)

            new_password = generate_password(
                generate_mode,
                length if "Berbasis Kata" not in generate_mode else None,
                word_count if "Berbasis Kata" in generate_mode else None,
                separator if "Berbasis Kata" in generate_mode else None
            )

            st.balloons()
            st.success(f"**Password baru**: `{new_password}`")

            key, encrypted = encrypt_password(new_password)

            st.write("**Kunci enkripsi** (simpan aman!):")
            st.code(key)
            st.write("**Password terenkripsi (AES-256)**:")
            st.code(encrypted)

            st.session_state.history.append({
                "no": len(st.session_state.history) + 1,
                "hint": "*****" + new_password[-4:],
                "type": generate_mode.split(" (")[0],
                "encrypted": encrypted
            })

    if st.session_state.history:
        st.markdown("### 📜 Riwayat Generate Password")
        if st.button("🗑️ Hapus Semua Riwayat"):
            st.session_state.history = []
            st.success("Riwayat berhasil dihapus!")
            st.rerun()

        for i in range(len(st.session_state.history)-1, -1, -1):
            item = st.session_state.history[i]
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"{item['no']}. [{item['type']}] Hint: {item['hint']} | Enkripsi: {item['encrypted'][:50]}...")
            with col2:
                if st.button("Hapus", key=f"del_{i}"):
                    st.session_state.history.pop(i)
                    for j in range(len(st.session_state.history)):
                        st.session_state.history[j]['no'] = j + 1
                    st.rerun()

else:
    st.info("👈 Silakan login di sidebar untuk mengakses fitur.")
    st.markdown("### Selamat datang di PassGuard!")
    st.markdown("Aplikasi ini membantu Anda membuat dan memeriksa password aman menggunakan teknologi zxcvbn dan enkripsi AES-256.")

st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) 

bisakah kamu rapikan code nya sekaligus pisah menjadi bebrapa file agar mudah