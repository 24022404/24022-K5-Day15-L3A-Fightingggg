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
STOP = set("la gi va the nao khac cua nhu co khong nay do cho duoc trong mot nhung de em minh toi ban hay vi sao sao thi voi tu o da lam biet giup sanh".split())


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


# Từ gợi ý mỗi đoạn: cách học viên hay gọi, để tìm được cả khi câu hỏi không dùng đúng từ trong bài.
TAGS = {
    "p01": "mô hình ngôn ngữ lớn llm sinh văn bản dự đoán chữ",
    "p02": "token mẩu chữ đơn vị tính chi phí giá tiền",
    "p03": "cửa sổ ngữ cảnh context window giới hạn độ dài quá dài",
    "p04": "temperature nhiệt độ ngẫu nhiên đa dạng ổn định",
    "p05": "bịa hallucination nói sai ảo giác sai sự thật",
    "p06": "prompt viết câu lệnh hướng dẫn ví dụ mẫu định dạng",
    "p07": "rag truy xuất tìm kiếm tài liệu kho tri thức",
    "p08": "đánh giá kiểm tra chất lượng tốt hay chưa đo lường bộ câu thử tỉ lệ đạt chấm điểm",
    "p09": "học dự đoán chữ tiếp theo xác suất tiền huấn luyện",
    "p10": "kiến trúc transformer attention chú ý vector lớp",
    "p11": "huấn luyện quy mô lớn dữ liệu máy tính chi phí",
    "p12": "tinh chỉnh theo chỉ dẫn instruction tuning làm theo yêu cầu",
    "p13": "căn chỉnh alignment an toàn hữu ích phù hợp giá trị con người",
    "p14": "rlhf phản hồi con người xếp hạng phần thưởng",
    "p15": "fine-tuning tinh chỉnh khác rag so sánh chọn cách nào",
    "p16": "prompt hệ thống system prompt mẫu template",
    "p17": "học trong ngữ cảnh few-shot zero-shot ví dụ trong prompt",
    "p18": "chuỗi suy luận chain of thought chia nhỏ bài toán từng bước",
    "p19": "rag thực tế vector cơ sở dữ liệu truy xuất ba bước",
    "p20": "giải mã greedy beam lấy mẫu top-k top-p temperature",
    "p21": "ngữ cảnh dài chuỗi dài mở rộng cửa sổ",
}


@tool
def search_lesson(query: str) -> list:
    """search_lesson. Input: câu hỏi của học viên (str). Output: tối đa 4 đoạn
    {"code", "title", "text"} xếp theo độ trùng từ khoá; rỗng nếu không đoạn nào trùng.
    Từ hiếm trong bài tính điểm cao hơn từ phổ biến; câu hỏi nhắc đủ tên đoạn thì cộng thêm.
    Không tác động ra ngoài (chỉ đọc)."""
    import math
    q = set(_tokens(query))
    passages = load_passages()
    docs = []
    for p in passages:
        title_words = set(_tokens(p["title"]))
        words = set(_tokens(p["title"] + " " + p["text"] + " " + TAGS.get(p["code"], "")))
        docs.append((p, title_words, words))
    n = len(docs)
    df = {}
    for _, _, words in docs:
        for w in words:
            df[w] = df.get(w, 0) + 1
    scored = []
    for p, title_words, words in docs:
        score = 0.0
        for w in q:
            if w in words:
                idf = math.log(1 + n / df[w])
                score += idf * (3 if w in title_words else 1)
        if title_words and title_words <= q:
            score += 4
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored[:4]]


@tool
def get_passage(code: str) -> dict:
    """get_passage. Input: mã đoạn (str, ví dụ "p02"). Output: {"code", "title", "text"}
    hoặc {} nếu mã không có trong bài. Không tác động ra ngoài (chỉ đọc)."""
    for p in load_passages():
        if p["code"] == code:
            return p
    return {}
