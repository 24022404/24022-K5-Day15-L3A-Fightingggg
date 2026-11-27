# Canvas — Fightingggg · Track A

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track A (EdTech) · A1 Tutor cho LMS và trang pre-class |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Học viên AI20K khoá 5 tự học bài trước giờ lên lớp trên trang pre-class |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Giả thuyết: học viên tự học pre-class có thể khó kiểm câu trả lời dựa vào đoạn nào, phải dò lại tài liệu hoặc hỏi thêm; nhật ký chưa chứng minh nguyên nhân hoặc thời gian mất |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | Đã đối chiếu `chat.csv`: 1.091 câu hỏi gửi trợ giảng, gồm 1.090 câu kênh video và 1 câu kênh phiên học; 70/1.091 câu ≤10 ký tự (6,4%), 26/1.091 phản hồi <0,5 giây (2,4%), 438/1.091 lượt hỏi tiếp ≤120 giây cùng học viên/video (40,1%, ở 91/143 học viên). Riêng kênh video C = 438/1.090 = 40,2%. Có 8 dòng và 5 cặp ví dụ trong `evidence/data-mining.md`; không có nội dung để trích lời học viên. Khảo sát Google Form (Phương, 24 học viên khoá 5, `evidence/summary.md` mục 6): trong 23 người đã từng hỏi trợ giảng, 12/23 (52,2%) có tìm nhưng không biết đoạn nào hoặc tin luôn không kiểm; 10/23 hỏi tiếp vì câu trả lời chưa đủ ý. Trích dẫn: "Trợ giảng trả lời hơi chung chung nên mình vẫn phải tua lại video để đối chiếu ngữ cảnh." (R05). Ngược giả thuyết: 11/23 tìm được đúng đoạn; phàn nàn nhiều nhất là câu trả lời không đúng trọng tâm (11/23) |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Một học viên hỏi một câu dưới bài; trợ giảng quyết định trả lời kèm mã đoạn, hỏi lại, hay nói "không có trong bài"; học viên tự kiểm bằng cách mở đúng đoạn |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI tự trả lời khi có đoạn căn cứ, chuyển TA khi không có. Sai thì học viên học sai một ý, nhưng có mã đoạn nên tự kiểm được, sửa rẻ |
| 7 | Phân công có tên | Minh: prototype, run.py, spec · Sang: số liệu pain, evidence · Phương: khảo sát, canvas, slide · Long: bài mẫu, benchmark, data card |
| — | *(CP2)* Đã đổi gì so với CP1 | Lát cắt giữ nguyên, thêm số bằng chứng đầu từ data thật (dòng 4); chốt bài mẫu Day 01 tự viết 8 đoạn, 12 câu thử, 4 metric, chuẩn "đạt" ≥85% và 100% câu tu_choi; thiết kế workflow cố định 4 bước (spec §4) |
| — | *(CP3)* Đã đổi gì so với CP2 | Lát cắt và chuẩn "đạt" giữ nguyên. Bài mẫu mở rộng từ 8 lên 21 đoạn (p01 đến p21); bộ câu thử 30 câu, trong đó 11 câu thật của học viên từ khảo sát (36,7%); thêm bằng chứng khảo sát 24 học viên (`evidence/summary.md` mục 6); chạy thật 2 lượt, 26/30 rồi 30/30 sau khi sửa bước tìm đoạn và cách từ chối (`eval/report.md`); có bản web chạy thật trên Render. Chi tiết ở nhật ký `spec.md` §10 |
