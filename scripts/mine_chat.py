"""Đếm tín hiệu pain từ chat.csv (trợ giảng dưới video). Chạy: python scripts/mine_chat.py data/preclass/chat.csv"""
import sys
import pandas as pd

path = sys.argv[1] if len(sys.argv) > 1 else "data/preclass/chat.csv"
c = pd.read_csv(path)
q = c[(c.kind == "question") & (c.agent_id == "teaching_assistant")].copy()
q["t0"] = pd.to_datetime(q.asked_at)
q["t1"] = pd.to_datetime(q.created_at)
q["lat"] = (q.t1 - q.t0).dt.total_seconds()
N = len(q)
print(f"N câu hỏi gửi trợ giảng = {N}, số học viên = {q.hv.nunique()}")

short = q[q.do_dai_cau_hoi <= 10]
print(f"A. Câu hỏi <=10 ký tự: {len(short)}/{N} = {len(short)/N:.1%}")

fast = q[q.lat < 0.5]
print(f"B. Trả lời tức thì (<0.5s, nghi mẫu có sẵn): {len(fast)}/{N} = {len(fast)/N:.1%}")
print(f"   trong đó câu hỏi <=15 ký tự: {(fast.do_dai_cau_hoi<=15).sum()}/{len(fast)}")
print("   độ dài câu trả lời phổ biến nhất:", fast.do_dai_tra_loi.value_counts().head(3).to_dict())

q = q.sort_values(["hv", "transcript", "t0"])
q["gap"] = q.groupby(["hv", "transcript"]).t0.diff().dt.total_seconds()
rep = q[q.gap <= 120]
print(f"C. Hỏi tiếp trong <=120s cùng học viên cùng video: {len(rep)}/{N} = {len(rep)/N:.1%}")
print(f"   số học viên có >=1 lần: {rep.hv.nunique()}/{q.hv.nunique()}")

print("\nVí dụ (id, hv, video, độ dài hỏi, độ dài trả lời, giây trả lời):")
cols = ["id", "hv", "transcript", "do_dai_cau_hoi", "do_dai_tra_loi", "lat"]
print(fast.sort_values("do_dai_cau_hoi")[cols].head(8).to_string(index=False))
