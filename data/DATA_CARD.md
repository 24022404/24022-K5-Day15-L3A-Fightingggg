# Data card: dữ liệu bản chạy thử dùng (nhóm Fightingggg, bản đầu CP2)

## Dataset 1 · Nhật ký chat pre-class (`chat.csv`)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain (`evidence/data-mining.md`). Không dùng để chạy thử và không đưa vào model. |
| Từ đâu | Data BTC cấp, `data/preclass/chat.csv` trong repo đề (đã ẩn danh, mã học viên đã thay) |
| Xử lý những bước gì | Lọc `kind = question` và `agent_id = teaching_assistant`; tính độ dài câu hỏi, thời gian trả lời, khoảng cách giữa hai câu hỏi cùng học viên cùng video (script: `scripts/mine_chat.py`) |
| Số dòng / số đoạn | 1.260 dòng gốc; 1.091 câu hỏi sau lọc, 143 học viên |
| Phiên bản / ngày lấy | Nhật ký 05/11 đến 25/11/2026, lấy ngày 27/11/2026 |
| Nhãn | thật |
| Giới hạn | Chỉ có độ dài, không có nội dung câu hỏi hay trả lời; chỉ cho biết học viên làm gì, không cho biết vì sao. Repo nhóm chỉ chứa số tổng hợp và mã dòng ví dụ, không chép lại file. |

## Dataset 2 · Bài mẫu (`data/lesson_sample.md`)

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ `search_lesson` và `get_passage`; thay cho lời giảng video khi chạy thử |
| Từ đâu | Nhóm tự viết bằng lời của mình về chủ đề nền tảng LLM (cùng chủ đề Day 01, ngày có nhiều câu hỏi nhất trong chat.csv). Không chép tài liệu khoá. |
| Xử lý những bước gì | Chia thành 8 đoạn, mỗi đoạn một mã p01 đến p08 |
| Số dòng / số đoạn | 8 đoạn |
| Phiên bản / ngày lấy | Bản 1, 27/11/2026 |
| Nhãn | `synthetic` (nhóm tự viết) |
| Giới hạn | Ngắn, chỉ một chủ đề, không phải lời giảng thật của khoá. Chưa có thành viên khác đọc lại nội dung: cần 1 người kiểm tay trước CP3. Không phải bằng chứng pain. |

**Data `synthetic` (nhóm tự viết):** viết tay, không sinh bằng script nên không có seed. Số đoạn đã kiểm tay: 0/8 (cần kiểm trước CP3).

## Dataset 3 · Bộ câu thử (`eval/benchmark.csv`)

| | |
|---|---|
| Dùng để làm gì | Đo bản chạy thử theo `eval/metric_spec.yaml` |
| Từ đâu | Nhóm tự viết (12/12 câu `tu_viet`), bám 6 tình huống ở `spec.md` §5; một số câu dựa theo mẫu câu ngắn, mơ hồ thấy trong chat.csv |
| Xử lý những bước gì | Gắn `type` (thuong / kho / tu_choi), `expected` có mã đoạn đúng, `pass_criterion` kiểm được |
| Số dòng / số đoạn | 12 câu: thuong 4 · kho 5 · tu_choi 3 (trong đó 2 câu tấn công) |
| Phiên bản / ngày lấy | Bản 1, 27/11/2026 |
| Nhãn | `synthetic` |
| Giới hạn | 0/12 câu từ lời người dùng hoặc data thật. Kế hoạch: thêm câu từ phỏng vấn học viên (`nguoi_dung: P1…`) để đạt ≥1/3 trước CP3 (10:00 Thứ Bảy 28/11), và tăng lên 20 đến 30 câu. |
