# Reflection — Đào Thị Thu Phương

> Làm ở guide bước 5.3. Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Thành viên nhóm, phụ trách khảo sát, canvas, slide và demo (`TEAMS.md`). Mình đổi nguồn kiểm lại bằng chứng từ phỏng vấn sang khảo sát Google Form để hỏi được nhiều học viên hơn trong thời gian còn lại; viết giả thuyết và hai ngưỡng đúng/sai trước khi xem kết quả (`evidence/hypothesis.md`, commit `f564505`). Form gửi vào nhóm Zalo lớp lúc 16:47 ngày 27/11, thu 24 câu trả lời (`evidence/survey/questions.md`, `evidence/survey/results.csv`). Mình tổng hợp kết quả vào `evidence/summary.md` mục 6, lấy 17 câu hỏi thật ở câu 7 cho bộ câu thử (`evidence/survey/cau-hoi-cau7.md`), cập nhật canvas dòng 4 và làm bộ slide `slides/demo-slides.pptx` (commit `825d7ef`).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Mình dùng Claude Code để soạn câu hỏi khảo sát và viết Apps Script tạo form, đếm kết quả bằng script, và tạo slide bằng python-pptx (chi tiết ở `docs/ai-usage.md`). Chỗ phải sửa: bản slide đầu nói mạnh hơn bằng chứng ("câu hỏi *bị* hỏi tiếp", "nghi câu mẫu"), nên mình sửa lại sau khi Sang đối chiếu số liệu và ghi rõ pain là giả thuyết. Khi bài mẫu tăng từ 8 lên 21 đoạn, slide demo vẫn dùng câu "Fine-tuning khác RAG" làm câu "không có trong bài", trong khi bài mới đã có đoạn p15, nên mình đổi sang câu Llama 3 và chạy lại model để lấy output thật. Hai ngưỡng trong giả thuyết là AI đề xuất, nhóm phải tự chốt. Mình cũng phải che một tên người thật trong câu trả lời khảo sát trước khi đưa lên repo.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   Câu B17 "Làm sao biết hệ thống AI của mình đã tốt hay chưa?" trượt ở lượt 1 (`eval/run-3.csv`): trợ giảng trả lời "Nội dung này không có trong bài", trong khi đoạn p08 nói đúng về bộ câu thử và đếm tỉ lệ đạt. Lỗi không nằm ở model mà ở bước tìm đoạn: tìm theo từ khoá không ra p08, nên model chỉ thấy đoạn không liên quan và nói "không có". Mình học được hai điều. Một, câu trả lời viết trôi chảy, đúng quy tắc vẫn có thể sai nếu bước tìm căn cứ sai, nên phải đo cả bước tìm chứ không chỉ đọc câu trả lời. Hai, nói sai "không có trong bài" cũng nguy hiểm như bịa, vì học viên sẽ tin bài không dạy ý đó; điều này khớp với khảo sát, nơi 7/23 người đã tìm mà không biết đoạn nào nói ý mình hỏi.
