
import streamlit as st, json, os, random, time, math

st.set_page_config(page_title="WTF is Up?", page_icon="💬", layout="centered")

DATA_DIR = os.path.dirname(__file__)
with open(os.path.join(DATA_DIR, "content.json"), "r", encoding="utf-8") as f:
    CONTENT = json.load(f)

if "phase" not in st.session_state:
    st.session_state.phase = "welcome"
if "handle" not in st.session_state:
    st.session_state.handle = ""
if "adjective" not in st.session_state:
    st.session_state.adjective = ""
if "animal" not in st.session_state:
    st.session_state.animal = ""
if "selected_moods" not in st.session_state:
    st.session_state.selected_moods = set()
if "time_choice" not in st.session_state:
    st.session_state.time_choice = None

PRIMARY = "#AAB7F8"
ACCENT_YELLOW = "#FFFACD"
TEXT = "#333333"
BUBBLE_BG = "#E8ECFF"
BUBBLE_SELECTED = "#F7EFA6"

moods = ["anxious","sad","angry","stressed","panic","overwhelmed","lonely","sleep problems","school pressure","family conflict","bullying","sports pressure","focus","motivation","breakup","friend drama","body image","social media","rumination","worry"]

def css():
    st.markdown(f"""
        <style>
        .stApp {{
            background: {PRIMARY};
        }}
        .title h1, .title h2, .title h3, .title p {{
            color: {TEXT};
        }}
        .bubble-wrap {{
            position: relative;
            width: 100%;
            height: 520px;
            overflow: hidden;
        }}
        .bubble {{
            position: absolute;
            width: 130px;
            height: 130px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            text-align: center;
            padding: 10px;
            cursor: pointer;
            user-select: none;
            border: 2px solid rgba(0,0,0,0.05);
            box-shadow: 0 10px 18px rgba(0,0,0,0.08);
            background: {BUBBLE_BG};
            color: #3a3a3a;
            transition: transform .15s ease;
        }}
        .bubble:hover {{
            transform: scale(1.04);
        }}
        .bubble.selected {{
            background: {BUBBLE_SELECTED};
            border-color: rgba(0,0,0,0.08);
        }}
        @keyframes orbit {{
            from {{ transform: rotate(0deg) translateX(var(--radius)) rotate(0deg); }}
            to   {{ transform: rotate(360deg) translateX(var(--radius)) rotate(-360deg); }}
        }}
        .orbiter {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform-origin: center;
            animation: orbit var(--duration) linear infinite;
        }}
        .center-card {{
            background: white;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.12);
            border: 1px solid rgba(0,0,0,0.05);
        }}
        .pill {{
            display: inline-block;
            padding: 8px 14px;
            border-radius: 999px;
            background: {ACCENT_YELLOW};
            color: #333;
            font-weight: 600;
            margin: 6px 6px 0 0;
            border: 1px solid rgba(0,0,0,0.05);
        }}
        .time-grid {{
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
        }}
        .time-btn {{
            width: 100%;
            background: white;
            border: 2px solid rgba(0,0,0,0.05);
            border-radius: 12px;
            padding: 14px 10px;
            font-weight: 700;
            color: #333;
        }}
        .time-btn:hover {{
            background: {ACCENT_YELLOW};
        }}
        </style>
    """, unsafe_allow_html=True)

def recommend(tags, minutes):
    items = CONTENT["items"]
    def s(it):
        if minutes is not None and it.get("minutes", 10) > minutes: 
            return -1e9
        overlap = len(set(it.get("tags", [])) & set(tags))
        time_fit = 1.0 if it.get("minutes", 10) <= minutes else 0.0
        return overlap*2 + time_fit
    ranked = sorted(items, key=lambda x: s(x), reverse=True)
    out = [x for x in ranked if s(x) > -1e5]
    return out[:3] if out else ranked[:2]

css()


