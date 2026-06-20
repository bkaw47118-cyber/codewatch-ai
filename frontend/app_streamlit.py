import streamlit as st
import requests

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="CodeWatch AI",
    page_icon="assets/logo.png" if False else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS — DASHBOARD PROFESSIONNEL
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background-color: #0f1117;
    color: #e2e8f0;
}

/* Cacher le header Streamlit */
#MainMenu, header, footer { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #141920;
    border-right: 1px solid #1e2530;
}

section[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

/* Header principal */
.cw-header {
    padding: 2rem 0 1.5rem 0;
    border-bottom: 1px solid #1e2530;
    margin-bottom: 2rem;
}

.cw-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.cw-logo-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.cw-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.5px;
}

.cw-version {
    font-size: 0.7rem;
    color: #3b82f6;
    background: #1e3a5f;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
}

/* Cartes métriques */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: #141920;
    border: 1px solid #1e2530;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}

.metric-card.total::before { background: #ef4444; }
.metric-card.pylint::before { background: #f59e0b; }
.metric-card.bandit::before { background: #ef4444; }
.metric-card.semgrep::before { background: #8b5cf6; }

.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.metric-card.total .metric-value { color: #ef4444; }
.metric-card.pylint .metric-value { color: #f59e0b; }
.metric-card.bandit .metric-value { color: #ef4444; }
.metric-card.semgrep .metric-value { color: #8b5cf6; }

.metric-label {
    font-size: 0.8rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-sub {
    font-size: 0.75rem;
    color: #475569;
    margin-top: 0.4rem;
}

/* Badges sévérité */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.badge-high { background: #2d1515; color: #ef4444; border: 1px solid #ef444440; }
.badge-medium { background: #2d2010; color: #f59e0b; border: 1px solid #f59e0b40; }
.badge-low { background: #1a2535; color: #3b82f6; border: 1px solid #3b82f640; }
.badge-convention { background: #1e1e2e; color: #8b5cf6; border: 1px solid #8b5cf640; }
.badge-warning { background: #2d2010; color: #f59e0b; border: 1px solid #f59e0b40; }
.badge-error { background: #2d1515; color: #ef4444; border: 1px solid #ef444440; }

/* Issue card */
.issue-card {
    background: #141920;
    border: 1px solid #1e2530;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.issue-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #475569;
    min-width: 60px;
}

.issue-message {
    font-size: 0.85rem;
    color: #cbd5e1;
    flex: 1;
}

.issue-symbol {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #475569;
    margin-top: 3px;
}

/* Section titre */
.section-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2530;
}

/* Rapport LLM */
.report-container {
    background: #141920;
    border: 1px solid #1e2530;
    border-radius: 10px;
    padding: 1.8rem;
    margin-top: 1rem;
    line-height: 1.7;
}

.report-container h3 {
    color: #f1f5f9;
    font-size: 1rem;
    font-weight: 600;
    margin-top: 1.2rem;
}

.report-container p {
    color: #94a3b8;
    font-size: 0.9rem;
}

/* Upload zone */
.upload-zone {
    border: 2px dashed #1e2530;
    border-radius: 12px;
    padding: 3rem;
    text-align: center;
    background: #141920;
    transition: border-color 0.2s;
}

/* Status bar */
.status-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.6rem 1rem;
    background: #141920;
    border: 1px solid #1e2530;
    border-radius: 8px;
    font-size: 0.8rem;
    color: #64748b;
    margin-bottom: 1.5rem;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 6px #22c55e;
}

/* Success/Error banners */
.banner-success {
    background: #0d2818;
    border: 1px solid #16a34a40;
    border-left: 3px solid #16a34a;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #4ade80;
    margin: 1rem 0;
}

.banner-error {
    background: #2d1515;
    border: 1px solid #ef444440;
    border-left: 3px solid #ef4444;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #f87171;
    margin: 1rem 0;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 0.8rem !important;
    color: #64748b !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #f1f5f9 !important;
}

/* Score */
.score-container {
    background: #141920;
    border: 1px solid #1e2530;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.score-number {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
}

.score-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
}

/* Divider */



hr { border-color: #1e2530 !important; }
/* Forcer le style de la zone upload */
.stFileUploader {
    background: #141920 !important;
    border: 1px solid #1e2530 !important;
    border-radius: 10px !important;
}

.stFileUploader > div {
    background: #141920 !important;
    border: 2px dashed #1e2530 !important;
    border-radius: 10px !important;
}

.stFileUploader label {
    color: #475569 !important;
    font-size: 0.85rem !important;
}

/* Input sidebar */
.stTextInput > div > div {
    background: #1e2530 !important;
    border-color: #2d3748 !important;
    color: #94a3b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #3b82f6 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### CodeWatch AI")
    st.markdown("---")
    api_url = st.text_input(
        "API Endpoint",
        value="http://5.78.97.46:8000",
        label_visibility="visible"
    )
    st.markdown("---")
    st.markdown("**Pipeline d'analyse**")
    st.markdown("""
<div style="font-size:0.82rem; color:#475569; line-height:2;">
    Pylint 4.0 &nbsp;&nbsp; Qualité<br>
    Bandit 1.9 &nbsp;&nbsp; Sécurité<br>
    Semgrep 1.x &nbsp; Patterns<br>
    Qwen2.5-Coder 14B &nbsp; LLM
</div>
""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
<div style="font-size:0.75rem; color:#334155; line-height:1.8;">
    ENPO-MA — 2026<br>
    Kawther BOUZEROUATA<br>
    Option IMSI
</div>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="cw-header">
    <div class="cw-logo">
        <div class="cw-logo-icon">&#9673;</div>
        <div>
            <span class="cw-title">CodeWatch AI</span>
            <span class="cw-version">v1.0.0</span>
        </div>
    </div>
    <div style="margin-top:0.5rem; font-size:0.85rem; color:#475569;">
        Plateforme de revue automatique de code Python — Analyse statique hybride
    </div>
</div>
""", unsafe_allow_html=True)

# Status bar
st.markdown("""
<div class="status-bar">
    <div class="status-dot"></div>
    Système opérationnel &nbsp;|&nbsp; Qwen2.5-Coder 14B &nbsp;|&nbsp; Pylint · Bandit · Semgrep
</div>
""", unsafe_allow_html=True)

# ============================================================
# UPLOAD
# ============================================================
col_upload, col_info = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Fichier Python à analyser",
        type=["py"],
        label_visibility="visible"
    )

with col_info:
    st.markdown("""
<div style="background:#141920; border:1px solid #1e2530; border-radius:10px; padding:1rem; font-size:0.8rem; color:#475569; line-height:1.9; margin-top:1.8rem;">
    <strong style="color:#94a3b8;">Fonctionnement</strong><br>
    1. Déposez un fichier .py<br>
    2. Lancement SAST automatique<br>
    3. Enrichissement par LLM<br>
    4. Rapport structuré généré
</div>
""", unsafe_allow_html=True)

# ============================================================
# ANALYSE
# ============================================================
if uploaded_file is not None:
    st.markdown("---")
    col_btn, col_name = st.columns([1, 3])
    with col_btn:
        run = st.button("Lancer l'analyse", use_container_width=True)
    with col_name:
        st.markdown(f"""
<div style="padding-top:0.6rem; font-size:0.82rem; color:#475569;">
    Fichier sélectionné : <span style="color:#94a3b8; font-family:'JetBrains Mono',monospace;">{uploaded_file.name}</span>
    &nbsp;·&nbsp; {uploaded_file.size} bytes
</div>
""", unsafe_allow_html=True)

    if run:
        with st.spinner("Analyse en cours..."):
            try:
                response = requests.post(
                    f"{api_url}/analyze",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")},
                    timeout=180
                )

                if response.status_code == 200:
                    data = response.json()
                    sast = data["sast_results"]
                    llm_report = data["llm_report"]
                    summary = sast["summary"]

                    st.markdown('<div class="banner-success">Analyse terminée avec succès.</div>', unsafe_allow_html=True)

                    # MÉTRIQUES
                    st.markdown('<div class="section-title">Résultats de l\'analyse statique</div>', unsafe_allow_html=True)
                    st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card total">
        <div class="metric-value">{sast['total_issues']}</div>
        <div class="metric-label">Total Issues</div>
        <div class="metric-sub">tous outils confondus</div>
    </div>
    <div class="metric-card pylint">
        <div class="metric-value">{summary['pylint_count']}</div>
        <div class="metric-label">Pylint</div>
        <div class="metric-sub">qualité · conventions</div>
    </div>
    <div class="metric-card bandit">
        <div class="metric-value">{summary['bandit_count']}</div>
        <div class="metric-label">Bandit</div>
        <div class="metric-sub">vulnérabilités sécurité</div>
    </div>
    <div class="metric-card semgrep">
        <div class="metric-value">{summary['semgrep_count']}</div>
        <div class="metric-label">Semgrep</div>
        <div class="metric-sub">patterns dangereux</div>
    </div>
</div>
""", unsafe_allow_html=True)

                    # DÉTAILS SAST
                    st.markdown('<div class="section-title">Détail des issues par outil</div>', unsafe_allow_html=True)
                    tab1, tab2, tab3 = st.tabs(["Pylint", "Bandit", "Semgrep"])

                    with tab1:
                        if sast["pylint"]:
                            for issue in sast["pylint"]:
                                if "error" not in issue:
                                    t = issue.get("type", "")
                                    badge_class = "badge-error" if t == "error" else ("badge-warning" if t == "warning" else "badge-convention")
                                    st.markdown(f"""
<div class="issue-card">
    <div>
        <span class="badge {badge_class}">{t}</span>
        <div class="issue-line" style="margin-top:6px;">L.{issue.get('line')}</div>
    </div>
    <div>
        <div class="issue-message">{issue.get('message')}</div>
        <div class="issue-symbol">{issue.get('symbol')}</div>
    </div>
</div>
""", unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="color:#22c55e; font-size:0.85rem; padding:1rem;">Aucun problème détecté.</div>', unsafe_allow_html=True)

                    with tab2:
                        if sast["bandit"]:
                            for issue in sast["bandit"]:
                                if "error" not in issue:
                                    sev = issue.get("severity", "LOW")
                                    badge_class = "badge-high" if sev == "HIGH" else ("badge-medium" if sev == "MEDIUM" else "badge-low")
                                    st.markdown(f"""
<div class="issue-card">
    <div>
        <span class="badge {badge_class}">{sev}</span>
        <div class="issue-line" style="margin-top:6px;">L.{issue.get('line')}</div>
        <div class="issue-symbol" style="margin-top:3px;">{issue.get('confidence')}</div>
    </div>
    <div>
        <div class="issue-message">{issue.get('message')}</div>
    </div>
</div>
""", unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="color:#22c55e; font-size:0.85rem; padding:1rem;">Aucune vulnérabilité détectée.</div>', unsafe_allow_html=True)

                    with tab3:
                        if sast["semgrep"]:
                            for issue in sast["semgrep"]:
                                if "error" not in issue:
                                    st.markdown(f"""
<div class="issue-card">
    <div>
        <span class="badge badge-high">{issue.get('severity','N/A')}</span>
        <div class="issue-line" style="margin-top:6px;">L.{issue.get('line')}</div>
    </div>
    <div>
        <div class="issue-message">{issue.get('message')}</div>
    </div>
</div>
""", unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="color:#475569; font-size:0.85rem; padding:1rem;">Aucun pattern dangereux détecté.</div>', unsafe_allow_html=True)

                    # RAPPORT LLM
                    st.markdown('<div class="section-title">Rapport d\'analyse — Qwen2.5-Coder 14B</div>', unsafe_allow_html=True)
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.markdown(llm_report)
                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.markdown(f'<div class="banner-error">Erreur API : {response.status_code}</div>', unsafe_allow_html=True)

            except requests.exceptions.Timeout:
                st.markdown('<div class="banner-error">Timeout — le modèle LLM n\'a pas répondu dans le délai imparti.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="banner-error">Erreur de connexion : {str(e)}</div>', unsafe_allow_html=True)
