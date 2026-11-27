"""Trang web demo (Streamlit): bài mẫu bên trái, hỏi trợ giảng bên phải. Chạy: streamlit run streamlit_app.py"""
import os
import sys

import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "codebase"))
try:  # trên Streamlit Cloud, khoá nằm trong Secrets
    for _k in ("MODEL_PROVIDER", "MODEL_NAME", "API_KEY"):
        if _k in st.secrets:
            os.environ.setdefault(_k, str(st.secrets[_k]))
except Exception:
    pass

import tracing  # noqa: E402
from agent import answer  # noqa: E402
from tools import load_passages  # noqa: E402

MAX_Q = 15  # giới hạn câu hỏi mỗi phiên để không cạn lượt gọi miễn phí

st.set_page_config(page_title="Trợ giảng có mã đoạn", layout="wide")
st.title("Trợ giảng trả lời có mã đoạn")
st.caption("Bài mẫu do nhóm Fightingggg tự viết; số liệu pain lấy từ nhật ký thật của khoá. Trả lời chỉ dựa trên 8 đoạn bên trái.")

left, right = st.columns([1, 1])
with left:
    st.subheader("Bài mẫu: nền tảng LLM")
    for p in load_passages():
        with st.expander("%s · %s" % (p["code"], p["title"]), expanded=False):
            st.write(p["text"])

with right:
    st.subheader("Hỏi trợ giảng")
    if "n" not in st.session_state:
        st.session_state.n = 0
        st.session_state.history = []
    with st.form("ask", clear_on_submit=True):
        q = st.text_input("Câu hỏi của bạn")
        sent = st.form_submit_button("Gửi")
    if sent and q.strip():
        if st.session_state.n >= MAX_Q:
            st.warning("Đã hết %d câu cho phiên này, tải lại trang để hỏi tiếp." % MAX_Q)
        else:
            st.session_state.n += 1
            tracing.begin("web")
            try:
                out = answer(q.strip())["output"]
            except Exception as e:  # lỗi gọi model
                out = "Lỗi khi gọi model: %s" % e
            summary, _ = tracing.end()
            st.session_state.history.insert(0, (q.strip(), out, summary))
    for hq, ho, hs in st.session_state.history:
        st.markdown("**Bạn:** " + hq)
        st.info(ho)
        st.caption("model: %s · token vào %d / ra %d" % (", ".join(hs["models"]) or "-", hs["tokens_in"], hs["tokens_out"]))
