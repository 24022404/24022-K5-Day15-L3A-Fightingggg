# Reflection — Nguyễn Ngọc Sang

1. **Vai trò và phần mình làm**

   Em phụ trách đào số liệu pain từ nhật ký và tổng hợp bằng chứng cho nhóm Fightingggg.  
   Phần việc gồm [script đếm](../scripts/mine_chat.py), [báo cáo đào dữ liệu](../evidence/data-mining.md), [bản tổng hợp evidence](../evidence/summary.md) và các công cụ kiểm chứng; đã nộp trong commit `dedfcac` — `Sangcommit`.  
   Từ 1.260 bản ghi, tập phân tích có 1.091 câu hỏi gửi trợ giảng từ 143 học viên; ba số chính là 70 câu ngắn, 26 phản hồi dưới 0,5 giây và 438 lượt hỏi tiếp gần nhau trên cùng video.  
   Báo cáo ghi rõ cách lọc, mẫu số, ví dụ và giới hạn: nhật ký không có nội dung hỏi/đáp nên chưa chứng minh được nguyên nhân học viên hỏi tiếp.

2. **AI hỗ trợ mình thế nào**

   Em dùng Codex để hỗ trợ chuyển script sang thư viện chuẩn Python, bổ sung kiểm thử, đối chiếu số liệu và soạn tài liệu evidence.  
   Một điểm phải chỉnh trong bản trước là cách mô tả toàn bộ 1.091 câu hỏi như câu hỏi dưới video; dữ liệu thực tế có 1.090 câu kênh video và 1 câu kênh phiên học.  
   Bản cuối phân biệt 438/1.091 = 40,1% trên tập chính với 438/1.090 = 40,2% khi chỉ xét kênh video; các bảng ví dụ được kiểm lại bằng công cụ độc lập.  
   Qua việc rà và yêu cầu sửa đầu ra AI, em rút ra rằng cần kiểm cả phạm vi và cách diễn giải, không chỉ nhìn xem con số có khớp; kiểm bằng công cụ cũng không được ghi thành đã có người kiểm tay.

3. **Một ca kiểm thử trượt và điều mình học được**

   Trong phần đào nhật ký, có ca thử gồm một dòng hợp lệ và một dòng câu hỏi thiếu `agent_id`; kết quả mong đợi là báo lỗi vì không xác định được dòng thiếu thông tin có thuộc tập cần đếm hay không.  
   Script trước đó vẫn nhận file, ghi tổng 2 dòng nhưng chỉ tính 1 câu hỏi, tức là âm thầm bỏ qua dòng thiếu trường lọc.  
   Sau đó, bước kiểm dữ liệu được đưa lên trước khi lọc và bổ sung ca kiểm thử hồi quy trong [test_mine_chat.py](../scripts/test_mine_chat.py); bộ kiểm thử kỹ thuật có 12 bài đã qua.  
   Bài học của em là phải thử cả dữ liệu thiếu và sai cấu trúc, vì một script chạy không lỗi vẫn có thể tạo ra mẫu số sai.  
   Đây là ca kiểm thử kỹ thuật của phần đào dữ liệu, không phải câu benchmark đánh giá trợ giảng; tại thời điểm viết, repo chưa có kết quả eval để ghi một câu benchmark trượt thực tế.
