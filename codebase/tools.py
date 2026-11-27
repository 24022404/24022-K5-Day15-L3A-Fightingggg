"""Công cụ của bài toán (nhóm Fightingggg): tra bài mẫu có mã đoạn.

Mỗi công cụ: tên · input · output · có tác động ra ngoài không (khớp spec.md §4).
Dữ liệu đọc: data/lesson_sample.md (bài mẫu 21 đoạn p01 đến p21, nhóm tự viết, xem data/DATA_CARD.md).
"""
import os
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

LESSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "lesson_sample.md")
_PASSAGE = re.compile(r"\*\*(p\d{2})\s*·\s*([^*]*?)\.\*\*\s*(.+)")
STOP = set("la gi va the nao khac cua nhu co khong nay do cho duoc trong mot nhung de em minh toi ban hay vi sao sao thi voi tu o".split())


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _tokens(s):
    return [w for w in re.findall(r"[a-z0-9]+", _norm(s)) if w not in STOP and len(w) > 1]


def load_passages():
    """Đọc bài mẫu → danh sách {"code", "title", "text"}."""
    out = []
    with open(LESSON, encoding="utf-8") as f:
        for line in f:
            m = _PASSAGE.match(line.strip())
            if m:
                out.append({"code": m.group(1), "title": m.group(2).strip(), "text": m.group(3).strip()})
    return out


def valid_codes():
    return {p["code"] for p in load_passages()}


@tool
def search_lesson(query: str) -> list:
    """search_lesson. Input: câu hỏi của học viên (str). Output: tối đa 3 đoạn
    {"code", "title", "text"} xếp theo độ trùng từ khoá; rỗng nếu không đoạn nào trùng.
    Không tác động ra ngoài (chỉ đọc)."""
    q = set(_tokens(query))
    scored = []
    for p in load_passages():
        words = _tokens(p["title"] + " " + p["text"])
        title_words = set(_tokens(p["title"]))
        score = sum(1 for w in q if w in words) + 2 * sum(1 for w in q if w in title_words)
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored[:3]]


@tool
def get_passage(code: str) -> dict:
    """get_passage. Input: mã đoạn (str, ví dụ "p02"). Output: {"code", "title", "text"}
    hoặc {} nếu mã không có trong bài. Không tác động ra ngoài (chỉ đọc)."""
    for p in load_passages():
        if p["code"] == code:
            return p
    return {}