st.markdown("<div style='text-align:center;'><h2>💬 WTF is Up?</h2></div>", unsafe_allow_html=True)


if st.session_state.phase == "welcome":
    st.markdown("<div class='title'><h1>WTF is Up?</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='center-card'><h3>Welcome</h3><p>This app shares supportive, clinician-approved self-help resources for teens. It is educational and not a diagnosis or a substitute for professional care. If you are in crisis in the US, call or text 988.</p></div>", unsafe_allow_html=True)
    adjs = ["Ferocious","Curious","Gentle","Bold","Radiant","Calm","Brave","Witty","Kind","Steady","Swift","Bright"]
    animals = ["Penguin","Otter","Hawk","Dolphin","Panda","Tiger","Koala","Falcon","Fox","Seal","Heron","Lynx"]
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.adjective = st.selectbox("Pick an adjective", adjs, index=0)
    with c2:
        st.session_state.animal = st.selectbox("Pick an animal", animals, index=0)
    if st.button("Continue"):
        st.session_state.handle = f"{st.session_state.adjective} {st.session_state.animal}"
        st.session_state.phase = "mood"
        st.rerun()

elif st.session_state.phase == "mood":
    if st.button('⬅ Back'):
        st.session_state.phase = 'welcome'
        st.rerun()
    st.markdown(f"<div class='title'><h2>Hi, {st.session_state.handle}</h2><p>Pick what fits today.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='bubble-wrap'>", unsafe_allow_html=True)
    for i, m in enumerate(moods):
        radius = 160 + (i % 3)*30
        dur = 16 + (i % 5)*2
        selected = m in st.session_state.selected_moods
        st.markdown(f"<div class='orbiter' style='--radius:{radius}px; --duration:{dur}s;'>", unsafe_allow_html=True)
        k = f"toggle_{m}"
        pressed = st.button(m.title(), key=k)
        if pressed:
            if selected:
                st.session_state.selected_moods.discard(m)
            else:
                st.session_state.selected_moods.add(m)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.selected_moods:
        st.markdown("".join([f"<span class='pill'>{x}</span>" for x in st.session_state.selected_moods]), unsafe_allow_html=True)
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("Clear"):
            st.session_state.selected_moods = set()
            st.rerun()
    with c2:
        if st.button("Next", disabled=not bool(st.session_state.selected_moods)):
            st.session_state.phase = "time"
            st.rerun()

elif st.session_state.phase == "time":
    if st.button('⬅ Back'):
        st.session_state.phase = 'mood'
        st.rerun()
    st.markdown("<div class='title'><h2>How much time do you have?</h2></div>", unsafe_allow_html=True)
    times = [2,5,10,15,20]
    cols = st.columns(5)
    chosen = None
    for i, t in enumerate(times):
        with cols[i]:
            if st.button(f"{t} min", key=f"time_{t}", use_container_width=True):
                chosen = t
    if chosen:
        st.session_state.time_choice = chosen
        st.session_state.phase = "plan"
        st.rerun()

elif st.session_state.phase == "plan":
    if st.button('⬅ Back'):
        st.session_state.phase = 'time'
        st.rerun()
    st.markdown("<div class='title'><h2>Your plan</h2><p>Based on your choices.</p></div>", unsafe_allow_html=True)
    recs = recommend(list(st.session_state.selected_moods), st.session_state.time_choice or 10)
    if not recs:
        st.info("No perfect match. Here are a few safe starters.")
        recs = CONTENT["items"][:2]
    for it in recs:
        with st.container(border=True):
            st.markdown(f"**{it['title']}**")
            st.caption(it["summary"])
            st.write("Modality:", it.get("modality","text"), " • Minutes:", it.get("minutes",5))
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("Start over"):
            st.session_state.phase = "welcome"
            st.session_state.selected_moods = set()
            st.session_state.time_choice = None
            st.rerun()
    with c2:
        if st.button("Pick different moods"):
            st.session_state.phase = "mood"
            st.rerun()
