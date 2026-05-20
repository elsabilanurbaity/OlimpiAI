import streamlit as st
import pandas as pd
import numpy as np
import pickle
import io
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SELEKSI OLIMPIADE MATEMATIKA",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px;}

/* ─── Hero banner ─── */
.hero-banner {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    text-align: center;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #fff;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.6);
    margin-top: 0.5rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, #f7971e, #ffd200);
    color: #000;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 99px;
    margin-bottom: 1rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ─── Cards ─── */
.glass-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 18px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(8px);
}
.section-title {
    color: #fff;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ─── Inputs ─── */
.stNumberInput input, .stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stNumberInput label, .stTextInput label, .stFileUploader label {
    color: rgba(255,255,255,0.8) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}
div[data-testid="stSlider"] label {
    color: rgba(255,255,255,0.8) !important;
}

/* ─── Buttons ─── */
.stButton > button {
    background: linear-gradient(135deg, #f7971e, #ffd200) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(247,151,30,0.4) !important;
}

/* ─── Download button ─── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #11998e, #38ef7d) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
}

/* ─── Result cards ─── */
.result-siap {
    background: linear-gradient(135deg, rgba(56,239,125,0.15), rgba(17,153,142,0.15));
    border: 1.5px solid #38ef7d;
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
}
.result-potensial {
    background: linear-gradient(135deg, rgba(247,151,30,0.15), rgba(255,210,0,0.15));
    border: 1.5px solid #ffd200;
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
}
.result-tidaksiap {
    background: linear-gradient(135deg, rgba(255,75,75,0.15), rgba(200,50,50,0.15));
    border: 1.5px solid #ff4b4b;
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
}
.result-status {
    font-size: 1.8rem;
    font-weight: 800;
    color: #fff;
    margin: 0.5rem 0;
}
.result-emoji {
    font-size: 3rem;
    line-height: 1;
}
.result-prob {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.65);
    margin-top: 0.5rem;
}

/* ─── Score bars ─── */
.score-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.7rem;
    gap: 10px;
}
.score-label {
    color: rgba(255,255,255,0.75);
    font-size: 0.82rem;
    font-weight: 500;
    min-width: 160px;
}
.score-bar-bg {
    flex: 1;
    background: rgba(255,255,255,0.1);
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
}
.score-val {
    color: #fff;
    font-size: 0.82rem;
    font-weight: 700;
    min-width: 38px;
    text-align: right;
}

/* ─── Recommendation box ─── */
.rec-box {
    background: rgba(255,255,255,0.05);
    border-left: 3px solid #ffd200;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    color: rgba(255,255,255,0.85);
    font-size: 0.9rem;
    line-height: 1.5;
}
.review-text {
    color: rgba(255,255,255,0.8);
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 1rem;
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.12);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    color: rgba(255,255,255,0.6);
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #f7971e, #ffd200) !important;
    color: #000 !important;
}

/* ─── Info boxes ─── */
.info-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
.info-chip {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    flex: 1;
    text-align: center;
}
.info-chip-val {
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffd200;
}
.info-chip-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.55);
    margin-top: 2px;
}

/* ─── Dataframe ─── */
.stDataFrame {border-radius: 12px; overflow: hidden;}
[data-testid="stDataFrame"] {border-radius: 12px;}

