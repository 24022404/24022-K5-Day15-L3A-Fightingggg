# Kiểm chứng phần đào nhật ký của Sang

Lượt cập nhật: 27/11/2026 17:17:25 (UTC+7). Codex thực hiện phân tích và đối chiếu bằng công cụ; không thay cho xác nhận kiểm tay/duyệt của một người trong nhóm.

## 1. Nguồn và kết quả đã kiểm

- File: `data/preclass/chat.csv`, 260.259 byte; SHA-256 `3331daa0356c1c1863e8b0dd8e74581071d425d9d956e24a98b6f0f2166d304c`. Giữ nguyên file gốc, Git bỏ qua thư mục nguồn.
- 1.260 bản ghi: 1.091 câu hỏi, 151 reply, 18 mention. Tập lọc trợ giảng gồm 1.091 câu hỏi từ 143 học viên, 05/11–25/11/2026.
- Trong tập lọc: 1.090 câu thuộc `video_question`, 1 câu thuộc `session_question`. `C00189` là câu kênh phiên học, không có `transcript`; không phải câu dưới video bị mất mã theo mặc định. Tất cả dòng kênh video có mã.
- A = 70, B = 26, C = 438, số học viên có C = 91. Mẫu số chính N = 1.091: 6,4%, 2,4%, 40,1%. Riêng kênh video C = 438/1.090 = 40,2%. Số đếm chính khớp bản đầu; việc bổ sung phân loại kênh không thay đổi số cũ.

## 2. Cách kiểm lại

```text
python scripts/mine_chat.py data/preclass/chat.csv --json
python -B -m unittest discover -s scripts -p test_mine_chat.py -v
powershell -NoProfile -File scripts/verify_chat.ps1
```

Python đọc CSV bằng thư viện chuẩn và tính theo định nghĩa trong `evidence/data-mining.md`. Bộ kiểm độc lập PowerShell dùng `Import-Csv`, `.NET DateTimeOffset` và nhóm/sắp thời điểm hỏi; không nhập hoặc gọi script Python. Kết quả lần lượt lưu tại `evidence/chat-summary.json` và `evidence/chat-verification.json`.

PowerShell đọc chính các dòng bảng trong `evidence/data-mining.md`: kiểm 8 mã ví dụ với số bản ghi, độ dài hỏi/trả lời và giây phản hồi; kiểm 5 cặp với học viên/video, vị trí liên tiếp trong nhóm và khoảng cách. Nếu không khớp hoặc thiếu số ví dụ tối thiểu, script báo lỗi. Số học viên/video gốc không được xuất trong hai file tổng hợp.

## 3. Kiểm dữ liệu và kiểm thử

12/12 bài kiểm thử kỹ thuật đã qua trên dữ liệu giả tạm thời: mốc 0,5 giây/120 giây, phân nhóm, thiếu mã video, kênh phiên học xen vào chuỗi video, tách mẫu số chính/video, thiếu trường bộ lọc, lệch số ô, cột trùng, các lỗi thời gian/độ dài, không tự ghi nguồn và không xuất mã người học/video.

Nguồn hiện tại qua kiểm tra: không có câu trong tập lọc thiếu mã học viên/kênh/thời điểm/độ dài, `id` câu hỏi không trùng, không có phản hồi âm. Dòng có bộ lọc trống hay lệch số ô được chặn trước khi lọc, không âm thầm thay mẫu số. Phép nhóm C chỉ nhận kênh video có mã video.

## 4. Ý nghĩa của kiểm chứng

Kiểm chứng xác nhận số liệu và ví dụ, không chứng minh học viên không hài lòng, hỏi lại cùng ý hoặc thiếu trích dẫn gây mất thời gian. Phần đào nhật ký/evidence của Sang đã có nguồn, phương pháp, x/N, %, ví dụ và kết luận có giới hạn. Phỏng vấn/impact là nguồn nghiên cứu tiếp của nhóm, không phải số được tạo thêm để lấp vào báo cáo này.
