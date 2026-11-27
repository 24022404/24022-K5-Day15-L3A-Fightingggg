"""Đếm tín hiệu hành vi từ nhật ký; không suy ra nguyên nhân hay độ đúng của AI.

python scripts/mine_chat.py <đường-dẫn-chat.csv>
python scripts/mine_chat.py <đường-dẫn-chat.csv> --json

Chỉ đọc file, in báo cáo; không ghi dữ liệu gốc, không gọi model. Chỉ dùng thư viện chuẩn.
"""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import sys


REQUIRED = {
    "id", "hv", "channel", "transcript", "kind", "agent_id", "asked_at", "created_at",
    "do_dai_cau_hoi", "do_dai_tra_loi",
}


def load_questions(path):
    """Kiểm dữ liệu dùng để đếm; lỗi chỉ hiện số dòng/cột, không in thông tin cá nhân."""
    raw = Path(path).read_bytes()
    text = raw.decode("utf-8-sig")
    first = next((line for line in text.splitlines() if line.strip()), "")
    delimiter = ";" if first.count(";") > first.count(",") else ","
    reader = csv.DictReader(io.StringIO(text.lstrip("\r\n")), delimiter=delimiter, strict=True)
    headers = reader.fieldnames or []
    if len(headers) != len(set(headers)):
        raise ValueError("Tiêu đề CSV có cột bị trùng")
    missing = REQUIRED - set(reader.fieldnames or [])
    if missing:
        raise ValueError("Thiếu cột: " + ", ".join(sorted(missing)))
    questions, total, seen_ids, timezone_modes = [], 0, set(), set()
    kinds = Counter()
    for row in reader:
        if not any(value for value in row.values()):
            continue
        total += 1
        where = "Dòng CSV %d" % reader.line_num
        if None in row or any(value is None for value in row.values()):
            raise ValueError(where + ": số ô không khớp tiêu đề")
        if not row["kind"].strip():
            raise ValueError(where + ": thiếu kind; không thể xác định điều kiện lọc")
        kinds[row["kind"].strip()] += 1
        if row["kind"].strip() != "question":
            continue
        if not row["agent_id"].strip():
            raise ValueError(where + ": thiếu agent_id của câu hỏi; không thể xác định điều kiện lọc")
        if row["agent_id"].strip() != "teaching_assistant":
            continue
        for key in ("id", "hv", "channel", "asked_at", "created_at"):
            if not row[key].strip():
                raise ValueError(where + ": thiếu " + key)
        code = row["id"].strip()
        if code in seen_ids:
            raise ValueError(where + ": id câu hỏi bị trùng; cần kiểm nguồn trước khi đếm")
        seen_ids.add(code)
        times = []
        for key in ("asked_at", "created_at"):
            try:
                value = datetime.fromisoformat(row[key].strip().replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(where + ": " + key + " phải là thời gian ISO 8601") from None
            timezone_modes.add(value.utcoffset() is not None)
            times.append(value)
        if len(timezone_modes) > 1:
            raise ValueError(where + ": thời gian đang trộn có/không có múi giờ; cần chuẩn hoá nguồn")
        latency = (times[1] - times[0]).total_seconds()
        if latency < 0:
            raise ValueError(where + ": thời gian phản hồi âm; cần kiểm nguồn trước khi đếm")
        lengths = []
        for key in ("do_dai_cau_hoi", "do_dai_tra_loi"):
            try:
                value = int(row[key])
            except ValueError:
                raise ValueError(where + ": " + key + " phải là số nguyên không âm") from None
            if value < 0:
                raise ValueError(where + ": " + key + " phải là số nguyên không âm")
            lengths.append(value)
        questions.append({"id": code, "learner": row["hv"].strip(), "channel": row["channel"].strip(),
                          "video": row["transcript"].strip(),
                          "asked": times[0], "latency_s": latency,
                          "question_length": lengths[0], "answer_length": lengths[1]})
    if not questions:
        raise ValueError("Không có câu hỏi thoả kind=question và agent_id=teaching_assistant")
    return questions, total, hashlib.sha256(raw).hexdigest(), dict(sorted(kinds.items()))


def analyze(path, examples=8):
    questions, total, digest, kinds = load_questions(path)
    short = [q for q in questions if q["question_length"] <= 10]
    fast = [q for q in questions if q["latency_s"] < 0.5]
    groups = defaultdict(list)
    for q in questions:
        if q["channel"] == "video_question" and q["video"]:
            groups[q["learner"], q["video"]].append(q)
    followups, pairs = [], []
    for group in groups.values():
        ordered = sorted(group, key=lambda q: q["asked"])
        for previous, current in zip(ordered, ordered[1:]):
            gap = (current["asked"] - previous["asked"]).total_seconds()
            if gap <= 120:
                followups.append(current)
                pairs.append({"previous_id": previous["id"], "current_id": current["id"], "gap_s": gap})
    n = len(questions)
    video_questions = [q for q in questions if q["channel"] == "video_question"]
    video_n = len(video_questions)
    # Chỉ xuất mã dòng/độ dài/khoảng thời gian, không xuất hv, video, nội dung hay thời điểm cá nhân.
    samples = [{key: q[key] for key in ("id", "question_length", "answer_length", "latency_s")}
               for q in sorted(fast, key=lambda q: (q["question_length"], q["latency_s"], q["id"]))[:examples]]
    return {
        "source_file": Path(path).name, "source_sha256": digest,
        "source_kinds": kinds,
        "filter": {"kind": "question", "agent_id": "teaching_assistant"},
        "total_rows": total, "questions": n, "learners": len({q["learner"] for q in questions}),
        "channels": dict(sorted(Counter(q["channel"] for q in questions).items())),
        "period": {"from": min(q["asked"] for q in questions).date().isoformat(),
                   "to": max(q["asked"] for q in questions).date().isoformat()},
        "short_questions": {"count": len(short), "percent": 100 * len(short) / n},
        "fast_responses": {"count": len(fast), "percent": 100 * len(fast) / n,
                           "questions_at_most_15_chars": sum(q["question_length"] <= 15 for q in fast),
                           "common_answer_lengths": [{"length": length, "count": count}
                               for length, count in Counter(q["answer_length"] for q in fast).most_common(3)]},
        "followups": {"count": len(followups), "percent": 100 * len(followups) / n,
                      "learners": len({q["learner"] for q in followups}),
                      "eligible_questions": sum(len(group) for group in groups.values())},
        "video_only": {"questions": video_n, "learners": len({q["learner"] for q in video_questions}),
                       "short_questions": sum(q["question_length"] <= 10 for q in video_questions),
                       "fast_responses": sum(q["latency_s"] < 0.5 for q in video_questions),
                       "followups": len(followups),
                       "followup_percent": 100 * len(followups) / video_n if video_n else None},
        "data_quality": {"missing_video_count": sum(not q["video"] for q in questions),
                         "missing_video_ids": [q["id"] for q in questions if not q["video"]],
                         "video_questions_missing_transcript": sum(not q["video"] for q in video_questions)},
        "fast_response_examples": samples, "followup_examples": pairs[:examples],
    }


def print_report(report):
    print("Nguồn: %s | SHA-256: %s" % (report["source_file"], report["source_sha256"]))
    print("Tổng dòng: %d | Câu hỏi sau lọc: %d | Học viên: %d" %
          (report["total_rows"], report["questions"], report["learners"]))
    print("Khoảng ngày hỏi: %(from)s đến %(to)s" % report["period"])
    print("Kênh câu hỏi: " + json.dumps(report["channels"], ensure_ascii=False))
    for label, key in (("A. Câu hỏi <=10 ký tự", "short_questions"),
                       ("B. Phản hồi 0 đến dưới 0,5 giây", "fast_responses"),
                       ("C. Hỏi tiếp <=120 giây cùng học viên/video", "followups")):
        metric = report[key]
        print("%s: %d/%d = %.1f%%" % (label, metric["count"], report["questions"], metric["percent"]))
    print("B: câu hỏi <=15 ký tự: %d/%d" %
          (report["fast_responses"]["questions_at_most_15_chars"], report["fast_responses"]["count"]))
    print("B: độ dài trả lời phổ biến: " + json.dumps(report["fast_responses"]["common_answer_lengths"]))
    print("C: học viên có ít nhất một lượt hỏi tiếp: %d/%d" % (report["followups"]["learners"], report["learners"]))
    print("C: %d câu thuộc kênh video và đủ mã để nhóm; %d câu không có mã video vẫn giữ trong mẫu số tổng %d" %
          (report["followups"]["eligible_questions"], report["data_quality"]["missing_video_count"], report["questions"]))
    video = report["video_only"]
    if video["questions"]:
        print("Riêng kênh video: %d/%d lượt hỏi tiếp = %.1f%% (mẫu số khác bảng chính)" %
              (video["followups"], video["questions"], video["followup_percent"]))
    print("\nVí dụ phản hồi nhanh (mã dòng, độ dài hỏi/trả lời, giây):")
    for row in report["fast_response_examples"]:
        print("{id}: {question_length} / {answer_length} / {latency_s}".format(**row))
    print("\nVí dụ cặp hỏi tiếp (mã trước -> mã sau, khoảng cách giây):")
    for row in report["followup_examples"]:
        print("{previous_id} -> {current_id}: {gap_s}".format(**row))
    print("\nGiới hạn: độ dài và thời gian không chứng minh sự hài lòng, độ đúng, thiếu trích dẫn hay nguyên nhân hỏi tiếp.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="data/preclass/chat.csv")
    parser.add_argument("--json", action="store_true", help="in JSON để đối chiếu số liệu; không tự ghi file")
    parser.add_argument("--examples", type=int, default=8, help="số ví dụ mỗi nhóm (mặc định 8)")
    args = parser.parse_args(argv)
    if args.examples < 1:
        parser.error("--examples phải >=1")
    try:
        report = analyze(args.path, args.examples)
    except (OSError, ValueError, csv.Error) as error:
        print("Không thể phân tích: %s" % error, file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    sys.exit(main())
