# Tổng hợp bằng chứng từ nhật ký

Phụ trách: Nguyễn Ngọc Sang — đào số liệu pain từ nhật ký, evidence. Ngày cập nhật: 27/11/2026.

## 1. Nguồn đã dùng

| Nguồn | Đã làm gì | Trạng thái |
|---|---|---|
| `data/preclass/chat.csv` do người dùng cung cấp | Lọc, kiểm dữ liệu, đếm bằng Python, đối chiếu độc lập PowerShell/.NET và các bảng ví dụ | Hoàn thành phần đào nhật ký: có x/N, %, cách chạy lại, 8 dòng và 5 cặp ví dụ |
| Khảo sát của Phương (Google Form) | 24 câu trả lời từ học viên khoá 5 (L3A 12 · L3B 10 · lớp khác 2), form mở 16:47, tải kết quả 19:12 ngày 27/11. Bản ẩn danh: `evidence/survey/results.csv`; bộ câu hỏi: `evidence/survey/questions.md` | **Đạt ngưỡng ≥20 người**; kết quả ở mục 6 bên dưới |

Theo yêu cầu khung, nguồn đào data đã có các thành phần định lượng và ví dụ. Việc xác minh số liệu không đồng nghĩa xác nhận nguyên nhân pain. Không ghi đã có người kiểm tay/duyệt khi mới có kiểm bằng công cụ.

## 2. Kết quả chính

Từ 1.260 bản ghi, lọc `kind=question` và `agent_id=teaching_assistant` được **1.091 câu hỏi từ 143 học viên**, trong khoảng 05/11–25/11/2026. Tập này gồm **1.090 câu hỏi kênh video và 1 câu hỏi kênh phiên học**.

| Chỉ số | Kết quả trên tập chính |
|---|---|
| Câu hỏi dài tối đa 10 ký tự | 70/1.091 — 6,4% |
| Phản hồi từ 0 đến dưới 0,5 giây | 26/1.091 — 2,4% |
| Hỏi tiếp trong tối đa 120 giây trên cùng video | 438/1.091 — 40,1%; xuất hiện ở 91/143 học viên |

Riêng kênh video có 438/1.090 lượt hỏi tiếp — **40,2%**. `C00189` thuộc kênh phiên học và không có mã video, không đưa vào nhóm C; mẫu số chính vẫn là 1.091 như định nghĩa đã công bố. Không cộng các tỷ lệ A/B/C.

## 3. Ví dụ và khả năng kiểm lại

Tám dòng `C01056`, `C00321`, `C00962`, `C00910`, `C01182`, `C00920`, `C00344`, `C01149`: đều có độ dài câu hỏi 2 ký tự và phản hồi dưới 0,15 giây. Bảng đầy đủ số bản ghi, độ dài trả lời và thời gian chính xác ở `evidence/data-mining.md` §4.

Cũng tại đó có 5 cặp câu liên tiếp cùng học viên/video minh hoạ C, kèm mã trước/sau và khoảng cách. Đây là ví dụ metadata có nguồn, không phải lời trích nguyên văn. Nguồn không có nội dung hỏi/đáp để tạo trích dẫn.

Lệnh chính: `python scripts/mine_chat.py data/preclass/chat.csv`. Kết quả Python lưu ở `evidence/chat-summary.json`; phương pháp và lệnh đối chiếu độc lập ở `evidence/verification.md`, kết quả đối chiếu ở `evidence/chat-verification.json`.

## 4. Kết luận và mức bằng chứng

