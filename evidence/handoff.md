# Bàn giao phần của Nguyễn Ngọc Sang

Phạm vi theo `TEAMS.md`: **Đào số liệu pain từ nhật ký, evidence**. Cập nhật 27/11/2026. Đây là tài liệu trong repo; không ghi nhận đã gửi tin hoặc có thành viên duyệt nếu chưa có xác nhận.

## 1. Sản phẩm bàn giao

| Sản phẩm | Nội dung | Trạng thái |
|---|---|---|
| `scripts/mine_chat.py` | Đọc nguồn, kiểm dữ liệu, đếm và xuất số tổng hợp; chỉ dùng thư viện chuẩn | Hoàn thành |
| `scripts/test_mine_chat.py` | 12 bài kiểm thử, gồm lỗi bộ lọc và phân biệt kênh video/phiên học | Đã qua |
| `scripts/verify_chat.ps1` | Đếm độc lập PowerShell/.NET và kiểm trực tiếp bảng ví dụ của báo cáo | Đã chạy; kết quả tại `evidence/chat-verification.json` |
| `evidence/data-mining.md` | Nguồn, mẫu số, phương pháp, số chính, 8 dòng và 5 cặp minh hoạ, giới hạn | Hoàn thành |
| `evidence/summary.md` | Kết luận đúng mức chứng cứ từ nhật ký | Hoàn thành |
| `evidence/hypothesis.md` | Phân biệt giả thuyết với điều có thể kiểm; khai báo thời điểm bổ sung trung thực | Hoàn thành hồ sơ |
| `evidence/verification.md`, hai file JSON tổng hợp | Dấu vân tay nguồn, kết quả và hướng dẫn kiểm lại | Hoàn thành |

Hoàn thành trên là phần đào nhật ký/evidence; không có tuyên bố nhóm đã chứng minh nguyên nhân pain hoặc đã thực hiện phỏng vấn.

## 2. Số liệu thống nhất để nhóm sử dụng

> Nhật ký có 1.260 bản ghi; lọc được 1.091 câu hỏi gửi trợ giảng từ 143 học viên trong 05/11–25/11/2026, gồm 1.090 câu kênh video và 1 câu kênh phiên học. Có 70 câu dài tối đa 10 ký tự (6,4%), 26 phản hồi dưới 0,5 giây (2,4%), và 438 lượt hỏi tiếp trong tối đa 120 giây trên cùng video (40,1% của tập 1.091; xuất hiện ở 91/143 học viên). Riêng kênh video, tỷ lệ hỏi tiếp là 438/1.090 = 40,2%. Nhật ký chưa xác định được nguyên nhân hỏi tiếp hoặc chất lượng câu trả lời.

## 3. Liên quan các thành viên khác

- **Minh — spec:** mô tả pain là giả thuyết. `spec.md` §0–§1 đã đồng bộ phạm vi và cách diễn giải; không đổi chuẩn đánh giá prototype. Chưa có số phút hay số người thực sự gặp pain để tính impact như kết quả đo thật.
- **Phương — khảo sát/canvas/slide:** dùng số liệu và giới hạn trên; canvas đã đồng bộ phần bằng chứng và kế hoạch khảo sát mới. Hồ sơ form tại `evidence/survey/questions.md`, tiêu chí tại `evidence/hypothesis.md`; `evidence/interviews/guide.md` là kịch bản phỏng vấn dự phòng nếu khảo sát không đủ mẫu. Không ghi kết quả nghiên cứu người dùng khi chưa có dữ liệu thật.
- **Long — data card/benchmark:** Dataset 1 đã đồng bộ nguồn và phân biệt kênh. Không biết nội dung câu hỏi 2 ký tự nên câu tự viết theo cảm hứng từ độ dài vẫn là `tu_viet`, không tự đổi thành `data_that`.

## 4. Kiểm lại hoặc cập nhật sau này

Chạy các lệnh trong `evidence/verification.md`. Nếu nguồn thay đổi, ghi dấu vân tay và kết quả lượt mới; không sửa dữ liệu để khớp số cũ. Các số trong kiểm thử là dữ liệu giả tạm thời, không phải bằng chứng nghiên cứu. Người trong nhóm tự ghi xác nhận rà khi thực sự thực hiện; báo cáo không giả lập việc đó.
