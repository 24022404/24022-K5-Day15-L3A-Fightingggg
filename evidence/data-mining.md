# Đào số liệu pain từ nhật ký pre-class

Phụ trách: Nguyễn Ngọc Sang — đào số liệu từ nhật ký và tổng hợp evidence theo `TEAMS.md`. Cập nhật: 27/11/2026 17:17:25 (UTC+7).

## 1. Nguồn, phạm vi và cách lọc

- File BTC do người dùng cung cấp: `data/preclass/chat.csv`, 260.259 byte; SHA-256 `3331daa0356c1c1863e8b0dd8e74581071d425d9d956e24a98b6f0f2166d304c`. File gốc giữ nguyên và được `.gitignore` bỏ qua; chỉ nộp số tổng hợp và mã ví dụ.
- 1.260 bản ghi không tính tiêu đề: 1.091 `question`, 151 `reply`, 18 `mention`.
- Tập phân tích chính: `kind=question` và `agent_id=teaching_assistant`, gồm **1.091 câu hỏi từ 143 mã học viên**, khoảng ngày hỏi 05/11–25/11/2026.
- Trong tập chính có **1.090 `video_question` và 1 `session_question`**. Không gọi toàn bộ 1.091 câu là hỏi dưới video.
- `C00189` thuộc `session_question`, không có `transcript`; giữ trong tập chính và A/B, không đưa vào phép nhóm cùng video. Cả 1.090 dòng kênh video đều có `transcript`. Không coi mã video trống ở kênh phiên học là lỗi mất dữ liệu nếu chưa có quy định schema như vậy.
- Nguồn có metadata, độ dài và thời gian; không có nội dung hỏi/đáp. Độ dài dùng đúng cột nguồn, không suy ra nội dung hay tính đúng của câu trả lời.

## 2. Cách chạy lại và kiểm dữ liệu

```text
python scripts/mine_chat.py data/preclass/chat.csv
python scripts/mine_chat.py data/preclass/chat.csv --json
python -B -m unittest discover -s scripts -p test_mine_chat.py -v
powershell -NoProfile -File scripts/verify_chat.ps1
```

Các script chỉ đọc nguồn và in kết quả, không gọi model hay gửi tin. Python chỉ dùng thư viện chuẩn. Bộ kiểm độc lập PowerShell/.NET đối chiếu số tổng hợp và chính các bảng ví dụ bên dưới; kết quả lưu ở `evidence/chat-verification.json`, còn bản tổng hợp Python ở `evidence/chat-summary.json`.

Trước khi lọc, kiểm số ô, cột trùng, `kind` trống; với dòng câu hỏi kiểm `agent_id` trống để không âm thầm làm mất câu. Trong tập phân tích kiểm `id` duy nhất, mã học viên/kênh/thời điểm không trống, thời gian ISO 8601 nhất quán múi giờ, độ dài nguyên không âm, phản hồi không âm. Dòng không hợp lệ sẽ báo lỗi; không sửa file gốc hoặc tự bỏ dòng lỗi để thay mẫu số. Nguồn hiện tại qua các kiểm tra này.

## 3. Kết quả và định nghĩa phép đo

| # | Hành vi đo được | Tử số / mẫu số | Cách đếm |
|---|---|---|---|
| A | Câu hỏi dài tối đa 10 ký tự | **70/1.091 = 6,4%** | `do_dai_cau_hoi <= 10` trên tập chính |
| B | Thời gian từ hỏi đến tạo phản hồi dưới 0,5 giây | **26/1.091 = 2,4%** | `0 <= created_at - asked_at < 0.5 giây`; đúng 0,5 giây không tính |
| C | Hỏi tiếp gần nhau trên cùng video | **438/1.091 = 40,1%** | Chỉ nhóm `video_question` có `transcript`, theo học viên/video, sắp `asked_at`, so với câu ngay trước; khoảng cách `<=120 giây` |

C xuất hiện ở **91/143 học viên**. Câu đầu mỗi nhóm không tính vào C; khoảng cách bằng 0 có tính. Đây là khoảng cách giữa hai lần hỏi, không yêu cầu câu trước đã được trả lời, không kiểm hai câu có cùng ý.

