from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import os
import sqlite3
import time
import pandas as pd
import streamlit as st
import google.generativeai as genai

# ============================================================
#  CONFIG
# ============================================================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(
    page_title="AI Text ➜ SQL Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
#  PROMPT
# ============================================================
PROMPT = [
    """
    You are an expert in converting English questions to SQL queries!

    The SQL database has the name STUDENT and has the following columns:
    NAME, CLASS, AGE, GENDER, ADDRESS, SECTION, MARKS

    Example 1:
    How many records are present?
    SQL:
    SELECT COUNT(*) FROM STUDENT;

    Example 2:
    Show all students in 10th Grade
    SQL:
    SELECT * FROM STUDENT WHERE CLASS='10th Grade';

    Example 3:
    Show all female students
    SQL:
    SELECT * FROM STUDENT WHERE GENDER='Female';

    Example 4:
    Show students with marks greater than 90
    SQL:
    SELECT * FROM STUDENT WHERE MARKS > 90;

    Example 5:
    What is the average marks of all students?
    SQL:
    SELECT AVG(MARKS) FROM STUDENT;

    Example 6:
    Who scored the highest marks?
    SQL:
    SELECT * FROM STUDENT ORDER BY MARKS DESC LIMIT 1;

    Also, the SQL query should not contain ```sql, ``` or any explanation.
    Return only the SQL query.
    """
]

MODEL_NAME = "gemini-1.5-flash"  # update to whichever Gemini model you have access to


# ============================================================
#  CORE FUNCTIONS
# ============================================================
def get_gemini_response(question: str, prompt: list[str]) -> str:
    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(prompt[0] + "\n\nQuestion: " + question)
    return response.text.strip().strip("`").replace("sql\n", "").strip()


def read_sql_response(sql: str, db: str):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description] if cur.description else []
    conn.commit()
    conn.close()
    return rows, columns


# ============================================================
#  SESSION STATE
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: question, sql, rows, cols, ok


# ============================================================
#  STYLES  (glassmorphism + gradients + animations)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"]  { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 0%, #1b1035 0%, #0b0714 45%, #050308 100%);
    color: #EDEBF7;
}

/* animated gradient title */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-title {
    font-size: 46px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #7F5AF0, #2CB67D, #FF6AC1, #7F5AF0);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 6s ease infinite;
    margin-bottom: 0px;
}
.hero-subtitle {
    text-align: center;
    color: #A9A4C2;
    font-size: 16px;
    margin-top: 4px;
    margin-bottom: 30px;
    letter-spacing: 0.3px;
}

/* floating orb decoration */
@keyframes floaty {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
}
.orb {
    animation: floaty 4s ease-in-out infinite;
    display: inline-block;
}

/* glass card */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 22px 26px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    margin-bottom: 18px;
    animation: fadeInUp 0.5s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* metric pill */
