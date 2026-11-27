"""Nối model: chỗ DUY NHẤT trong bản chạy thử gọi model AI (nhóm Fightingggg dùng Gemini).

Hợp đồng: call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}.
Token lấy từ usageMetadata của API (tokens_out gồm cả token suy nghĩ nếu có), không ước lượng.
Chế độ giả khi .env chưa có MODEL_PROVIDER (hoặc MODEL_PROVIDER=fake). Không dán API key vào file này.
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()

SHOW_RAW = False   # đổi thành True để in nguyên phản hồi của API khi cần tìm tên trường


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_gemini(system, user):
    """Gọi Gemini đúng một lần (thử lại tối đa 3 lần khi bị giới hạn lượt 429 hoặc 503)."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL_NAME
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0.2},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = None
    for attempt in range(3):
        try:
            data = post_json(url, {"x-goog-api-key": API_KEY}, body)
            break
        except RuntimeError as e:
            if attempt < 2 and (str(e).startswith("HTTP 429") or str(e).startswith("HTTP 503")):
                time.sleep(6 * (attempt + 1))
                continue
            raise
    cands = data.get("candidates") or []
    if not cands:
        raise RuntimeError("Gemini không trả câu trả lời: %s" % json.dumps(data.get("promptFeedback", data), ensure_ascii=False)[:300])
    parts = cands[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    u = data.get("usageMetadata", {})
    return {"text": text,
            "tokens_in": u.get("promptTokenCount", 0),
            "tokens_out": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER == "gemini":
        r = call_gemini(system, user)
    else:
        raise NotImplementedError("chưa viết phần gọi model cho MODEL_PROVIDER=%s trong codebase/ai.py" % MODEL_PROVIDER)
    return {"text": r["text"], "model": MODEL_NAME,
            "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}