Bảng chính giữ bộ lọc và mẫu số 1.091 của bản đầu; các số 70, 26, 438, 143, 91 đều khớp. **Riêng kênh video**, A = 70/1.090 (6,4%), B = 26/1.090 (2,4%), C = **438/1.090 (40,2%)**. Hai tỷ lệ 40,1% và 40,2% có mẫu số khác nhau, không dùng thay thế nhau mà bỏ nhãn.

Chi tiết B đã kiểm: 26/26 câu hỏi dài tối đa 15 ký tự; độ dài phản hồi 171 ký tự xuất hiện 11 lần (138 ký tự: 6 lần; 40 ký tự: 3 lần). Không suy từ thời gian/độ dài ra câu mẫu, cache hay độ đúng.

## 4. Ví dụ có nguồn để đối chiếu

Tám mã sau giữ từ báo cáo ban đầu. Số bản ghi bắt đầu từ 1, không tính tiêu đề; độ dài lấy từ cột nguồn, thời gian tính từ hai timestamp. Không trích lời người dùng vì không có nội dung.

| Mã dòng | Bản ghi nguồn | Độ dài câu hỏi | Độ dài trả lời | Phản hồi (giây) |
|---|---|---|---|---|
| C01056 | 8 | 2 | 171 | 0,018206 |
| C00321 | 34 | 2 | 134 | 0,046064 |
| C00962 | 98 | 2 | 171 | 0,114540 |
| C00910 | 571 | 2 | 171 | 0,035098 |
| C01182 | 306 | 2 | 67 | 0,019552 |
| C00920 | 298 | 2 | 171 | 0,028518 |
| C00344 | 126 | 2 | 40 | 0,021807 |
| C01149 | 109 | 2 | 171 | 0,018925 |

Năm cặp sau là hai câu liên tiếp sau khi sắp thời điểm hỏi trong cùng nhóm học viên/video:

| Mã câu trước | Mã câu sau | Khoảng cách hỏi (giây) | Cùng học viên/video |
|---|---|---|---|
| C00581 | C00499 | 69,076788 | Có |
| C00499 | C01138 | 64,658684 | Có |
| C01138 | C01085 | 43,429216 | Có |
| C01122 | C00937 | 55,859240 | Có |
| C00216 | C00775 | 29,727245 | Có |

## 5. Kết luận từ nhật ký và giới hạn

**Đã xác nhận:** trong tập quan sát có câu hỏi ngắn, phản hồi nhanh và 438 lượt hỏi tiếp gần nhau trên cùng video. Đây là tín hiệu để nhóm tìm hiểu trải nghiệm hỏi bài và thiết kế tình huống thử.

**Chưa xác nhận:** học viên không hài lòng, hỏi lại cùng một ý, câu trả lời sai/thiếu trích dẫn, hay thiếu trích dẫn gây mất thời gian. Câu ngắn có thể là lời xác nhận; hỏi gần nhau có thể là đào sâu hoặc gửi nhiều câu trước khi đọc phản hồi. Các nhóm A/B/C có thể chồng nhau, không cộng phần trăm. Tập có hỏi không đại diện toàn khoá; 143 không phải quy mô người dùng toàn sản phẩm.

Nhật ký này chưa đo được số phút tiết kiệm, tần suất gặp pain mỗi tháng hoặc hiệu quả của prototype. Nhóm có thể dùng nghiên cứu người dùng do Phương phụ trách để kiểm nguyên nhân; kết quả đó là nguồn bổ sung, không phải điều kiện để hoàn tất phép đào và báo cáo nhật ký của Sang.

## 6. Trạng thái bàn giao

Phần của Sang đã có nguồn, bộ lọc, x/N, %, phương pháp chạy lại, kiểm lỗi và hơn 5 ví dụ. Kết quả được đối chiếu bằng hai cách độc lập; xem `evidence/verification.md`. Kết luận trung thực là **số liệu hành vi đã xác minh, giả thuyết nguyên nhân chưa được dữ liệu này chứng minh**. Không tự tạo phỏng vấn hoặc ghi nhận người duyệt khi chưa có xác nhận.
