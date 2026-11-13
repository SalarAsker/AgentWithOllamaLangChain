"""AI Future Lab 2035 — Öppet hus, svensk Streamlit-demo."""
from pathlib import Path
import base64
import html
import streamlit as st
from careers import CAREERS, INTEREST_MAP, select_career
from ai_engine import generate, MODEL, OLLAMA_URL

BASE = Path(__file__).resolve().parent
st.set_page_config(page_title="AI Future Lab 2035", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap');
html,body,[class*="css"],.stApp {font-family:'Outfit',sans-serif}
.stApp {background: radial-gradient(ellipse at 15% 5%,#20214e 0%,transparent 42%),radial-gradient(ellipse at 90% 30%,#162d46 0%,transparent 35%),#080c1d;color:#eef3ff}
.block-container {max-width:1100px;padding-top:1.4rem;padding-bottom:4rem}
header[data-testid="stHeader"] {background:transparent}
h1,h2,h3,p {color:#eef3ff}
.hero {text-align:center;padding:2.1rem 1rem 1.5rem}
.eyebrow {display:inline-block;border:1px solid #5367a0;border-radius:999px;background:#182447;padding:8px 18px;color:#9ceeff;font-size:.84rem;letter-spacing:2px;font-weight:800}
.hero h1 {font-size:clamp(2.7rem,7vw,5.5rem);line-height:1.05;margin:20px 0 12px;font-weight:900;background:linear-gradient(90deg,#61e6ff,#b994ff,#ff8bc8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p {font-size:1.2rem;color:#b7c6e4;max-width:700px;margin:auto}
.glass {background:linear-gradient(130deg,rgba(31,45,85,.94),rgba(19,26,53,.94));border:1px solid #3c4d7c;border-radius:25px;padding:24px;margin-bottom:16px;box-shadow:0 15px 40px #0003}
.section-title {font-size:1.4rem;font-weight:800;margin:8px 0 14px}
.small-note {color:#9eafcf;font-size:.85rem;text-align:center;margin-top:18px}
.stButton>button[kind="primary"] {background:linear-gradient(100deg,#02c8f8,#7966f5,#db5bcb);border:0;color:white;border-radius:16px;font-size:1.1rem;font-weight:800;padding:.85rem 1.5rem;box-shadow:0 7px 26px #5e59e55c}
.stButton>button {border-radius:14px;border-color:#536394;color:#f2f5ff;background:#1d2a4d}
div[data-baseweb="select"]>div, .stTextInput input {background:#172341!important;color:white!important;border:1px solid #425783!important;border-radius:13px!important}
label,div[data-testid="stWidgetLabel"] p {color:#dce8ff!important;font-weight:600!important}
.result-name {font-size:clamp(2rem,4vw,3.4rem);font-weight:900;line-height:1.12;margin:8px 0;background:linear-gradient(90deg,#7beaff,#ff95e3);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tag {color:#7fe8f7;letter-spacing:2px;font-size:.78rem;font-weight:800}
.result-copy {font-size:1.12rem;line-height:1.65;color:#e0e9ff}
.info-card {border:1px solid #3c507e;background:#162345;border-radius:18px;padding:19px;margin:12px 0;min-height:125px}
.info-card b {color:#8beaff;font-size:1rem}
.info-card p {color:#e5ecff;margin:8px 0 0}
.step {text-align:center;background:#142040;border:1px solid #354b79;border-radius:16px;padding:12px;color:#c5d7ff;font-weight:600}
img.hero-image {width:100%;border-radius:22px;border:1px solid #536294;box-shadow:0 16px 42px #0006}
div[data-testid="stAlert"] {border-radius:14px}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
if "round" not in st.session_state:
    st.session_state.round = 0

with st.sidebar:
    st.header("⚙️ Inställningar")
    mode = st.radio("Körläge", ["Auto (AI + reserv)", "Demoläge (alltid snabbt)"], index=0, help="Auto försöker med Ollama och visar ett färdigt svar om AI inte fungerar.")
    server_url = st.text_input("Ollama-server (nätverk)", value=OLLAMA_URL)
    model = st.text_input("Ollama-modell på servern", value=MODEL)
    st.caption("AI körs på nätverksservern, inte på din laptop. Båda enheterna måste vara på samma nätverk.")
    if st.button("🔄 Nollställ besökare", use_container_width=True):
        st.session_state.result = None
        st.session_state.round = 0
        st.rerun()

st.markdown('''<div class="hero"><h1>AI FUTURE LAB <span style="white-space:nowrap">2035 🚀</span></h1><p>Vilket fantastiskt framtidsjobb passar din fantasi? Välj tre saker om dig själv och låt AI skapa ditt äventyr!</p></div>''', unsafe_allow_html=True)

# c1,c2,c3=st.columns(3)
# for col,txt in zip((c1,c2,c3),("🎯 1. Välj dina intressen","🧠 2. AI skapar din framtid","✨ 3. Upptäck ditt uppdrag")):
#     col.markdown(f'<div class="step">{txt}</div>',unsafe_allow_html=True)
# st.write("")

left,right=st.columns([1.05,.95],gap="large")
with left:
    st.markdown('<div class="section-title">🌟 Din framtid börjar här</div>',unsafe_allow_html=True)
    name=st.text_input("Vad heter du? (frivilligt)",placeholder="Ditt förnamn",max_chars=24)
    interest=st.selectbox("❤️ Vad tycker du är roligast?",list(INTEREST_MAP.keys()))
    strength=st.selectbox("💪 Vilken superkraft väljer du?",["Att vara kreativ","Att lösa problem","Att hjälpa andra","Att samarbeta","Att upptäcka nya saker","Att bygga och skapa"])
    adventure=st.selectbox("🌍 Vilket äventyr lockar mest?",["Utforska det okända","Uppfinna något nytt","Göra världen bättre","Skapa en egen värld","Lösa ett stort mysterium"])
    st.write("")
    launch=st.button("🚀 UPPTÄCK MIN FRAMTID!",type="primary",use_container_width=True)
    st.markdown('<div class="small-note">🔒 Inga svar sparas. Ett lekfullt AI-äventyr – inte ett riktigt karriärtest.</div>',unsafe_allow_html=True)
with right:
    if st.session_state.result is None:
        st.image(str(BASE/"assets"/"cover.png"),use_container_width=True)
        st.markdown('<div class="glass" style="text-align:center"><div style="font-size:1.6rem;font-weight:800">✨ Din framtid väntar!</div><p style="color:#b5c6e9">Tre snabba val. En oväntad framtid. Oändliga möjligheter.</p></div>',unsafe_allow_html=True)
    else:
        data=st.session_state.result
        career=CAREERS[data["career_id"]]
        st.image(str(BASE/"assets"/(data["career_id"]+".png")),use_container_width=True)
        st.markdown(f'<div class="tag">✦ DIN FRAMTID ÅR 2035 · {html.escape(career["category"].upper())}</div><div class="result-name">{html.escape(career["icon"]+" "+data["title"])}</div><div class="result-copy">{html.escape(data["story"])}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="info-card"><b>💻 DIN PROGRAMMERINGSKRAFT</b><p>{html.escape(data["programming"])}</p></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="info-card"><b>🎯 DITT FÖRSTA UPPDRAG</b><p>{html.escape(data["mission"])}</p></div>',unsafe_allow_html=True)
        st.caption("⚡ "+st.session_state.get("source", ""))
        if st.button("🔁 Prova en annan framtid",use_container_width=True):
            st.session_state.round+=1
            st.session_state.result=None
            st.rerun()

if launch:
    career_id=select_career(interest,strength,adventure,st.session_state.round)
    with st.spinner("🪄 AI bygger din framtid..."):
        data,source=generate(career_id,name,interest,strength,adventure,model=model.strip() or MODEL,base_url=server_url.strip().rstrip("/") or OLLAMA_URL,demo=mode.startswith("Demo"))
    st.session_state.result=data
    st.session_state.source=source
    st.rerun()

st.divider()
a,b=st.columns([2,1])
with a:
    st.markdown("### 👩‍💻 Visste du att?")
    st.write("Den här appen är byggd med **Python**, **Streamlit**, **LangChain** och en lokal **AI-modell via Ollama**. Programmering kan användas till spel, robotar, appar, forskning och mycket mer!")
with b:
    st.markdown("### 🧩 Bakom kulisserna")
    st.code("Elevens val → Python → AI → Resultat",language=None)
st.markdown('<div class="small-note">AI FUTURE LAB 2035 · Skapad för Öppet hus · Alla framtidsjobb är fantasifulla exempel</div>',unsafe_allow_html=True)
