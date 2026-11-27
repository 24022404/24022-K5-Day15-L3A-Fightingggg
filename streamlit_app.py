"""Lớp học có trợ giảng (Streamlit) của nhóm Fightingggg.
Bài học bằng chữ bên trái, hỏi trợ giảng bên phải; trợ giảng chỉ trả lời từ bài và ghi mã đoạn.
Chạy: streamlit run streamlit_app.py"""
import html
import os
import re
import sys
import time

import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "codebase"))
try:  # trên Streamlit Cloud, khoá nằm trong Secrets
    for _k in ("MODEL_PROVIDER", "MODEL_NAME", "API_KEY"):
        if _k in st.secrets:
            os.environ.setdefault(_k, str(st.secrets[_k]))
except Exception:
    pass

import tracing  # noqa: E402
from agent import answer, NO_ANSWER, REFUSE_REPLY  # noqa: E402
from tools import load_passages  # noqa: E402

MAX_Q = 15  # giới hạn câu hỏi mỗi phiên để không cạn lượt gọi miễn phí
COURSE = "Nền tảng LLM"

st.set_page_config(page_title="Nền tảng LLM · Day 1", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');
html, body, [class*="css"], .stMarkdown, button, input, textarea {font-family: 'Lato', 'Helvetica Neue', Arial, sans-serif !important;}
header, #MainMenu, footer {visibility: hidden; height: 0;}
[data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] {display: none;}
.stApp {background: #fff;}
.block-container {padding: 1rem 2rem 5rem 2rem; max-width: 100%;}
[data-testid="stSidebar"] {background: linear-gradient(90deg, #1f3d99 0, #1f3d99 80px, #fff 80px); border-right: 1px solid #c7cdd1; width: 290px !important; min-width: 290px !important;}
[data-testid="stSidebar"] > div:first-child {width: 290px;}
[data-testid="stSidebarContent"] {padding-left: 80px;}
[data-testid="stSidebar"] .block-container, [data-testid="stSidebarContent"] {padding-top: 1.2rem;}
[data-testid="stSidebar"] .stButton button {justify-content: flex-start !important; border: 0; background: transparent; color: #0374b5; font-size: .95rem; padding: .25rem .6rem; min-height: 0; border-radius: 0; box-shadow: none;}
[data-testid="stSidebar"] .stButton button div, [data-testid="stSidebar"] .stButton button p {justify-content: flex-start !important; text-align: left !important; width: 100%;}
[data-testid="stSidebar"] .stButton button[kind="primary"] {color: #111; font-weight: 700; border-left: 2px solid #111; background: transparent;}
/* thanh xanh toàn cục: các nút nằm cố định bên trái */
.gnav-logo {position: fixed; left: 0; top: 0; width: 80px; height: 84px; background: #1f3d99; z-index: 999990; display: flex; align-items: center; justify-content: center;}
.gnav-logo div {width: 52px; height: 52px; border-radius: 50%; background: #fff; color: #1f3d99; font-weight: 900; display: flex; align-items: center; justify-content: center; border: 3px solid #9fb3f0;}
[class*="st-key-g_"] {position: fixed !important; left: 0; width: 80px !important; z-index: 999991; margin: 0 !important;}
[class*="st-key-g_"] button {width: 80px !important; height: 70px; border-radius: 0 !important; background: transparent !important; color: #fff !important; border: 0 !important; flex-direction: column; justify-content: center !important; padding: 0 !important; gap: 4px;}
[class*="st-key-g_"] button::before {content: ""; display: block; width: 26px; height: 26px; background-color: currentColor; -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat; -webkit-mask-position: center; mask-position: center; -webkit-mask-size: contain; mask-size: contain;}
[class*="st-key-g_"] button p {text-align: center !important; width: 100%; font-size: .74rem; line-height: 1;}
[class*="st-key-g_"] button[kind="primary"] {background: #fff !important; color: #1f3d99 !important; font-weight: 700;}
.st-key-g_account button::before {-webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8'/%3E%3C/svg%3E"); mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8'/%3E%3C/svg%3E");}
.st-key-g_dash button::before {-webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 17a9 9 0 1 1 18 0'/%3E%3Cpath d='M12 17l4-5'/%3E%3Ccircle cx='12' cy='17' r='1.2'/%3E%3C/svg%3E"); mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 17a9 9 0 1 1 18 0'/%3E%3Cpath d='M12 17l4-5'/%3E%3Ccircle cx='12' cy='17' r='1.2'/%3E%3C/svg%3E");}
.st-key-g_courses button::before {-webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z'/%3E%3Cpath d='M5 17a3 3 0 0 1 3-3h11'/%3E%3Cpath d='M9 8h6'/%3E%3C/svg%3E"); mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z'/%3E%3Cpath d='M5 17a3 3 0 0 1 3-3h11'/%3E%3Cpath d='M9 8h6'/%3E%3C/svg%3E");}
.st-key-g_inbox button::before {-webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 13l3-8h12l3 8v6H3z'/%3E%3Cpath d='M3 13h5l1 3h6l1-3h5'/%3E%3C/svg%3E"); mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 13l3-8h12l3 8v6H3z'/%3E%3Cpath d='M3 13h5l1 3h6l1-3h5'/%3E%3C/svg%3E");}
.st-key-g_help button::before {-webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpath d='M9.5 9.5a2.5 2.5 0 1 1 4 2c-1 .7-1.5 1.2-1.5 2.5'/%3E%3Cpath d='M12 17.5v.01'/%3E%3C/svg%3E"); mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpath d='M9.5 9.5a2.5 2.5 0 1 1 4 2c-1 .7-1.5 1.2-1.5 2.5'/%3E%3Cpath d='M12 17.5v.01'/%3E%3C/svg%3E");}
.st-key-g_account {top: 92px;} .st-key-g_dash {top: 164px;} .st-key-g_courses {top: 236px;} .st-key-g_inbox {top: 308px;} .st-key-g_help {top: 380px;}
.term {font-size: .62rem; color: #333; margin: 0 0 .7rem .6rem;}
.crumb {display: flex; align-items: center; gap: .6rem; font-size: 1.05rem; padding-bottom: .8rem; border-bottom: 1px solid #c7cdd1; margin-bottom: 1.2rem;}
.crumb a {color: #0374b5;} .crumb .sep {color: #6b7780;} .crumb .hb {font-size: 1.4rem; color: #0374b5;}
.pagetitle {font-size: 1.8rem; font-weight: 400; color: #2d3b45; margin: .2rem 0 .8rem 0;}
.ann {display: flex; gap: 1rem; padding: .9rem 0; border-top: 1px solid #c7cdd1; border-bottom: 1px solid #c7cdd1; margin-bottom: 0;}
.ann .av {width: 34px; height: 34px; border-radius: 50%; background: #c7cdd1; flex: none;}
.ann b {display: block;} .ann small {color: #2d3b45;} .ann .when {margin-left: auto; text-align: right; font-size: .78rem; color: #2d3b45; white-space: nowrap;}
.mhead {background: #f5f5f5; border: 1px solid #c7cdd1; padding: .85rem 1rem; font-size: 1rem; color: #2d3b45; margin-top: 1rem;}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {gap: 0;}
[data-testid="stHorizontalBlock"]:has(.rowc):not(:has([data-testid="stHorizontalBlock"])) {border-bottom: 1px solid #e1e5e8; align-items: center; padding: .1rem 0;}
.sidebtn {background: #f5f5f5; border: 1px solid #c7cdd1; padding: .55rem .8rem; margin-bottom: .45rem; color: #2d3b45; font-size: .9rem;}
.sidebox h4 {font-size: 1rem; margin: 1.2rem 0 .3rem 0; border-bottom: 1px solid #c7cdd1; padding-bottom: .4rem;} .sidebox p {font-size: .82rem; color: #2d3b45; margin: .2rem 0;}
.page {border: 1px solid #c7cdd1; padding: 1.6rem 2rem; background: #fff; font-size: 1.05rem; line-height: 1.7; color: #2d3b45;}
.page ul {margin: .6rem 0 .2rem 1.2rem;} .page li {margin-bottom: .5rem;}
.tag {background: #0374b5; color: #fff; border-radius: 0; padding: 0 .45rem; font-size: .72rem; font-weight: 700; margin-left: .5rem; vertical-align: middle;}
.tbl {width: 100%; border-collapse: collapse; font-size: .92rem; color: #2d3b45;} .tbl th, .tbl td {border-bottom: 1px solid #e1e5e8; padding: .5rem .6rem; text-align: left;} .tbl th {background: #f5f5f5;}
.card {border: 1px solid #c7cdd1; padding: 1rem 1.2rem; margin-bottom: .8rem; background: #fff;} .card h3 {margin: 0 0 .3rem 0; font-size: 1.1rem; color: #2d3b45;}
.badge {display: inline-block; padding: .12rem .55rem; border-radius: 0; font-size: .74rem; font-weight: 700; margin-bottom: .35rem;}
.b-answer {background: #e6f4ea; color: #0b6b36;} .b-ask {background: #e3f0fa; color: #0a5a96;}
.b-none {background: #fdf1d8; color: #8a5300;} .b-refuse {background: #fde7e6; color: #a0201a;} .b-other {background: #eceff1; color: #2d3b45;}
.code {background: #0374b5; color: #fff; border-radius: 0; padding: 0 .4rem; font-weight: 700; font-size: .85em;}
.meta {color: #6b7780; font-size: .72rem; margin-top: .3rem;} .note {color: #6b7780; font-size: .75rem;}
/* nút kiểu Canvas: phẳng, bo nhẹ */
.stButton button {border-radius: 2px !important;}
section.stMain .stButton button {background: #f5f5f5; border: 1px solid #c7cdd1; color: #2d3b45; box-shadow: none;}
section.stMain .stButton button[kind="primary"] {background: #0374b5; border-color: #0374b5; color: #fff;}
section.stMain .stButton button[kind="primary"] p {color: #fff;}
section.stMain .stButton button[kind="tertiary"] {background: transparent; border: 0; color: #0374b5; padding-left: 0;}
.modhead {display: flex; justify-content: space-between; align-items: center;}
.pgico {color: #6b7780; padding-top: .35rem;}
.circ {display: inline-block; width: 18px; height: 18px; border-radius: 50%; background: #0b874b; color: #fff; text-align: center; font-size: .72rem; line-height: 18px; font-weight: 700;}
.circ.off {background: #fff; border: 1px solid #c7cdd1; color: #fff;}
.ex {border-left: 4px solid #0374b5; background: #f1f8fc; padding: .7rem 1rem; margin-top: 1rem; font-size: .98rem;}
.more {margin-top: 1rem; font-size: .95rem;} .more a {color: #0374b5;} .more li {margin-bottom: .25rem;}
.src {color: #6b7780; font-size: .75rem; margin-top: .6rem;}
/* khung trợ giảng kiểu Messenger, nằm bên phải trang bài */
.st-key-msgr {border: 1px solid #c7cdd1; border-radius: 0; background: #fff; position: sticky; top: .8rem; padding: 0 0 1rem 0; box-shadow: 0 1px 4px rgba(0,0,0,.08);}
.st-key-msgr [data-testid="stVerticalBlock"] {gap: .2rem;}
.mhd {display: flex; align-items: center; gap: .6rem; padding: .7rem .9rem; border-bottom: 1px solid #e1e5e8;}
.mhd b {display: block; font-size: .98rem; color: #1c1e21;} .mhd small {color: #6b7780; font-size: .72rem; display: block;}
.ava {width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0374b5, #4aa3d8); color: #fff; font-weight: 800; font-size: .72rem; display: flex; align-items: center; justify-content: center; flex: none;}
.ava.sm {width: 26px; height: 26px; font-size: .6rem;}
.dot {width: 8px; height: 8px; border-radius: 50%; background: #31a24c; display: inline-block; margin-right: .25rem;}
.mline {display: flex; gap: .4rem; margin: .3rem .6rem; align-items: flex-start;} .mline.me {justify-content: flex-end;}
.bub {max-width: 84%; padding: .5rem .8rem; border-radius: 2px; line-height: 1.45; font-size: .92rem; word-wrap: break-word;}
.bub.me {background: #0374b5; color: #fff;}
.bub.bot {background: #eef1f3; color: #1c1e21; border-left: 3px solid #0374b5;}
.bub .lab {display: block; font-size: .66rem; font-weight: 800; margin-bottom: .15rem; text-transform: uppercase; letter-spacing: .02em;}
.l-answer {color: #0b6b36;} .l-ask {color: #0a5a96;} .l-none {color: #8a5300;} .l-refuse {color: #a0201a;} .l-other {color: #444;}
.mmeta {color: #8a949c; font-size: .64rem; margin: -.1rem 0 .2rem 2.6rem;}
.st-key-msgr .stButton button {border-radius: 0 !important; border: 1px solid #0374b5 !important; color: #0374b5 !important; background: #fff !important; font-size: .8rem; padding: .15rem .8rem; min-height: 0;}
.st-key-msgr .stButton button p {color: #0374b5 !important; font-size: .8rem;}
.badge {display: inline-block; padding: .12rem .55rem; border-radius: 0; font-size: .74rem; font-weight: 700; margin-bottom: .35rem;}
.b-answer {background: #e6f4ea; color: #0b6b36;} .b-ask {background: #e3f0fa; color: #0a5a96;}
.b-none {background: #fdf1d8; color: #8a5300;} .b-refuse {background: #fde7e6; color: #a0201a;} .b-other {background: #eceff1; color: #2d3b45;}

.login-bg {position: fixed; inset: 0; background: linear-gradient(160deg, #1f3d99 0%, #16296b 100%); z-index: -1;}
.loginbox {background: #fff; padding: 2rem 2.2rem; border-top: 6px solid #0374b5; margin-top: 4vh;}
.loginbox h2 {font-size: 1.5rem; color: #2d3b45; margin: .6rem 0 .2rem 0; font-weight: 700;} .loginbox p {color: #6b7780; font-size: .88rem;}
.loginlogo {width: 64px; height: 64px; border-radius: 50%; background: #1f3d99; color: #fff; font-weight: 900; font-size: 1.3rem; display: flex; align-items: center; justify-content: center; border: 4px solid #9fb3f0;}
.bigava {width: 96px; height: 96px; border-radius: 50%; background: #1f3d99; color: #fff; font-weight: 800; font-size: 2rem; display: flex; align-items: center; justify-content: center;}
.dl {display: grid; grid-template-columns: 11rem 1fr; gap: .5rem 1rem; font-size: .95rem; margin: .8rem 0;} .dl dt {color: #6b7780;} .dl dd {margin: 0; color: #2d3b45; font-weight: 700;}
.ccard {border: 1px solid #c7cdd1; background: #fff; width: 100%; max-width: 280px;} .ccard .top {background: #1f3d99; height: 110px; padding: .7rem .9rem; color: #fff; font-size: .72rem; letter-spacing: .04em; text-transform: uppercase;}
.ccard .bd {padding: .8rem .9rem;} .ccard .bd b {color: #0374b5; display: block; font-size: 1rem;} .ccard .bd span {color: #6b7780; font-size: .78rem;}
.ccard .ft {border-top: 1px solid #e1e5e8; padding: .5rem .9rem; color: #6b7780; font-size: .78rem;}
.who {font-size: .8rem; color: #2d3b45; margin: .4rem 0 .3rem .6rem;} .who b {display: block;}
.avs {width: 32px; height: 32px; border-radius: 50%; background: #1f3d99; color: #fff; font-weight: 700; font-size: .75rem; display: inline-flex; align-items: center; justify-content: center; margin-right: .5rem; vertical-align: middle;}
[data-testid="stForm"] {background: #fff; border: 0 !important; border-radius: 0 !important; padding: 1rem 2.2rem 1.4rem 2.2rem;}
[data-testid="stForm"] label p {color: #2d3b45 !important;} [data-testid="stForm"] input {border-radius: 0 !important;}
.loginbox {padding-bottom: .4rem !important;}
.pgico {padding-top: 0 !important; transform: translateY(-9px);} .rowc {transform: translateY(-9px);}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius: 0 !important;}
[data-testid="stTextInput"] input, [data-testid="stChatInput"] {border-radius: 2px !important;}
</style>
""",
    unsafe_allow_html=True,
)

PASSAGES = load_passages()
BY_CODE = {p["code"]: p for p in PASSAGES}
CODES = [p["code"] for p in PASSAGES]
KINDS = {
    "answer": ("Có căn cứ trong bài", "l-answer"),
    "ask": ("Hỏi lại cho rõ", "l-ask"),
    "none": ("Không có trong bài", "l-none"),
    "refuse": ("Từ chối", "l-refuse"),
    "other": ("Phản hồi", "l-other"),
    "fake": ("Chưa nối model", "l-other"),
    "error": ("Lỗi", "l-refuse"),
}
NAV = [("home", "Home"), ("announcements", "Announcements"), ("assignments", "Assignments"),
       ("grades", "Grades"), ("people", "People"), ("files", "Files"), ("syllabus", "Syllabus"), ("modules", "Modules")]
GNAV = [("account", "Tài khoản"), ("dash", "Dashboard"), ("courses", "Khóa học"), ("inbox", "Hộp thư"), ("help", "Trợ giúp")]

# Phần mở rộng của mỗi trang: ví dụ do nhóm viết + liên kết đọc thêm lấy từ web (tìm ngày 27/11/2026).
# Trợ giảng chỉ dựa vào phần "Nội dung chính" (data/lesson_sample.md), không dựa vào ví dụ hay liên kết.
EXTRA = {
    "p01": ("Bạn gõ \"Thủ đô của Việt Nam là\": mô hình chọn mẩu chữ có khả năng cao tiếp theo, ví dụ \"Hà Nội\", rồi cứ thế viết tiếp từng mẩu.",
            [("Cloudflare: What is a large language model?", "https://cloudflare.com/learning/ai/what-is-large-language-model"),
             ("Udemy Blog: How do LLMs work?", "https://blog.udemy.com/how-do-llms-work/")]),
    "p02": ("Một câu tiếng Việt ngắn có thể bị tách thành vài token. Chi phí tính theo số token chứ không theo số từ, nên viết dài hơn thì tốn hơn.",
            [("Harvard Chan: What is a token in AI?", "https://hsph.harvard.edu/advanced-learning-academy/news/token/"),
             ("It's FOSS: What are tokens in LLMs?", "https://itsfoss.com/llm-token/"),
             ("Viblo: Token AI là gì? (tiếng Việt)", "https://viblo.asia/p/token-ai-la-gi-don-vi-du-lieu-va-cua-so-ngu-canh-cua-ai-K9Vy8wKdLQR")]),
    "p03": ("Bạn dán một tài liệu rất dài rồi hỏi ở cuối. Phần nằm ngoài cửa sổ ngữ cảnh thì mô hình không nhìn thấy, nên cần cắt nhỏ hoặc chỉ đưa phần liên quan.",
            [("Viblo: Cửa sổ ngữ cảnh là gì và quản lý ra sao? (tiếng Việt)", "https://viblo.asia/p/cua-so-ngu-canh-context-window-la-gi-va-quan-ly-ra-sao-lZL9XQkvJQK"),
             ("IBM: What is a context window?", "https://www.ibm.com/think/topics/context-window"),
             ("AWS Security Blog: Context window overflow", "https://aws.amazon.com/blogs/security/context-window-overflow-breaking-the-barrier")]),
    "p04": ("Cần trả lời đúng một định nghĩa thì dùng temperature thấp. Cần nghĩ nhiều tên gọi khác nhau cho một sản phẩm thì có thể để cao hơn.",
            [("IBM: What is LLM temperature?", "https://www.ibm.com/think/topics/llm-temperature"),
             ("Mistral docs: Sampling and temperature", "https://docs.mistral.ai/cookbooks/concept-deep-dive-sampling-temperature")]),
    "p05": ("Hỏi về một bài báo không có thật, mô hình vẫn có thể bịa ra tên tác giả nghe rất hợp lý. Đưa tài liệu nguồn và cho phép nói \"không có trong tài liệu\" giúp giảm lỗi này.",
            [("Zapier: What are AI hallucinations?", "https://zapier.com/blog/ai-hallucinations/")]),
    "p06": ("Thay vì \"Tóm tắt bài này\", hãy viết: \"Tóm tắt bài này trong 3 gạch đầu dòng, mỗi gạch dưới 20 từ, không thêm ý ngoài bài.\"",
            [("web.dev: Prompt engineering", "https://web.dev/learn/ai/prompt-engineering"),
             ("Claude: Best practices for prompt engineering", "https://claude.com/resources/articles/best-practices-for-prompt-engineering")]),
    "p07": ("Học viên hỏi về cửa sổ ngữ cảnh. Hệ thống tìm đoạn p03 trước, đưa vào prompt, rồi mới nhờ mô hình trả lời dựa trên đoạn đó.",
            [("AWS Builder Center: What is RAG? A beginner-friendly guide", "https://builder.aws.com/content/3KQHuNUmvOJGDh5Xo8yZrWaN282/what-is-rag-a-beginner-friendly-guide-to-retrieval-augmented-generation"),
             ("DEV: RAG explained for beginners", "https://dev.to/aashna_mahajan/rag-explained-for-beginners-how-ai-assistants-stop-making-things-up-2i05")]),
    "p08": ("Dựng 10 câu thử: 6 câu dễ, 2 câu khó, 2 câu cần từ chối. Chạy lại sau mỗi lần sửa và đếm bao nhiêu câu đạt.",
            [("Thoughtworks: How to evaluate an LLM system", "https://www.thoughtworks.com/en-in/insights/blog/generative-ai/how-to-evaluate-an-LLM-system"),
             ("Arize: The definitive guide to LLM evaluations", "https://arize.com/blog/llm-evaluation-guide/")]),
}
GREET = "Chào {name}! Mình là trợ giảng của khoá. Chỗ nào trong trang này chưa rõ thì cứ hỏi. Mình chỉ trả lời từ nội dung chính của bài và luôn ghi mã đoạn để bạn kiểm tra."
CHIPS = ["Token là gì và vì sao nó ảnh hưởng chi phí?", "Fine-tuning khác RAG ở điểm nào?", "Viết hộ tôi bài nộp tuần này."]


def classify(out):
    if out.startswith("[giả"):
        return "fake"
    if out.startswith("Lỗi khi gọi model"):
        return "error"
    if re.search(r"\bp\d{2}\b", out):
        return "answer"
    low = out.lower()
    if out == NO_ANSWER or "không có trong bài" in low:
        return "none"
    if out == REFUSE_REPLY or "không làm được" in low or "không thể" in low or "từ chối" in low:
        return "refuse"
    if out.rstrip().endswith("?"):
        return "ask"
    return "other"


def pretty(out):
    return re.sub(r"\[?\b(p\d{2})\b\]?", r'<span class="code">\1</span>', html.escape(out))


def btn(label, **kw):
    """Nút dạng liên kết; bản Streamlit cũ không có type tertiary thì dùng nút thường."""
    try:
        return st.button(label, type="tertiary", **kw)
    except Exception:
        return st.button(label, **kw)


def ask(text):
    st.session_state.n += 1
    tracing.begin("web")
    t0 = time.time()
    try:
        out = answer(text)["output"]
    except Exception as e:  # lỗi gọi model
        out = "Lỗi khi gọi model: %s" % e
    summary, _ = tracing.end()
    codes = [c for c in dict.fromkeys(re.findall(r"\bp\d{2}\b", out)) if c in BY_CODE]
    st.session_state.msgs.append(
        {"q": text, "out": out, "kind": classify(out), "codes": codes, "sum": summary, "sec": time.time() - t0}
    )


def set_pending(q):
    st.session_state.pending = q


def go(page):
    st.session_state.page = page


def set_sec(i):
    st.session_state.sec = max(0, min(len(PASSAGES) - 1, i))


def open_lesson(i):
    set_sec(i)
    st.session_state.page = "lesson"


def open_code(code):
    open_lesson(CODES.index(code))


def toggle_done(code):
    d = st.session_state.understood
    d.discard(code) if code in d else d.add(code)


def toggle_collapse():
    st.session_state.collapsed = not st.session_state.collapsed


SCROLL_JS = """<script>
try {
  const d = window.parent.document;
  const go = () => d.querySelectorAll('.st-key-msgr div').forEach(el => {
    if (el.scrollHeight > el.clientHeight + 4 && getComputedStyle(el).overflowY !== 'visible') el.scrollTop = el.scrollHeight;
  });
  setTimeout(go, 150); setTimeout(go, 600);
} catch (e) {}
</script>"""


def run_js(code):
    """Chạy một đoạn JS nhỏ (cuộn khung chat xuống tin mới nhất). Lỗi thì bỏ qua, app không phụ thuộc vào nó."""
    try:
        if hasattr(st, "iframe"):
            st.iframe(code, height=1)
        else:
            import streamlit.components.v1 as components
            components.html(code, height=0)
    except Exception:
        pass


def initials(name):
    parts = [w for w in re.split(r"\s+", name.strip()) if w]
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else (parts[0][:2].upper() if parts else "?")


def do_login(name, sid, email):
    st.session_state.user = {"name": name.strip(), "id": sid.strip(), "email": email.strip()}
    st.session_state.login_at = time.strftime("%H:%M %d/%m/%Y")
    st.session_state.page = "home"


def do_logout():
    for k in ("user", "login_at", "msgs", "n", "understood", "sec", "page", "collapsed", "pending"):
        st.session_state.pop(k, None)


if "n" not in st.session_state:
    st.session_state.n = 0
    st.session_state.msgs = []
    st.session_state.page = "home"
    st.session_state.sec = 0
    st.session_state.understood = set()
    st.session_state.collapsed = False
    st.session_state.user = None
    st.session_state.login_at = None


# ---------------------------------------------------------------- đăng nhập (demo, không xác thực)
if not st.session_state.get("user"):
    st.markdown("<style>[data-testid='stSidebar']{display:none;} .stApp{background:linear-gradient(160deg,#1f3d99 0%,#16296b 100%);}</style>", unsafe_allow_html=True)
    _l, _m, _r = st.columns([1, 1.15, 1])
    with _m:
        st.markdown('<div class="loginbox"><div class="loginlogo">AI</div><h2>Đăng nhập Lớp học AI20K</h2>'
                    "<p>Khoá 5 · Nền tảng LLM · Day 1</p></div>", unsafe_allow_html=True)
        with st.form("login"):
            lname = st.text_input("Họ và tên", placeholder="Ví dụ: Nguyễn Văn An")
            lid = st.text_input("Mã học viên (không bắt buộc)")
            lmail = st.text_input("Email (không bắt buộc)")
            ok = st.form_submit_button("Đăng nhập", type="primary", use_container_width=True)
        if ok:
            if lname.strip():
                do_login(lname, lid, lmail)
                st.rerun()
            else:
                st.error("Vui lòng nhập họ và tên.")
        st.button("Vào với tư cách khách", key="guest", on_click=do_login, args=("Khách", "", ""), use_container_width=True)
        st.markdown('<div class="note" style="color:#cfd8f5;margin-top:.8rem">Bản demo: không có mật khẩu và không xác thực danh tính. '
                    "Thông tin chỉ nằm trong phiên trình duyệt này, không được lưu hay gửi đi đâu.</div>", unsafe_allow_html=True)
    st.stop()
USER = st.session_state.user

page = st.session_state.page
n_sec = len(PASSAGES)
done_n = len(st.session_state.understood)

# Thanh xanh toàn cục bên trái (mọi nút bấm được)
gactive = page if page in ("account", "dash", "courses", "inbox", "help") else "courses"
for key, label in GNAV:
    st.button(label, key="g_" + key, on_click=go, args=(key,), type="primary" if gactive == key else "secondary")

# Menu của khoá học
with st.sidebar:
    st.markdown('<div class="gnav-logo"><div>AI</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="term">AI20K · Khoá 5 · Day 1</div>', unsafe_allow_html=True)
    cur_nav = "modules" if page == "lesson" else page
    for key, label in NAV:
        st.button(label, key="nav_" + key, on_click=go, args=(key,), use_container_width=True,
                  type="primary" if cur_nav == key else "secondary")
    st.markdown("---")
    if st.session_state.n:
        st.progress(min(st.session_state.n / MAX_Q, 1.0), text="Đã hỏi %d/%d câu" % (st.session_state.n, MAX_Q))
        if st.button("Xoá cuộc trò chuyện", use_container_width=True):
            st.session_state.msgs = []
            st.session_state.n = 0
            st.rerun()
    st.markdown('<div class="who"><span class="avs">%s</span><b style="display:inline">%s</b></div>' % (initials(USER["name"]), html.escape(USER["name"])), unsafe_allow_html=True)
    st.button("Đăng xuất", key="logout", on_click=do_logout, use_container_width=True)
    st.markdown(
        '<div class="note">Bản demo: không xác thực danh tính, dữ liệu chỉ nằm trong phiên này. Bài mẫu 8 đoạn do nhóm '
        "Fightingggg tự viết, không phải tài liệu của khoá. Không nhập thông tin cá nhân.</div>",
        unsafe_allow_html=True,
    )


def crumb(*parts):
    items = '<span class="sep">›</span>'.join(
        '<a>%s</a>' % html.escape(x) if i < len(parts) - 1 else '<span>%s</span>' % html.escape(x) for i, x in enumerate(parts))
    st.markdown('<div class="crumb"><span class="hb">≡</span>%s</div>' % items, unsafe_allow_html=True)


def title(t):
    st.markdown('<div class="pagetitle">%s</div>' % html.escape(t), unsafe_allow_html=True)


def table(headers, rows):
    th = "".join("<th>%s</th>" % h for h in headers)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    st.markdown('<table class="tbl"><tr>%s</tr>%s</table>' % (th, tr), unsafe_allow_html=True)


PG_SVG = ('<svg width="16" height="18" viewBox="0 0 16 18" fill="none" stroke="#6b7780" stroke-width="1.4">'
          '<path d="M3 1h7l4 4v12H3z"/><path d="M10 1v4h4M5.5 9h6M5.5 12h6"/></svg>')


def modules_list():
    c1, c2 = st.columns([5, 1])
    c2.button("Expand All" if st.session_state.collapsed else "Collapse All", key="collapse", on_click=toggle_collapse, use_container_width=True)
    st.markdown('<div class="mhead">%s &nbsp;Day 1 · Nền tảng LLM</div>' % ("▸" if st.session_state.collapsed else "▾"), unsafe_allow_html=True)
    if st.session_state.collapsed:
        return
    with st.container(border=True):
        for i, p in enumerate(PASSAGES):
            done = p["code"] in st.session_state.understood
            i0, i1, i2 = st.columns([0.4, 5, 1.4])
            i0.markdown('<div class="pgico">%s</div>' % PG_SVG, unsafe_allow_html=True)
            with i1:
                btn("%02d · %s" % (i + 1, p["title"]), key="mod_%d" % i, on_click=open_lesson, args=(i,))
            i2.markdown('<div class="note rowc" style="padding-top:0;text-align:right">%s</div>'
                        % ('<span class="circ">✓</span> Đã hoàn thành' if done else "Mã đoạn " + p["code"]), unsafe_allow_html=True)


def side_box():
    todo = "Còn %d trang chưa đánh dấu hoàn thành." % (n_sec - done_n) if done_n < n_sec else "Nothing for now"
    st.markdown('<div class="sidebtn">Tiến độ: %d/%d trang hoàn thành</div>'
                '<div class="sidebox"><h4>To Do</h4><p>%s</p></div>' % (done_n, n_sec, todo), unsafe_allow_html=True)


def announcement(t, body, when="27/11/2026"):
    st.markdown('<div class="ann"><div class="av"></div><div><b>%s</b><small>%s</small></div>'
                '<div class="when"><b style="display:inline">Posted on:</b><br>%s</div></div>' % (html.escape(t), html.escape(body), when),
                unsafe_allow_html=True)


ANNS = [
    ("Day 1 đã mở: Nền tảng LLM",
     "Bài đọc trước giờ lên lớp gồm 8 trang. Vào Modules, mở từng trang; bên phải mỗi trang có khung hỏi đáp để bạn hỏi ngay chỗ chưa hiểu."),
    ("Về bài mẫu và độ tin cậy",
     "Nội dung chính của 8 trang do nhóm Fightingggg tự viết cho bản demo, không phải tài liệu chính thức của khoá. Mỗi trang kèm ví dụ và liên kết đọc thêm từ nguồn công khai trên web."),
]

# ---------------------------------------------------------------- các trang
if page == "home":
    crumb("Nền tảng LLM (Day 1)")
    main, side = st.columns([4, 1.2], gap="large")
    with main:
        title("Recent Announcements")
        announcement(*ANNS[0])
        modules_list()
    with side:
        side_box()

elif page == "announcements":
    crumb("Nền tảng LLM (Day 1)", "Announcements")
    title("Announcements")
    for a in ANNS:
        announcement(*a)

elif page == "assignments":
    crumb("Nền tảng LLM (Day 1)", "Assignments")
    title("Assignments: tự kiểm tra Day 1")
    st.caption("Không chấm điểm. Tự trả lời bằng lời của bạn, rồi mở đáp án tham khảo để đối chiếu.")
    for i, p in enumerate(PASSAGES):
        with st.expander("%02d · Giải thích bằng lời của bạn: %s?" % (i + 1, p["title"])):
            st.markdown("**Đáp án tham khảo** (%s): %s" % (p["code"], p["text"]))
            st.button("Mở trang bài", key="as_open_%d" % i, on_click=open_lesson, args=(i,))

elif page == "grades":
    crumb("Nền tảng LLM (Day 1)", "Grades")
    title("Grades: tiến độ của bạn")
    c1, c2 = st.columns(2)
    c1.metric("Trang đã hoàn thành", "%d/%d" % (done_n, n_sec))
    c2.metric("Còn lại", n_sec - done_n)
    table(["Trang", "Mã đoạn", "Trạng thái"],
          [[p["title"], p["code"], "Đã hoàn thành" if p["code"] in st.session_state.understood else "Chưa"] for p in PASSAGES])
    st.markdown("&nbsp;")
    st.caption("Số liệu chỉ tính trong phiên này, không được lưu.")

elif page == "files":
    crumb("Nền tảng LLM (Day 1)", "Files")
    title("Files")
    base = os.path.dirname(os.path.abspath(__file__))
    for path, desc in ((os.path.join(base, "data", "lesson_sample.md"), "Nội dung chính 8 trang Day 1 (p01 đến p08), nhóm tự viết"),
                       (os.path.join(base, "data", "DATA_CARD.md"), "Thẻ dữ liệu: nguồn gốc và giới hạn của dữ liệu trong bản demo")):
        if os.path.exists(path):
            c1, c2 = st.columns([4, 1.4])
            c1.markdown("**%s**<br><span class='note'>%s</span>" % (os.path.basename(path), desc), unsafe_allow_html=True)
            with open(path, "rb") as f:
                c2.download_button("Tải về", f.read(), file_name=os.path.basename(path), key="dl_" + os.path.basename(path))

elif page == "syllabus":
    crumb("Nền tảng LLM (Day 1)", "Syllabus")
    title("Syllabus: Day 1 · Nền tảng LLM")
    st.markdown("Bài đọc trước giờ lên lớp gồm 8 trang. Mỗi trang có nội dung chính, một ví dụ và các liên kết đọc thêm.")
    table(["Mã", "Trang", "Ý chính"], [[p["code"], p["title"], html.escape(p["text"].split(". ")[0].rstrip(".") + ".")] for p in PASSAGES])

elif page == "modules":
    crumb("Nền tảng LLM (Day 1)", "Modules")
    main, side = st.columns([4, 1.2], gap="large")
    with main:
        modules_list()
    with side:
        side_box()

elif page == "lesson":
    cur = st.session_state.sec
    P = PASSAGES[cur]
    cited = set(st.session_state.msgs[-1]["codes"]) if st.session_state.msgs else set()
    crumb("Nền tảng LLM (Day 1)", "Pages", "%02d · %s" % (cur + 1, P["title"]))
    left, right = st.columns([3.3, 1.7], gap="large")

    # ---- nội dung trang bài (giữa)
    with left:
        h1, h2 = st.columns([3, 1.4])
        h1.markdown('<div class="pagetitle">%s</div>' % html.escape(P["title"]), unsafe_allow_html=True)
        done = P["code"] in st.session_state.understood
        h2.button("✓ Đã hoàn thành" if done else "Đánh dấu hoàn thành", key="done", on_click=toggle_done, args=(P["code"],),
                  use_container_width=True, type="secondary" if done else "primary")
        sentences = [x.strip() for x in re.split(r"(?<=[.!?])\s+", P["text"]) if x.strip()]
        lis = "".join("<li>%s</li>" % html.escape(x) for x in sentences)
        example, links = EXTRA[P["code"]]
        more = "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, html.escape(t)) for t, u in links)
        st.markdown(
            '<div class="page"><span class="code">%s</span>%s<ul>%s</ul>'
            '<div class="ex"><b>Ví dụ.</b> %s</div>'
            '<div class="more"><b>Đọc thêm</b><ul>%s</ul></div>'
            '<div class="src">Nội dung chính do nhóm viết (data/lesson_sample.md). Ví dụ do nhóm viết. Liên kết là nguồn công khai trên web, tìm ngày 27/11/2026; '
            "khung hỏi đáp chỉ dựa vào nội dung chính.</div></div>"
            % (P["code"], '<span class="tag">đoạn được trích</span>' if P["code"] in cited else "", lis, html.escape(example), more),
            unsafe_allow_html=True,
        )
        st.markdown("&nbsp;")
        a, b, c = st.columns([1, 2, 1])
        a.button("‹ Previous", key="prev", on_click=set_sec, args=(cur - 1,), disabled=cur == 0, use_container_width=True)
        c.button("Next ›", key="next", on_click=set_sec, args=(cur + 1,), disabled=cur >= n_sec - 1, use_container_width=True)

    # ---- khung trợ giảng kiểu Messenger (phải)
    with right:
        with st.container(key="msgr"):
            st.markdown('<div class="mhd"><div class="ava">TG</div><div><b>Trợ giảng AI</b>'
                        '<small><span class="dot"></span>Đang xem: %02d · %s</small></div></div>' % (cur + 1, html.escape(P["title"])),
                        unsafe_allow_html=True)
            box = st.container(height=430, border=False)
            with box:
                st.markdown('<div class="mline"><div class="ava sm">TG</div><div class="bub bot">%s</div></div>' % html.escape(GREET.format(name=USER["name"].split()[-1])),
                            unsafe_allow_html=True)
                for mi, m in enumerate(st.session_state.msgs):
                    st.markdown('<div class="mline me"><div class="bub me">%s</div></div>' % html.escape(m["q"]), unsafe_allow_html=True)
                    label, lcls = KINDS[m["kind"]]
                    st.markdown('<div class="mline"><div class="ava sm">TG</div><div class="bub bot"><span class="lab %s">%s</span>%s</div></div>'
                                % (lcls, label, pretty(m["out"])), unsafe_allow_html=True)
                    if m["codes"]:
                        cols = st.columns(len(m["codes"]))
                        for cc, code in zip(cols, m["codes"]):
                            cc.button("Mở đoạn %s" % code, key="open_%d_%s" % (mi, code), on_click=open_code, args=(code,))
                    s_ = m["sum"]
                    st.markdown('<div class="mmeta">%s · token %d/%d · %.1f giây</div>'
                                % (", ".join(s_["models"]) or "-", s_["tokens_in"], s_["tokens_out"], m["sec"]), unsafe_allow_html=True)
                if not st.session_state.msgs:
                    st.button("Giải thích trang này giúp mình", key="chip_ctx", on_click=set_pending,
                              args=("Giải thích giúp mình phần %s trong bài." % P["title"],))
                    for i, ex in enumerate(CHIPS):
                        st.button(ex, key="chip_%d" % i, on_click=set_pending, args=(ex,))
            typed = st.chat_input("Nhắn cho trợ giảng...")
            st.markdown('<div class="note" style="padding:0 .9rem">Trợ giảng chỉ dựa vào nội dung chính của bài. Có thể sai, hãy mở đoạn được trích để kiểm tra.</div>',
                        unsafe_allow_html=True)
    run_js(SCROLL_JS)
    q = (typed or st.session_state.pop("pending", None) or "").strip()
    if q:
        if st.session_state.n >= MAX_Q:
            st.toast("Đã hết %d câu cho phiên này. Bấm 'Xoá cuộc trò chuyện' ở thanh bên để hỏi tiếp." % MAX_Q)
        else:
            with st.spinner("Trợ giảng đang soạn câu trả lời..."):
                ask(q)
            st.rerun()

elif page == "people":
    crumb("Nền tảng LLM (Day 1)", "People")
    title("People")
    st.markdown("**Học viên**")
    table(["Tên", "Vai trò", "Mã học viên"], [[html.escape(USER["name"]), "Học viên (bạn)", html.escape(USER["id"] or "-")]])
    st.markdown("&nbsp;")
    st.markdown("**Nhóm phát triển bản demo (Fightingggg, Hackathon AI Day 15 · Track A)**")
    table(["Thành viên", "Phụ trách"],
          [["Minh", "Prototype, bộ khung chạy thử, spec"], ["Sang", "Số liệu pain, bằng chứng"],
           ["Phương", "Phỏng vấn, canvas, slide"], ["Long", "Bài mẫu, bộ câu thử, thẻ dữ liệu"]])
    st.caption("Giảng viên và TA chưa có trong bản demo.")

elif page == "dash":
    crumb("Dashboard")
    title("Dashboard")
    c1, c2 = st.columns([2.5, 1.2], gap="large")
    with c1:
        st.markdown('<div class="ccard"><div class="top">AI20K · Khoá 5</div><div class="bd"><b>Nền tảng LLM · Day 1</b>'
                    '<span>Xin chào %s. Tiến độ %d/%d trang.</span></div><div class="ft">8 trang bài đọc</div></div>'
                    % (html.escape(USER["name"]), done_n, n_sec), unsafe_allow_html=True)
        st.button("Vào khoá học", key="dash_open", on_click=go, args=("home",), type="primary")
        st.markdown("&nbsp;")
        title("Recent Announcements")
        announcement(*ANNS[0])
    with c2:
        side_box()

elif page == "courses":
    crumb("Khóa học")
    title("All Courses")
    table(["Khóa", "Học kỳ", "Trạng thái"], [["Nền tảng LLM · Day 1 (AI20K · Khoá 5)", "Demo", "Đang mở"]])
    st.markdown("&nbsp;")
    st.button("Mở khoá Nền tảng LLM · Day 1", key="courses_open", on_click=go, args=("home",), type="primary")
    st.caption("Bản demo chỉ có Day 1. Day 2 đến Day 15 chưa có bài.")

elif page == "inbox":
    crumb("Hộp thư")
    title("Inbox")
    st.info("Không có tin nhắn.")

elif page == "help":
    crumb("Trợ giúp")
    title("Help: cách dùng")
    st.markdown("1. Vào **Modules**, mở một trang bài và đọc nội dung chính, ví dụ và liên kết đọc thêm.\n"
                "2. Chưa hiểu chỗ nào, nhắn vào khung trợ giảng bên phải trang bài (hoặc bấm một câu gợi ý).\n"
                "3. Câu trả lời có thẻ mã đoạn như `p02`. Bấm **Mở đoạn p02** để mở đúng trang bài và tự đối chiếu.\n"
                "4. Hiểu xong thì bấm **Đánh dấu hoàn thành** để theo dõi tiến độ trong **Grades**.")
    st.markdown("**Lưu ý:** trợ giảng chỉ dựa vào nội dung chính của bài, có thể sai, và không thay giảng viên hay TA.")

elif page == "account":
    crumb("Tài khoản")
    title("Account")
    c1, c2 = st.columns([1, 4])
    c1.markdown('<div class="bigava">%s</div>' % initials(USER["name"]), unsafe_allow_html=True)
    with c2:
        st.markdown('<dl class="dl"><dt>Họ và tên</dt><dd>%s</dd><dt>Mã học viên</dt><dd>%s</dd><dt>Email</dt><dd>%s</dd>'
                    "<dt>Vai trò</dt><dd>Học viên</dd><dt>Khoá đang học</dt><dd>Nền tảng LLM · Day 1 (AI20K · Khoá 5)</dd>"
                    "<dt>Đăng nhập lúc</dt><dd>%s</dd><dt>Tiến độ</dt><dd>%d/%d trang hoàn thành</dd></dl>"
                    % (html.escape(USER["name"]), html.escape(USER["id"] or "Chưa nhập"), html.escape(USER["email"] or "Chưa nhập"),
                       st.session_state.login_at, done_n, n_sec), unsafe_allow_html=True)
        new_name = st.text_input("Đổi tên hiển thị", value=USER["name"], key="rename")
        b1, b2, _ = st.columns([1, 1, 3])
        if b1.button("Lưu tên", key="save_name") and new_name.strip():
            st.session_state.user["name"] = new_name.strip()
            st.rerun()
        b2.button("Đăng xuất", key="logout2", on_click=do_logout)
    st.caption("Bản demo không xác thực danh tính và không lưu thông tin ngoài phiên trình duyệt này.")