- **Được dữ liệu ủng hộ:** có các hành vi hỏi ngắn và hỏi tiếp gần nhau đáng để tìm hiểu thêm trong luồng tự học.
- **Chưa được chứng minh:** học viên thiếu cách kiểm căn cứ, hỏi lại cùng một ý do thiếu trích dẫn, không hài lòng, hoặc mất bao nhiêu phút. Số 40,1% là tỷ lệ hành vi theo định nghĩa C, không phải tỷ lệ câu trả lời sai hay tỷ lệ người gặp pain.
- **Giả thuyết giải pháp:** trả lời kèm mã đoạn có thể giúp học viên kiểm câu trả lời; cần bằng chứng khác để kiểm giả thuyết. Nhật ký không đủ để xác nhận hoặc bác bỏ nguyên nhân này.
- **Giới hạn phạm vi:** không suy rộng 143 học viên thành toàn khoá, không quy đổi khoảng quan sát thành tần suất tháng và không tính impact/chi phí từ số ví dụ chưa có nguồn.

## 5. Trạng thái công việc của Sang

**Hoàn thành phần đào nhật ký và hồ sơ evidence trong phạm vi phân công:** báo cáo có nguồn, cách đếm, số liệu, ví dụ, kiểm chứng và kết luận đúng mức bằng chứng. Các mô tả số liệu liên quan trong spec/canvas/data card đã được đồng bộ.

Khảo sát do Phương phụ trách sẽ bổ sung khi có dữ liệu trả lời thật; tiêu chí ở `evidence/hypothesis.md`, bộ câu hỏi ở `evidence/survey/questions.md`. Phỏng vấn là nguồn dự phòng theo kế hoạch nhóm. Khi có nguồn mới, nhóm cập nhật kết luận, giữ cả kết quả trái giả thuyết. Không coi chưa có nguồn bổ sung là lỗi tính số của Sang và không tự tạo người tham gia/câu trả lời.

## 6. Khảo sát học viên khoá 5 (phần của Phương)

Phụ trách: Đào Thị Thu Phương. Nguồn: Google Form, 24 câu trả lời (mở 16:47, câu trả lời cuối 19:06, tải kết quả 19:12 ngày 27/11/2026). Bản ẩn danh `evidence/survey/results.csv` (bỏ cột dấu thời gian, che 1 tên người thật ở R14); bản gốc `raw-*` không commit. Tiêu chí đúng/sai đặt trước khi xem kết quả, ở `evidence/hypothesis.md` (17:16). Mã R01–R24 là số thứ tự câu trả lời.

**Người trả lời (câu 1):** 24/24 là học viên khoá 5: L3A 12, L3B 10, lớp khác 2. *Chưa xác nhận trong 24 người có thành viên nhóm điền thử hay không.* Mẫu số dưới đây là **23 người đã từng hỏi trợ giảng** (bỏ R02 chọn "Chưa bao giờ hỏi"), đúng như tiêu chí đã đặt.

### 6.1 Số chính

| Câu | Kết quả (n = 23) |
|---|---|
| 3. Sau câu trả lời, có kiểm lại trong bài không? | Tìm được đúng đoạn **11** · Có tìm nhưng không biết đoạn nào **7** · Không kiểm, tin luôn **5** |
| 4. Có hỏi tiếp ngay sau đó không? | Vì câu trả lời chưa đủ ý **10** · Vì không chắc đúng **1** · Hỏi sang ý khác **5** · Không hỏi tiếp **7** |
| 5. Mất bao lâu để hiểu được ý mình hỏi? | Dưới 5 phút **10** · 5–15 phút **6** · 15–30 phút **4** · Trên 30 phút **2** · Cuối cùng vẫn chưa hiểu **1** → trung vị nằm ở nhóm **5–15 phút** |
| 6. Số lần hỏi trợ giảng trong 1 tuần qua | Trung vị **3 lần/tuần**, trung bình 4,8; thấp nhất 0, cao nhất 18 |

### 6.2 So với tiêu chí đã đặt trước

| Tiêu chí (`evidence/hypothesis.md`) | Kết quả | Đạt? |
|---|---|---|
| ≥50% chọn "không biết đoạn nào" hoặc "tin luôn" ở câu 3 | **12/23 = 52,2%** | Đạt, sát ngưỡng |
| ≥30% chọn "chưa đủ ý" hoặc "không chắc đúng" ở câu 4 | **11/23 = 47,8%** | Đạt |

