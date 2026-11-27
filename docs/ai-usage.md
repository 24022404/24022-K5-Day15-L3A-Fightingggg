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
| Khảo sát Google Form | Claude Code | Ngày 27/11/2026: soạn 9 câu hỏi khảo sát (5 trắc nghiệm, 4 trả lời ngắn) hỏi về hành vi đã xảy ra; viết Apps Script tạo form; soạn lời mời gửi lớp; tạo `evidence/survey/questions.md` | Phương chạy script trên tài khoản của mình, kiểm form bằng cửa sổ ẩn danh, tự gửi vào nhóm Zalo lớp lúc 16:47, thu được 24 câu trả lời. AI không tạo, không sửa câu trả lời khảo sát | Phương |
| Giả thuyết và đồng bộ tài liệu khi đổi sang khảo sát | Claude Code | Soạn nháp `evidence/hypothesis.md`, đề xuất hai ngưỡng (≥50% câu 3, ≥30% câu 4); sửa TEAMS.md, canvas dòng 4 và 7, spec §1, thêm dòng changelog spec §10 | Phương đọc lại và commit (`f564505`). Hai ngưỡng do AI đề xuất, nhóm cần chốt trước khi mở kết quả khảo sát | Phương |
| Slide, văn bản | Claude Code | Tạo `slides/demo-slides.pptx` (10 trang) bằng script python-pptx theo `slides/outline.md`; lấy số từ file trong repo, ghi nguồn ở chân mỗi trang; chỗ chưa có số để ô "CHỜ SỐ"; output trên slide demo là output thật chạy `python run.py` với Gemini ngày 27/11/2026 | Phương xem từng bản, yêu cầu đổi font (Times New Roman), màu (navy, xanh dương, trắng), cỡ chữ. Cần tự đối chiếu lại các số trên slide với file nguồn trước khi trình bày | Phương |
| Tài liệu bằng chứng của Sang | Codex | Hoàn thiện báo cáo nhật ký, đồng bộ spec/canvas/data card; hòa giải thay đổi khảo sát từ main với phần số liệu đã xác minh | Số liệu, phạm vi và ví dụ đã đối chiếu; chưa có xác nhận duyệt của người. Giữ tiêu chí khảo sát của Phương, không tạo câu trả lời, trích dẫn hay số impact | Sang — hồ sơ evidence từ nhật ký đã hoàn thành |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
