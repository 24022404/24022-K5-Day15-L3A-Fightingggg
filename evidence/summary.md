# Tổng hợp bằng chứng từ nhật ký

Phụ trách: Nguyễn Ngọc Sang — đào số liệu pain từ nhật ký, evidence. Ngày cập nhật: 27/11/2026.

## 1. Nguồn đã dùng

| Nguồn | Đã làm gì | Trạng thái |
|---|---|---|
| `data/preclass/chat.csv` do người dùng cung cấp | Lọc, kiểm dữ liệu, đếm bằng Python, đối chiếu độc lập PowerShell/.NET và các bảng ví dụ | Hoàn thành phần đào nhật ký: có x/N, %, cách chạy lại, 8 dòng và 5 cặp ví dụ |
| Khảo sát của Phương | Nhóm đã có form và bộ câu hỏi tại `evidence/survey/questions.md`; chưa dùng làm kết quả trong báo cáo vì chưa có dữ liệu trả lời trong repo | Đang thu theo hồ sơ của nhóm: mở 16:47 ngày 27/11, chốt 9:00 ngày 28/11; phỏng vấn là nguồn dự phòng |

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