/* ─── Uploader ─── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border: 1.5px dashed rgba(255,255,255,0.2);
    border-radius: 14px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

FEATURES = ["aljabar", "geometri", "bilangan", "data_ketidakpastian", "menalar", "literasi"]
LABELS = {0: "Tidak Siap", 1: "Potensial", 2: "Siap Olimpiade"}
EMOJIS = {0: "❌", 1: "⚡", 2: "🏆"}
CSS_CLASSES = {0: "result-tidaksiap", 1: "result-potensial", 2: "result-siap"}


# ── Helper: predict single ─────────────────────────────────────────────────────
def predict_single(scores: dict):
    X = np.array([[scores[f] for f in FEATURES]])
    X_s = scaler.transform(X)
    label = model.predict(X_s)[0]
    proba = model.predict_proba(X_s)[0]
    return int(label), proba


def get_review(label, scores, avg):
    alj, geo, bil, dat, men, lit = [scores[f] for f in FEATURES]
    weak = [n for n, v in zip(
        ["Aljabar", "Geometri", "Bilangan", "Data & Ketidakpastian", "Menalar", "Literasi"],
        [alj, geo, bil, dat, men, lit]) if v < 60]
    strong = [n for n, v in zip(
        ["Aljabar", "Geometri", "Bilangan", "Data & Ketidakpastian", "Menalar", "Literasi"],
        [alj, geo, bil, dat, men, lit]) if v >= 80]

    if label == 2:
        review = (f"Siswa ini menunjukkan performa yang sangat baik dengan rata-rata skor {avg:.1f}. "
                  f"Kemampuan di bidang {', '.join(strong) if strong else 'semua aspek'} "
                  f"sudah memenuhi standar olimpiade. Siswa layak untuk diikutsertakan dalam seleksi olimpiade matematika.")
    elif label == 1:
        review = (f"Siswa ini memiliki potensi yang cukup baik dengan rata-rata skor {avg:.1f}. "
                  f"{'Terdapat keunggulan di bidang ' + ', '.join(strong) + '.' if strong else ''} "
                  f"{'Namun masih perlu penguatan di bidang ' + ', '.join(weak) + '.' if weak else ''} "
                  f"Dengan latihan yang tepat, siswa ini berpotensi meningkat ke level Siap Olimpiade.")
    else:
        review = (f"Siswa ini belum mencapai standar minimum dengan rata-rata skor {avg:.1f}. "
                  f"{'Bidang yang perlu perhatian khusus: ' + ', '.join(weak) + '.' if weak else ''} "
                  f"Dibutuhkan program belajar yang intensif dan terstruktur untuk meningkatkan kemampuan secara menyeluruh.")
    return review, weak, strong


def get_recommendations(label, scores, weak):
    recs = []
    tips_map = {
        "Aljabar": "Latih soal persamaan, pertidaksamaan, dan pola bilangan secara rutin.",
        "Geometri": "Perbanyak latihan soal bangun ruang, kesebangunan, dan transformasi geometri.",
        "Bilangan": "Fokus pada operasi bilangan, FPB, KPK, dan bilangan prima.",
        "Data & Ketidakpastian": "Pelajari statistika dasar, peluang, dan interpretasi data.",
        "Menalar": "Tingkatkan kemampuan logika dengan soal pola, analogi, dan deduksi.",
        "Literasi": "Latih membaca soal matematika kontekstual dan merumuskan solusi.",
    }
    if label == 2:
        recs = [
            "✅ Daftarkan ke seleksi olimpiade tingkat kabupaten/kota.",
            "🎯 Ikuti program pelatihan intensif olimpiade matematika.",
            "📚 Pelajari soal-soal olimpiade tingkat nasional (OSN) tahun sebelumnya.",
            "🤝 Bergabung dengan komunitas atau klub matematika untuk meningkatkan wawasan.",
        ]
    elif label == 1:
        recs = ["⚡ Ikuti program bimbingan belajar matematika terstruktur."]
        for w in weak:
            if w in tips_map:
                recs.append(f"📌 {w}: {tips_map[w]}")
        recs.append("🔄 Evaluasi ulang dalam 1–2 bulan setelah menjalani program peningkatan.")
    else:
        recs = ["📖 Mulai dari materi dasar matematika yang sesuai kurikulum."]
        for w in weak:
            if w in tips_map:
                recs.append(f"📌 {w}: {tips_map[w]}")
        recs += [
            "👨‍🏫 Konsultasikan dengan guru untuk mendapatkan program remedial yang sesuai.",
            "🗓️ Buat jadwal belajar harian yang konsisten minimal 1 jam per hari.",
        ]
    return recs


def render_score_bars(scores):
    labels_map = {
        "aljabar": "Numerasi Aljabar",
        "geometri": "Numerasi Geometri",
        "bilangan": "Numerasi Bilangan",
        "data_ketidakpastian": "Data & Ketidakpastian",
        "menalar": "Menalar",
        "literasi": "Literasi",
    }
    color_map = {
        "aljabar": "#f7971e",
        "geometri": "#38ef7d",
        "bilangan": "#4facfe",
        "data_ketidakpastian": "#a18cd1",
        "menalar": "#ffd200",
        "literasi": "#f093fb",
    }
    html = ""
    for key in FEATURES:
        val = scores[key]
        pct = min(val, 100)
        color = color_map[key]
        html += f"""
        <div class="score-row">
            <div class="score-label">{labels_map[key]}</div>
            <div class="score-bar-bg">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:99px;transition:width 0.5s"></div>
            </div>
            <div class="score-val">{val:.1f}</div>
        </div>"""
    st.markdown(html, unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🔬 Data Mining · Klasifikasi · Random Forest</div>
    <div class="hero-title">🏆 Sistem Seleksi Olimpiade Matematika</div>
    <div class="hero-subtitle">Identifikasi kesiapan siswa berdasarkan 6 dimensi kemampuan numerasi & literasi matematika</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["👤  Input Satu Siswa", "📂  Upload File Excel"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: INPUT SATU SISWA
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_form, col_result = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Data Siswa</div>', unsafe_allow_html=True)
        nama = st.text_input("Nama Siswa", placeholder="Contoh: Budi Santoso", key="nama")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Skor Kemampuan (0–100)</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            alj = st.number_input("🔢 Numerasi Aljabar", 0.0, 100.0, 65.0, 0.1, key="alj")
            bil = st.number_input("🔣 Numerasi Bilangan", 0.0, 100.0, 65.0, 0.1, key="bil")
            men = st.number_input("🧠 Menalar", 0.0, 100.0, 65.0, 0.1, key="men")
        with c2:
            geo = st.number_input("📐 Numerasi Geometri", 0.0, 100.0, 65.0, 0.1, key="geo")
            dat = st.number_input("📈 Data & Ketidakpastian", 0.0, 100.0, 65.0, 0.1, key="dat")
            lit = st.number_input("📖 Literasi", 0.0, 100.0, 65.0, 0.1, key="lit")

        st.markdown('</div>', unsafe_allow_html=True)

        predict_btn = st.button("🔍 Analisis Kesiapan Siswa", key="btn_single")

    with col_result:
        if predict_btn:
            scores = {
                "aljabar": alj, "geometri": geo, "bilangan": bil,
                "data_ketidakpastian": dat, "menalar": men, "literasi": lit,
            }
            avg = np.mean(list(scores.values()))
            label, proba = predict_single(scores)
            review, weak, strong = get_review(label, scores, avg)
            recs = get_recommendations(label, scores, weak)

            # Result card
            css_class = CSS_CLASSES[label]
            emoji = EMOJIS[label]
            status = LABELS[label]
            conf = proba[label] * 100

            display_name = nama if nama.strip() else "Siswa"
            st.markdown(f"""
            <div class="{css_class}">
                <div class="result-emoji">{emoji}</div>
                <div style="color:rgba(255,255,255,0.7);font-size:0.9rem;margin-top:0.5rem">{display_name}</div>
                <div class="result-status">{status}</div>
                <div class="result-prob">Tingkat keyakinan: {conf:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

            # Info chips
            st.markdown(f"""
            <div class="info-row" style="margin-top:1rem">
                <div class="info-chip">
                    <div class="info-chip-val">{avg:.1f}</div>
                    <div class="info-chip-label">Rata-rata Skor</div>
                </div>
                <div class="info-chip">
                    <div class="info-chip-val">{len(strong)}/6</div>
                    <div class="info-chip-label">Aspek Unggul (≥80)</div>
                </div>
                <div class="info-chip">
                    <div class="info-chip-val">{len(weak)}/6</div>
                    <div class="info-chip-label">Aspek Lemah (<60)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Score bars
            st.markdown('<div class="glass-card" style="margin-top:0.5rem">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Profil Kemampuan</div>', unsafe_allow_html=True)
            render_score_bars(scores)
            st.markdown('</div>', unsafe_allow_html=True)

            # Review
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📝 Review</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="review-text">{review}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Recommendations
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💡 Rekomendasi & Saran</div>', unsafe_allow_html=True)
            for r in recs:
                st.markdown(f'<div class="rec-box">{r}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:3rem 2rem;margin-top:0">
                <div style="font-size:3rem;margin-bottom:1rem">📊</div>
                <div style="color:rgba(255,255,255,0.5);font-size:0.95rem">
                    Masukkan data skor siswa di sebelah kiri,<br>lalu klik tombol <b style="color:#ffd200">Analisis Kesiapan Siswa</b>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: UPLOAD FILE EXCEL
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📂 Upload File Excel Siswa</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:rgba(255,255,255,0.55);font-size:0.85rem;margin-bottom:1rem">
    Format kolom yang diperlukan: <b style="color:#ffd200">Nama</b> (opsional), 
    <b style="color:#ffd200">NUM_ALJ</b>, <b style="color:#ffd200">NUM_GEO</b>, 
    <b style="color:#ffd200">NUM_BIL</b>, <b style="color:#ffd200">NUM_DAT</b>, 
    <b style="color:#ffd200">NUM_L3</b>, <b style="color:#ffd200">LIT</b>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        try:
            df_up = pd.read_excel(uploaded_file)
            # Normalize column names
            col_map = {}
            for c in df_up.columns:
                cu = c.upper().strip()
                if cu in ["NUM_ALJ", "ALJABAR", "NUM_ALJABAR"]:
                    col_map[c] = "aljabar"
                elif cu in ["NUM_GEO", "GEOMETRI", "NUM_GEOMETRI"]:
                    col_map[c] = "geometri"
                elif cu in ["NUM_BIL", "BILANGAN", "NUM_BILANGAN"]:
                    col_map[c] = "bilangan"
                elif cu in ["NUM_DAT", "DATA", "NUM_DATA", "DATA_KETIDAKPASTIAN"]:
                    col_map[c] = "data_ketidakpastian"
                elif cu in ["NUM_L3", "MENALAR", "NUM_MENALAR", "NALAR"]:
                    col_map[c] = "menalar"
                elif cu in ["LIT", "LITERASI"]:
                    col_map[c] = "literasi"
                elif cu in ["NAMA", "NAME", "SISWA"]:
                    col_map[c] = "nama"
            df_up = df_up.rename(columns=col_map)

            missing = [f for f in FEATURES if f not in df_up.columns]
            if missing:
                st.error(f"❌ Kolom tidak ditemukan: {', '.join(missing)}")
            else:
                df_valid = df_up.dropna(subset=FEATURES).copy()
                n_total = len(df_up)
                n_valid = len(df_valid)

                st.markdown(f"""
                <div class="info-row">
                    <div class="info-chip"><div class="info-chip-val">{n_total}</div><div class="info-chip-label">Total Data</div></div>
                    <div class="info-chip"><div class="info-chip-val">{n_valid}</div><div class="info-chip-label">Data Valid</div></div>
                    <div class="info-chip"><div class="info-chip-val">{n_total - n_valid}</div><div class="info-chip-label">Data Kosong</div></div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🚀 Proses Semua Data", key="btn_batch"):
                    with st.spinner("Menganalisis data siswa..."):
                        X_batch = df_valid[FEATURES].values
                        X_scaled_batch = scaler.transform(X_batch)
                        preds = model.predict(X_scaled_batch)
                        probas = model.predict_proba(X_scaled_batch)

                        df_valid = df_valid.copy()
                        df_valid["Status_Kesiapan"] = [LABELS[p] for p in preds]
                        df_valid["Keyakinan_%"] = [round(probas[i][preds[i]] * 100, 1) for i in range(len(preds))]
                        df_valid["Rata_rata_Skor"] = df_valid[FEATURES].mean(axis=1).round(2)

                        def quick_review(row):
                            avg = row["Rata_rata_Skor"]
                            lbl = [k for k, v in LABELS.items() if v == row["Status_Kesiapan"]][0]
                            weak = [n for n, c in zip(
                                ["Aljabar","Geometri","Bilangan","Data & Ketidakpastian","Menalar","Literasi"],
                                FEATURES) if row[c] < 60]
                            if lbl == 2:
                                return f"Performa sangat baik (avg {avg:.1f}). Layak seleksi olimpiade."
                            elif lbl == 1:
                                w = ', '.join(weak) if weak else "semua aspek cukup"
                                return f"Berpotensi (avg {avg:.1f}). Perkuat: {w}."
                            else:
                                w = ', '.join(weak) if weak else "semua aspek"
                                return f"Belum siap (avg {avg:.1f}). Fokus perbaiki: {w}."

                        df_valid["Review"] = df_valid.apply(quick_review, axis=1)

                    # Summary stats
                    vc = pd.Series(preds).value_counts()
                    siap = vc.get(2, 0)
                    pot = vc.get(1, 0)
                    tidak = vc.get(0, 0)

                    st.markdown(f"""
                    <div class="glass-card">
                        <div class="section-title">📊 Ringkasan Hasil Analisis</div>
                        <div class="info-row">
                            <div class="info-chip">
                                <div class="info-chip-val" style="color:#38ef7d">{siap}</div>
                                <div class="info-chip-label">🏆 Siap Olimpiade</div>
                            </div>
                            <div class="info-chip">
                                <div class="info-chip-val" style="color:#ffd200">{pot}</div>
                                <div class="info-chip-label">⚡ Potensial</div>
                            </div>
                            <div class="info-chip">
                                <div class="info-chip-val" style="color:#ff4b4b">{tidak}</div>
                                <div class="info-chip-label">❌ Tidak Siap</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Preview table
                    cols_show = (["nama"] if "nama" in df_valid.columns else []) + \
                                FEATURES + ["Status_Kesiapan", "Keyakinan_%", "Rata_rata_Skor", "Review"]
                    df_show = df_valid[[c for c in cols_show if c in df_valid.columns]]

                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">📋 Preview Hasil (10 baris pertama)</div>', unsafe_allow_html=True)
                    st.dataframe(
                        df_show.head(10).rename(columns={
                            "aljabar": "Aljabar", "geometri": "Geometri",
                            "bilangan": "Bilangan", "data_ketidakpastian": "Data & KT",
                            "menalar": "Menalar", "literasi": "Literasi",
                            "nama": "Nama", "Rata_rata_Skor": "Rata-rata",
                        }),
                        use_container_width=True, hide_index=True,
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df_out = df_show.rename(columns={
                            "aljabar": "Skor Aljabar", "geometri": "Skor Geometri",
                            "bilangan": "Skor Bilangan", "data_ketidakpastian": "Skor Data & KT",
                            "menalar": "Skor Menalar", "literasi": "Skor Literasi",
                            "nama": "Nama Siswa", "Rata_rata_Skor": "Rata-rata Skor",
                            "Status_Kesiapan": "Status Kesiapan Olimpiade",
                            "Keyakinan_%": "Tingkat Keyakinan (%)",
                        })
                        df_out.to_excel(writer, index=False, sheet_name="Hasil Seleksi")

                        # Summary sheet
                        df_summary = pd.DataFrame({
                            "Status": ["Siap Olimpiade", "Potensial", "Tidak Siap", "TOTAL"],
                            "Jumlah Siswa": [siap, pot, tidak, n_valid],
                            "Persentase (%)": [
                                round(siap/n_valid*100, 1),
                                round(pot/n_valid*100, 1),
                                round(tidak/n_valid*100, 1), 100.0
                            ],
                        })
                        df_summary.to_excel(writer, index=False, sheet_name="Ringkasan")

                    fname = f"Hasil_Seleksi_Olimpiade_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                    st.download_button(
                        label="⬇️ Download Hasil Excel",
                        data=output.getvalue(),
                        file_name=fname,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_btn",
                    )

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan membaca file: {e}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding:1rem;color:rgba(255,255,255,0.25);font-size:0.78rem">
    Sistem Seleksi Olimpiade Matematika · Data Mining · Pendidikan Matematika<br>
    Metode: Random Forest Classifier · Akurasi: 99%
</div>
""", unsafe_allow_html=True)