.metric-pill {
    background: linear-gradient(135deg, rgba(127,90,240,0.18), rgba(44,182,125,0.12));
    border: 1px solid rgba(127,90,240,0.35);
    border-radius: 14px;
    padding: 14px 18px;
    text-align: center;
}
.metric-pill .num { font-size: 26px; font-weight: 700; color: #C9C2FF; }
.metric-pill .lbl { font-size: 12px; color: #9E97C0; text-transform: uppercase; letter-spacing: 1px; }

/* input box */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    border: 1.5px solid rgba(127,90,240,0.45);
    color: #fff;
    padding: 14px 16px;
    font-size: 15px;
}
.stTextInput > div > div > input:focus {
    border: 1.5px solid #7F5AF0;
    box-shadow: 0 0 0 3px rgba(127,90,240,0.25);
}

/* button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #7F5AF0, #5E3BD8);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 18px rgba(127,90,240,0.35);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(127,90,240,0.55);
}

/* code block */
.stCodeBlock, pre {
    border-radius: 14px !important;
    border: 1px solid rgba(44,182,125,0.35) !important;
}

/* sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120a24, #0b0714);
    border-right: 1px solid rgba(255,255,255,0.07);
}

/* chip */
.chip {
    display: inline-block;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 6px 14px;
    margin: 4px 6px 4px 0;
    font-size: 13px;
    color: #C9C2FF;
    cursor: pointer;
}

hr { border-color: rgba(255,255,255,0.08); }
</style>
""", unsafe_allow_html=True)


# ============================================================
#  HERO HEADER
# ============================================================
st.markdown('<div class="hero-title">🤖 AI Text ➜ SQL Studio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Ask questions in plain English '
    '<span class="orb">✨</span> get instant SQL &amp; live results, powered by Gemini</div>',
    unsafe_allow_html=True,
)

# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ About this Studio")
    st.write(
        "Converts natural-language questions into SQL for the **STUDENT** table, "
        "runs them live, and shows the results — instantly."
    )
    st.markdown("---")
    st.markdown("**Database:** SQLite &nbsp;•&nbsp; `student.db`")
    st.markdown(f"**AI Model:** `{MODEL_NAME}`")
    st.markdown("**Framework:** Streamlit")
    st.markdown("---")
    st.markdown("### 💡 Try asking")
    examples = [
        "How many records are present?",
        "Show all female students",
        "Show students with marks greater than 90",
        "Who scored the highest marks?",
        "Average marks by section",
    ]
    for ex in examples:
        st.markdown(f'<div class="chip">💬 {ex}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.history:
        st.markdown(f"**Queries run this session:** {len(st.session_state.history)}")
        if st.button("🗑️ Clear history"):
            st.session_state.history = []
            st.rerun()


# ============================================================
#  METRIC STRIP
# ============================================================
total_queries = len(st.session_state.history)
successful = sum(1 for h in st.session_state.history if h["ok"])
last_rows = st.session_state.history[-1]["row_count"] if st.session_state.history else 0

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="metric-pill"><div class="num">{total_queries}</div><div class="lbl">Queries Run</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-pill"><div class="num">{successful}</div><div class="lbl">Successful</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-pill"><div class="num">{last_rows}</div><div class="lbl">Rows (Last Query)</div></div>', unsafe_allow_html=True)

st.write("")

# ============================================================
#  MAIN INPUT CARD
# ============================================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_input(
        "💬 Ask your question",
        placeholder="e.g. Show all students with marks greater than 90",
        label_visibility="collapsed",
    )
with col2:
    submit = st.button("🚀 Generate")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
#  PROCESSING
# ============================================================
if submit and question.strip():

    progress_ph = st.empty()
    with progress_ph.container():
        st.markdown('<div class="glass-card">⚡ Thinking… converting your question into SQL</div>', unsafe_allow_html=True)
        bar = st.progress(0)
        for pct in (25, 55, 80, 100):
            time.sleep(0.12)
            bar.progress(pct)
    progress_ph.empty()

    sql_query, rows, columns, ok, error_msg = "", [], [], False, None
    try:
        sql_query = get_gemini_response(question, PROMPT)
        rows, columns = read_sql_response(sql_query, "student.db")
        ok = True
    except Exception as e:
        error_msg = str(e)

    st.session_state.history.append({
        "question": question,
        "sql": sql_query,
        "rows": rows,
        "columns": columns,
        "row_count": len(rows) if ok else 0,
        "ok": ok,
        "error": error_msg,
    })
    st.rerun()

elif submit and not question.strip():
    st.warning("Type a question first ✨")

# ============================================================
#  RESULTS (most recent first)
# ============================================================
if st.session_state.history:
    st.markdown("### 📜 Results")

for entry in reversed(st.session_state.history):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"**❓ {entry['question']}**")

    if entry["ok"]:
        st.markdown("📝 **Generated SQL**")
        st.code(entry["sql"], language="sql")

        st.markdown("📊 **Query Result**")
        if entry["rows"]:
            df = pd.DataFrame(entry["rows"], columns=entry["columns"] or None)
            st.dataframe(df, use_container_width=True)
            st.download_button(
                "⬇️ Download CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="query_result.csv",
                mime="text/csv",
                key=f"dl_{id(entry)}",
            )
        else:
            st.info("No records found.")
    else:
        st.error(f"Database Error: {entry['error']}")

    st.markdown('</div>', unsafe_allow_html=True)