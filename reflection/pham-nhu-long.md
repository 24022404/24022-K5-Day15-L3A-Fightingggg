# Reflection — Phạm Như Long

1. **Vai trò và phần mình làm**

   Mình phụ trách bộ câu thử và dữ liệu bài học: bộ 30 câu (12 thuong, 13 kho, 5 tu_choi, trong đó 11 câu thật từ khảo sát học viên), `data/DATA_CARD.md` và `eval/README.md`. Mình cũng là người thứ hai chấm độc lập: ngày 27/11 lúc 22:02 mình chấm 5 output của lượt 2 (B12, B17, B21, B24, B25) trước khi xem cột `pass`, kết quả khớp 5/5 (`eval/cham-nguoi-thu-hai.md`). Commit của mình: `04a510a`.

2. **AI hỗ trợ mình thế nào**

   Claude soạn `expected` và `pass_criterion` cho 11 câu thật; câu hỏi được chép nguyên văn từ `evidence/survey/results.csv`, không sửa. Mình đọc lại các `expected` đó rồi mới giữ. Khi chấm độc lập mình không dùng AI và không hỏi người đã chấm.
   Chỗ phải sửa: data card ghi "đã kiểm tay 21/21" trong khi chưa ai đọc lại nguồn p09 đến p21 (chỉ có AI đối chiếu 13/13). Mình đã sửa lại thành 0/21 để khớp với `data/KIEM-NGUON.md` và README.

3. **Một câu thử trượt và điều mình học được**

   Câu B23 "So sánh token và cửa sổ ngữ cảnh giúp tôi" trượt ở lượt 1: trợ giảng chỉ trích p03 mà thiếu p02 (token), vì bước tìm đoạn không tìm ra p02. Câu này nằm trong bộ câu thử nên lỗi lộ ra ngay.
   Điều mình học: câu hỏi so sánh hai khái niệm cần đưa được đoạn của cả hai khái niệm, nên câu thử loại "kho" phải có tiêu chí ghi rõ cần những mã đoạn nào. Lượt 2 đạt B23 sau khi nhóm tăng số đoạn tìm lên 4, nhưng bản sửa viết sau khi thấy lỗi nên không nên coi 30/30 là kết quả trên câu chưa thấy.
