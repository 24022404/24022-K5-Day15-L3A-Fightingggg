# Data card: dữ liệu bản chạy thử dùng (nhóm Fightingggg, bản đầu CP2)

## Dataset 1 · Nhật ký chat pre-class (`chat.csv`)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain (`evidence/data-mining.md`). Không dùng để chạy thử và không đưa vào model. |
| Từ đâu | Data BTC cấp, `data/preclass/chat.csv` trong repo đề (đã ẩn danh, mã học viên đã thay) |
| Xử lý những bước gì | Kiểm dữ liệu và lọc `kind = question`, `agent_id = teaching_assistant`; đếm độ dài nguồn và thời gian phản hồi trên tập chính; phép hỏi tiếp chỉ nhóm `video_question` có mã video theo học viên/video (script: `scripts/mine_chat.py`) |
| Số dòng / số đoạn | 1.260 dòng gốc; 1.091 câu hỏi sau lọc từ 143 học viên, gồm 1.090 `video_question` và 1 `session_question` |
| Phiên bản / ngày lấy | Nhật ký 05/11 đến 25/11/2026, lấy ngày 27/11/2026 |
| Nhãn | thật |
| Giới hạn | Chỉ có độ dài, không có nội dung câu hỏi hay trả lời; chỉ cho biết học viên làm gì, không cho biết vì sao. Repo nhóm chỉ chứa số tổng hợp và mã dòng ví dụ, không chép lại file. |

**Đối chiếu nguồn ngày 27/11/2026:** file cục bộ `data/preclass/chat.csv` có 260.259 byte, SHA-256 `3331daa0356c1c1863e8b0dd8e74581071d425d9d956e24a98b6f0f2166d304c`. Hai phép đếm độc lập Python/PowerShell xác nhận các số trên. `C00189` thuộc kênh phiên học và không có `transcript`; không tự coi đây là một câu hỏi dưới video mất mã. Dòng này ở mẫu số chính 1.091, không vào nhóm cùng video; cả 1.090 câu kênh video đều có mã. C = 438/1.091 (40,1%) trên tập chính, hoặc 438/1.090 (40,2%) khi chỉ xét kênh video. File nguồn được Git bỏ qua, không đưa nguyên file vào bản nộp. Xem `evidence/verification.md`; kiểm bằng công cụ không thay cho xác nhận người trong nhóm đã rà.

## Dataset 2 · Bài mẫu (`data/lesson_sample.md`)

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ `search_lesson` và `get_passage`; thay cho lời giảng video khi chạy thử |
| Từ đâu | p01 đến p08: nhóm tự viết. p09 đến p21: nhóm viết lại bằng lời của mình từ (1) sách mở "Foundations of Large Language Models" của Tong Xiao và Jingbo Zhu (arXiv 2501.09223, giấy phép CC BY-NC 4.0) và (2) bài khảo sát "A Survey of Large Language Models" của Zhao và cộng sự (arXiv 2303.18223; tác giả giữ bản quyền hình và bảng nên chỉ dùng ý chính bằng chữ). Mỗi đoạn p09 đến p21 ghi mục nguồn ở cuối. Không chép nguyên văn, không dùng hình, bảng hay công thức của tác giả. Không chép tài liệu khoá. |
| Xử lý những bước gì | Chia thành 21 đoạn, mỗi đoạn một mã p01 đến p21, xếp thành 3 module (1: p01-p08, 2: p09-p15, 3: p16-p21) |
| Số dòng / số đoạn | 21 đoạn |
| Phiên bản / ngày lấy | Bản 2, 27/11/2026 (đã đọc sách và khảo sát ngày 27/11/2026) |
| Nhãn | `synthetic` (nhóm tự viết, p09 đến p21 viết lại từ nguồn mở) |
| Giới hạn | Ngắn, chỉ một chủ đề, không phải lời giảng thật của khoá. Chưa có thành viên khác đọc lại nội dung: cần 1 người kiểm tay trước CP3. Không phải bằng chứng pain. |

**Data `synthetic` (nhóm tự viết):** viết tay, không sinh bằng script nên không có seed. Số đoạn đã kiểm tay: 0/21 (cần kiểm trước CP3, nhất là p09 đến p21 so với sách nguồn).

**Nội dung mở rộng trong bản web (không thuộc Dataset 2):** mỗi trang bài trong `streamlit_app.py` có thêm một ví dụ nhóm tự viết và 1 đến 3 liên kết "Đọc thêm" tới nguồn công khai trên web (tìm ngày 27/11/2026: Harvard Chan, IBM, Cloudflare, AWS, Mistral, web.dev, Thoughtworks, Arize, Viblo, Zapier và các trang tương tự). Chỉ có liên kết và tiêu đề, không chép nội dung. Trợ giảng chỉ dựa vào 8 đoạn của Dataset 2, không dựa vào ví dụ hay liên kết này, nên bộ câu thử và chuẩn "đạt" không đổi.

## Dataset 3 · Bộ câu thử (`eval/benchmark.csv`)

| | |
|---|---|
| Dùng để làm gì | Đo bản chạy thử theo `eval/metric_spec.yaml` |
| Từ đâu | Nhóm tự viết (25/25 câu `tu_viet`; vài câu ghi thêm nguồn FAQ công khai làm gợi ý chủ đề, không phải lời học viên), bám 6 tình huống ở `spec.md` §5; một số câu dựa theo mẫu câu ngắn, mơ hồ thấy trong chat.csv |
| Xử lý những bước gì | Gắn `type` (thuong / kho / tu_choi), `expected` có mã đoạn đúng, `pass_criterion` kiểm được |
| Số dòng / số đoạn | 30 câu: thuong 14 · kho 11 · tu_choi 5 (trong đó 3 câu tấn công) |
| Phiên bản / ngày lấy | Bản 2, 27/11/2026 (bản 1 có 25 câu, B07 đổi nhãn từ kho sang thuong và B19 đổi câu hỏi vì bài mới đã trả lời được; thêm B26 đến B30) |
| Nhãn | `synthetic` |
| Giới hạn | 0/30 câu từ lời người dùng hoặc data thật. Kế hoạch: thu câu hỏi thật từ bạn học ngoài nhóm (`nguoi_dung: P1…`) để đạt ≥1/3 trước CP3 (10:00 Thứ Bảy 28/11); chưa làm được thì khai thật là chưa đạt. |