**Độ nhạy:** bỏ 3 phiếu có phần trả lời tự do không đọc được (R11, R14, R17) thì câu 3 còn 10/20 = 50,0% (vừa chạm ngưỡng), câu 4 còn 9/20 = 45,0%. Ngưỡng câu 3 phụ thuộc vào 1–2 phiếu, nên không coi đây là kết quả mạnh.

### 6.3 Câu trả lời tự do (câu 8: điều khó chịu nhất)

Nhóm tự đọc và gom theo chủ đề (n = 23): **trả lời chung chung, không đúng trọng tâm, rời rạc hoặc chưa đủ ý: 11** (R01, R03, R05, R06, R10, R12, R13, R16, R22, R23, R24) · không có gì khó chịu: 4 (R15, R19, R20, R21) · khác hoặc không đọc được: 8.

Trích nguyên văn:

1. "Trợ giảng trả lời hơi chung chung nên mình vẫn phải tua lại video để đối chiếu ngữ cảnh." — R05
2. "Câu trả lời nhận được không đúng trọng tâm, tôi cần hỏi thêm nhiều lần để có được câu trả lời." — R22
3. "Agent không biết tóm tắt mà chỉ trả lời linh tinh, thông tin rác không phải của bài" — R24
4. "Trợ giảng trả lời rời rạc, không có ý chính" — R16
5. "Phải chờ phản hồi khá lâu đúng lúc đang kẹt giữa chừng, hoặc nhận được câu trả lời quá chung chung" — R03
6. *(ngược giả thuyết)* "Không có gì, agent trả lời đúng khái niệm" — R19; "Không có gì, agent hiểu rất đúng mấy khái niệm trong bài học" — R21

**Câu 9 (cách khác):** 17/20 câu trả lời có nội dung nhắc tới ChatGPT, Claude hoặc AI khác; 3 người hỏi TA, lab coach hoặc tua video; 4 phiếu để trống hoặc không đọc được.

### 6.4 Data và người dùng có khớp nhau không

- **Khớp:** nhật ký có 40,1% câu hỏi là hỏi tiếp trong 2 phút; khảo sát có 10/23 người hỏi tiếp *vì câu trả lời chưa đủ ý* và R22 nói phải "hỏi thêm nhiều lần". Vậy một phần lượt hỏi tiếp trong nhật ký có thể do câu trả lời chưa thoả mãn, không chỉ do hỏi dồn tự nhiên.
- **Lệch / điều mới:** 11/23 người nói đã tìm được đúng đoạn trong bài, và lời phàn nàn nhiều nhất là câu trả lời **chung chung, không đúng trọng tâm** chứ không phải "không biết câu trả lời lấy từ đâu". Chỉ R05 và R24 nói trực tiếp tới việc đối chiếu với bài hoặc thông tin "không phải của bài".

### 6.5 Kết luận phần khảo sát

Theo tiêu chí đặt trước, giả thuyết **đạt cả hai ngưỡng nhưng sát mức** (52,2% so với 50%). Kết luận đúng mức bằng chứng: học viên có gặp khó với câu trả lời của trợ giảng, nhưng pain rộng hơn giả thuyết, gồm cả **câu trả lời không đúng trọng tâm**. Mã đoạn giúp học viên kiểm câu trả lời (R05, R24) nhưng tự nó không làm câu trả lời đúng trọng tâm hơn; điều này cần đo ở bộ câu thử. Khảo sát là tự khai, 24 người, không đại diện toàn khoá.

**Chuyển cho nhóm:**
- Long: các câu hỏi nguyên văn ở câu 7 dùng làm câu thử `nguoi_dung`, danh sách ở `evidence/survey/cau-hoi-cau7.md`.
- Minh (spec §2 impact): trung vị 3 lần/tuần (câu 6), trung vị 5–15 phút/lần (câu 5), n = 23. Quy đổi sang tháng là ước tính của nhóm, cần ghi rõ.
