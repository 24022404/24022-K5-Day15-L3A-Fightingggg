"""Máy chủ web: phục vụ giao diện (static/) và API cho trợ giảng.

Chạy local:  uvicorn server:app --port 8000
Render:      uvicorn server:app --host 0.0.0.0 --port $PORT   (không Docker)
Biến môi trường: MODEL_PROVIDER, MODEL_NAME, API_KEY (giống bản Streamlit).
"""
import json
import os
import re
import sys
import time
from collections import defaultdict, deque

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "codebase"))

from fastapi import FastAPI, HTTPException, Request  # noqa: E402
from fastapi.responses import FileResponse, JSONResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel  # noqa: E402

import tracing  # noqa: E402
from agent import answer, NO_ANSWER, REFUSE_REPLY  # noqa: E402
from tools import load_passages  # noqa: E402

app = FastAPI(title="Lớp học AI20K - trợ giảng", docs_url=None, redoc_url=None)
PASSAGES = load_passages()
CODES = {p["code"] for p in PASSAGES}
EXTRA = json.load(open(os.path.join(BASE, "data", "lesson_extra.json"), encoding="utf-8"))

LIMIT, WINDOW = 40, 3600  # mỗi IP tối đa 40 câu hỏi / giờ (giữ hạn mức API miễn phí)
_hits = defaultdict(deque)


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


class Ask(BaseModel):
    q: str


class Login(BaseModel):
    username: str
    password: str


class Grade(BaseModel):
    answers: list


# Tài khoản demo: đặt biến môi trường DEMO_USERS="ten:matkhau,ten2:matkhau2" để đổi. Mặc định hocvien / ai20k2026.
USERS = {}
for part in (os.environ.get("DEMO_USERS") or "hocvien:ai20k2026").split(","):
    if ":" in part:
        u, pw = part.split(":", 1)
        USERS[u.strip()] = pw.strip()
QUIZ = json.load(open(os.path.join(BASE, "data", "quiz.json"), encoding="utf-8")) if os.path.exists(os.path.join(BASE, "data", "quiz.json")) else []


@app.post("/api/login")
def login(body: Login):
    u = body.username.strip()
    if USERS.get(u) is None or USERS[u] != body.password:
        return JSONResponse({"error": "Sai tên đăng nhập hoặc mật khẩu."}, status_code=401)
    return {"ok": True, "username": u}


@app.get("/api/quiz")
def quiz_list():
    """Danh sách bài trắc nghiệm, KHÔNG kèm đáp án."""
    return [{"id": q["id"], "title": q["title"], "desc": q["desc"],
             "questions": [{"q": x["q"], "options": x["options"]} for x in q["questions"]]} for q in QUIZ]


@app.post("/api/quiz/{qid}/grade")
def quiz_grade(qid: str, body: Grade):
    """Chấm bài ở máy chủ; chỉ trả đáp án sau khi nộp."""
    quiz = next((q for q in QUIZ if q["id"] == qid), None)
    if not quiz:
        raise HTTPException(404, "Không có bài này")
    res, score = [], 0
    for i, x in enumerate(quiz["questions"]):
        a = body.answers[i] if i < len(body.answers) else None
        ok = a == x["answer"]
        score += ok
        res.append({"correct": ok, "chosen": a, "answer": x["answer"], "explain": x["explain"], "code": x["code"]})
    return {"score": score, "total": len(quiz["questions"]), "results": res}


@app.get("/api/lesson")
def lesson():
    return {"passages": [dict(p, **EXTRA.get(p["code"], {"example": "", "links": []})) for p in PASSAGES]}


@app.get("/api/health")
def health():
    return {"ok": True, "provider": os.environ.get("MODEL_PROVIDER") or "fake"}


@app.post("/api/ask")
def ask(body: Ask, request: Request):
    q = body.q.strip()
    if not q:
        raise HTTPException(400, "Câu hỏi trống")
    if len(q) > 600:
        raise HTTPException(400, "Câu hỏi quá dài (tối đa 600 ký tự)")
    ip = (request.headers.get("x-forwarded-for") or (request.client.host if request.client else "?")).split(",")[0].strip()
    now = time.time()
    dq = _hits[ip]
    while dq and now - dq[0] > WINDOW:
        dq.popleft()
    if len(dq) >= LIMIT:
        return JSONResponse({"error": "Đã hết lượt hỏi trong giờ này, vui lòng quay lại sau."}, status_code=429)
    dq.append(now)
    tracing.begin("web")
    t0 = time.time()
    try:
        out = answer(q)["output"]
    except Exception as e:  # lỗi gọi model
        out = "Lỗi khi gọi model: %s" % e
    summary, _ = tracing.end()
    summary = summary or {}
    codes = [c for c in dict.fromkeys(re.findall(r"\bp\d{2}\b", out)) if c in CODES]
    return {
        "out": out, "kind": classify(out), "codes": codes,
        "models": summary.get("models", []), "tokens_in": summary.get("tokens_in", 0),
        "tokens_out": summary.get("tokens_out", 0), "sec": round(time.time() - t0, 1),
    }


@app.get("/files/{name}")
def files(name: str):
    allowed = {"lesson_sample.md", "DATA_CARD.md"}
    if name not in allowed:
        raise HTTPException(404)
    return FileResponse(os.path.join(BASE, "data", name), media_type="text/markdown; charset=utf-8", filename=name)


@app.get("/")
def index():
    return FileResponse(os.path.join(BASE, "static", "index.html"))


app.mount("/static", StaticFiles(directory=os.path.join(BASE, "static")), name="static")
