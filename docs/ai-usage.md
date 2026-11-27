# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | Codex | Ngày 27/11/2026: chuẩn hoá script thư viện chuẩn, chặn dữ liệu lỗi trước bộ lọc; tách kênh video/phiên học và mẫu số, đối chiếu Python/PowerShell; lưu số tổng hợp và dấu vân tay | 12 bài kiểm thử đã qua; bộ kiểm độc lập xác nhận số tổng, 8 dòng và 5 cặp trong bảng báo cáo. Không ghi nhận kiểm tay của người khi chưa có xác nhận; xem `evidence/verification.md` | Sang — phần đào nhật ký/evidence đã hoàn thành bằng công cụ |
| Rà câu hỏi phỏng vấn / khảo sát | Codex | Soạn kịch bản phỏng vấn dự phòng, rà tránh dẫn dắt; khi cập nhật main giữ nguyên câu hỏi và tiêu chí khảo sát Phương đã ghi | Chưa tạo dữ liệu trả lời; kịch bản không phải ghi chép phỏng vấn. Khảo sát chính theo `evidence/survey/questions.md` | Phương phụ trách khảo sát; Sang phụ trách nhật ký/evidence |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |
| Tài liệu bằng chứng của Sang | Codex | Hoàn thiện báo cáo nhật ký, đồng bộ spec/canvas/data card; hòa giải thay đổi khảo sát từ main với phần số liệu đã xác minh | Số liệu, phạm vi và ví dụ đã đối chiếu; chưa có xác nhận duyệt của người. Giữ tiêu chí khảo sát của Phương, không tạo câu trả lời, trích dẫn hay số impact | Sang — hồ sơ evidence từ nhật ký đã hoàn thành |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
