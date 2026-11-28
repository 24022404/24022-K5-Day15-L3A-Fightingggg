# Reflection — Nguyễn Đức Minh

1. **Vai trò và phần mình làm**

   Mình là trưởng nhóm Fightingggg, phụ trách điều phối và bản chạy thử. Phần việc gồm `codebase/` (luồng 4 bước trong `agent.py`, tìm đoạn trong `tools.py`), web `server.py` và `static/`, deploy lên Render, chạy eval lượt 1 và lượt 2 (`eval/run-3.csv`, `eval/run-4.csv`), viết `eval/report.md` và spec §2 đến §7.
   Các commit chính: `6a7772a` (agent, tools), `3734a8e` (web 21 trang, bộ 30 câu), `5d175a2` (lượt 1 và lượt 2), `5509576` (giao diện v4).

2. **AI hỗ trợ mình thế nào**

   Mình dùng Claude để viết giao diện web và mã `codebase/`, soạn `expected` và `pass_criterion` cho 11 câu thật của học viên, và nháp cột `pass` cho `run-3`, `run-4`.
   Chỗ phải sửa lại: mình tự đọc từng output rồi mới chốt cột `pass`, không nhận bản nháp của AI. Mình cũng phải nói thẳng trong báo cáo rằng bản sửa lượt 2 được viết sau khi thấy lỗi trên chính bộ câu này, nên 30/30 không nên đọc là kết quả trên câu chưa thấy.

3. **Một câu thử trượt và điều mình học được**

   Câu B17 "Làm sao biết hệ thống AI của mình đã tốt hay chưa?" trượt ở lượt 1: trợ giảng trả lời "không có trong bài" trong khi p08 nói đúng về bộ câu thử và tỉ lệ đạt. Lỗi nằm ở bước tìm đoạn: từ khoá của câu hỏi không trùng chữ trong p08 nên p08 không được đưa cho model.
   Mình sửa bằng cách lấy 4 đoạn thay vì 3, thêm từ gợi ý và trọng số từ hiếm. Bài học: lỗi "nói không có" làm học viên tin bài không dạy ý đó, nặng hơn lỗi trả lời dài dòng; và tìm theo từ khoá vẫn có thể sót khi hỏi bằng cách nói khác, nên là điểm yếu còn lại (`eval/report.md` mục 4).
