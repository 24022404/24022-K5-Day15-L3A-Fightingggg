# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, tỉ lệ 25% / 50% / 25% — dùng ít ≈9 · dùng vừa ≈13 · dùng nhiều ≈24 lần hỏi / tháng, mỗi phiên 2 lượt hỏi (4,5 / 6,5 / 12 phiên / tháng). Nguồn: số lần hỏi / tháng lấy đúng từ `spec.md` §2 (khảo sát câu 6, n = 23, `evidence/survey/results.csv`; quy ra tháng × 4,3 tuần *(tự ước tính)*); 2 lượt / phiên từ `chat.csv`: 1.091 câu hỏi, 438 câu hỏi tiếp trong ≤120 giây → 653 chuỗi hỏi, ≈1,67 câu / chuỗi, làm tròn lên 2 *(tự ước tính)*.
- **Số người dùng thật** 3 kịch bản: thấp 143 · cơ sở 700 · cao 1.000. Nguồn: 143 = số học viên đã thực sự hỏi trợ giảng 05–25/11/2026 (`evidence/data-mining.md`); 700 = lớp L3 hơn 700 học viên (README hackathon, như `spec.md` §2); 1.000 *(tự ước tính, thêm các lớp khác của khoá 5)*.
- **Giá** 2 mức model, gói trả phí Standard (USD / 1 triệu token), [trang giá Gemini API](https://ai.google.dev/gemini-api/docs/pricing), xem 27/11/2026: gemini-3.1-flash-lite vào 0,25 · ra 1,50 · gemini-3.8-flash vào 0,75 · ra 3,75 (giá này áp dụng đến 31/12/2026; từ 01/01/2027 là 1,50 / 7,50). Repo đề có `further-reading/model-prices.md` nhưng nhóm không có bản trên máy, nên lấy thẳng từ trang giá chính thức.
- **Tỉ lệ đạt** dùng để tính: 30/30 (100%) — lượt `run-4` (lượt 2). Lưu ý: 100% đo trên chính bộ câu đã dùng để sửa (`eval/report.md` mục 4), nên tỉ lệ thật có thể thấp hơn; nếu lấy lượt 1 (26/30 = 86,7%) thì chi phí / task thành công tăng khoảng 15%.
- Đo token trên model gemini-3.1-flash-lite, tính giá model gemini-3.1-flash-lite và gemini-3.8-flash.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID simulate-1@20261127-222750 · 50 phiên (48 phiên tính trung bình; 2 phiên S036, S048 lỗi `TimeoutError` khi gọi API, khung tự loại) · seed 42

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 9 | 2 | 1700 | 126 | 1.9 | 1.9 |
| dung_vua | 28 | 2 | 1612 | 133 | 1.9 | 1.9 |
| dung_nhieu | 11 | 2 | 1481 | 126 | 1.9 | 1.9 |

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (143 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00059 | $0.00059 | $0.00030 | $0.6187 | $3.03 | $4.33 | $0.0043 |
| gemini-3.8-flash (vào 0.75 · ra 3.75 $/1M) | $0.0017 | $0.0017 | $0.00084 | $1.75 | $8.59 | $12.27 | $0.0123 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**. *(Ở lượt này tỉ lệ đạt đo được là 100% nên hai cột bằng nhau; xem lưu ý ở mục 1.)*

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ≈13 lần × ≈10 phút = ≈130 phút (≈2,2 giờ) học viên đang bỏ vào hỏi và hiểu bài mỗi tháng *(gồm hai ước tính: × 4,3 tuần và 10 phút)*. Đây là thời gian đang bỏ ra, không phải thời gian tiết kiệm được.
- Chi phí / người / tháng (cơ sở, model gemini-3.1-flash-lite): $0,0043 (model mạnh hơn gemini-3.8-flash: $0,0123).
- **Kết luận một dòng — đáng làm không:** chi phí model không phải rào cản (cả lớp 700 người chỉ khoảng $3–9 / tháng); câu hỏi quyết định là trợ giảng có giúp học viên đỡ mất thời gian thật hay không, điều chưa đo được (khảo sát: phàn nàn chính là trả lời chung chung, 11/23).

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Mỗi lượt hỏi tốn ≈800 token vào và ≈65 token ra; phần lớn token vào là 4 đoạn căn cứ đưa vào prompt (sau lượt 2 tăng từ 3 lên 4 đoạn, token vào trung bình +22%, `eval/report.md` mục 3).
- Chưa tính: hosting web demo (Render gói miễn phí), giờ công TA trả lời các câu "không có trong bài".
