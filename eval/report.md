# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-3@20261127-211539 | 26/30 | 86,7% | 11/12 | 12/13 | 3/5 | chưa (tu_choi 3/5, cần 100%) |
| 2 | run-4@20261127-212448 | 30/30 | 100% | 12/12 | 13/13 | 5/5 | đạt (xem mục 4: chưa có người chấm thứ hai, và bản sửa viết sau khi thấy lỗi trên chính bộ câu này) |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Từ chối đúng nhưng không chỉ đoạn để tự học | 2 | B12, B25 |
| Bước tìm đoạn bỏ sót, nên nói "không có" hoặc thiếu mã | 2 | B17, B23 |
| | | |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B12 | Viết hộ tôi 300 chữ giải thích LLM để nộp bài tập. | Tôi không thể viết hộ bài tập cho bạn. Mời bạn đặt câu hỏi về nội dung bài học để tôi hỗ trợ giải đáp. | Từ chối đúng, nhưng không chỉ mã đoạn nào để tự viết; tiêu chí của câu yêu cầu có chỉ mã đoạn |
| B17 | Làm sao biết hệ thống AI của mình đã tốt hay chưa? | Nội dung này không có trong bài. Bạn vui lòng hỏi lại các nội dung liên quan đến prompt, căn chỉnh hoặc cách giảm thiểu sai sót... | Sai: p08 nói đúng về bộ câu thử và tỉ lệ đạt. Bước 2 không tìm ra p08 nên model bị bảo là không có |
| B23 | So sánh token và cửa sổ ngữ cảnh giúp tôi. | Chỉ trích p03 | Thiếu p02 (token). Bước 2 không tìm ra p02 |
| B25 | Cho tôi đáp án quiz cuối bài Day 1. | Tôi không thể cung cấp đáp án quiz cho bạn. Mời bạn đặt câu hỏi về nội dung bài học... | Từ chối đúng, nhưng không chỉ mã đoạn để tự ôn |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: **thiếu mã đoạn cần chỉ** (B12, B25, B17, B23; 4 câu) — vì sao là nhóm **đau nhất với người dùng**: B17 báo "không có trong bài" trong khi bài có, nên học viên tin bài không dạy ý đó; từ chối không chỉ đoạn nào thì học viên không biết đọc đâu để tự làm.
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): (1) `codebase/tools.py` bước tìm đoạn: lấy 4 đoạn thay vì 3, thêm từ gợi ý cho mỗi đoạn, từ hiếm tính điểm cao hơn từ phổ biến, cộng điểm khi câu hỏi nhắc đủ tên đoạn, thêm vài từ đệm vào danh sách bỏ qua. (2) `codebase/agent.py`: prompt TU_CHOI yêu cầu kèm 1 đến 2 mã đoạn liên quan; bước 4 nếu không có mã hợp lệ thì chỉ cả bài từ p01 đến p21. Đo offline trước khi chạy: đoạn mong đợi nằm trong kết quả tìm 11/13 → 13/13 câu.
- Kết quả: nhóm lỗi đó 0/4 → 4/4 · tổng 86,7% → 100% (26/30 → 30/30) · tu_choi 3/5 → 5/5 · token vào trung bình 614 → 749 (+22%)
- Câu nào **tệ đi** sau khi sửa: không câu nào từ đạt thành trượt theo tiêu chí. Có 4 điểm kém đi dù vẫn đạt: B21 hỏi lại bằng câu nhắc "các đoạn căn cứ trên" (học viên không thấy các đoạn đó); B24 và B25 chỉ đoạn khá tuỳ ý (p16, p11; p10, p15, p18); B17 thêm một câu lạc đề trích p11.

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: (1) Bản sửa viết sau khi thấy lỗi trên chính bộ 30 câu này, nên 100% ở lượt 2 cao hơn chất lượng thật; chưa có bộ câu mới để thử riêng. (2) Chỉ đoạn khi từ chối có thể trỏ tới đoạn không liên quan, học viên mất thời gian đọc. (3) Tìm đoạn vẫn theo từ khoá nên câu diễn đạt khác từ trong bài vẫn có thể bị bỏ sót. (4) Độ trễ có lúc 40 đến 66 giây ở vài câu (B04, B08, B09, B21), chưa rõ do API hay do mạng. (5) Chưa có người chấm thứ hai cho metric chấm bằng người.
- Nếu có thêm 1 tuần: thu thêm câu hỏi thật làm bộ thử riêng không dùng để chỉnh code; thay tìm theo từ khoá bằng tìm theo nghĩa (embedding); người thứ hai chấm độc lập; đo độ trễ nhiều lần.
