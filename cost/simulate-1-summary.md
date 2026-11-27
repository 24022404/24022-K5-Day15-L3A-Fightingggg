# Tóm tắt mô phỏng simulate-1@20261127-222750

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 9 | 2 | 1700 | 126 | 1.9 | 1.9 |
| dung_vua | 28 | 2 | 1612 | 133 | 1.9 | 1.9 |
| dung_nhieu | 11 | 2 | 1481 | 126 | 1.9 | 1.9 |

Tỉ lệ đạt dùng để tính: 30/30 (100%) — lượt run-4@20261127-212448

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-4.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (143 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00059 | $0.00059 | $0.00030 | $0.6187 | $3.03 | $4.33 | $0.0043 |
| gemini-3.8-flash (vào 0.75 · ra 3.75 $/1M) | $0.0017 | $0.0017 | $0.00084 | $1.75 | $8.59 | $12.27 | $0.0123 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 2/50.
