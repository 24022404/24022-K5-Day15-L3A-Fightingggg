# Khảo sát: tự học bài pre-class và hỏi trợ giảng dưới video

> Nhóm Fightingggg · guide bước 1.2 · người phụ trách: Phương.
> Ngưỡng: ≥20 người ngoài nhóm, đúng người dùng (học viên AI20K khoá 5). Câu trả lời của thành viên nhóm không tính.

## Thông tin form

| | |
|---|---|
| Công cụ | Google Form, tạo bằng Apps Script ngày 27/11/2026 lúc 16:26 |
| Link trả lời | https://docs.google.com/forms/d/e/1FAIpQLSfDud2JbmXbzMcxVSQbJrLZKFRBwu74Pf3m5Uo4dDBotesGAQ/viewform |
| Kênh đã gửi | nhóm Zalo PreClass Online - AI20K Cohort 5 |
| Giờ mở | 16:47 Thứ Sáu 27/11/2026 |
| Giờ chốt | 9:00 Thứ Bảy 28/11/2026 |
| Số người trả lời khi chốt | __ (ngoài nhóm: __) |
| Thu thông tin cá nhân | Không: không thu tên, email, mã học viên |

## Bộ câu hỏi (nguyên văn trên form)

| # | Câu hỏi | Kiểu | Lựa chọn | Bắt buộc | Dùng cho |
|---|---|---|---|---|---|
| 1 | Bạn là: | Trắc nghiệm | Học viên L3A · Học viên L3B · Học viên lớp khác của khoá 5 · Lab coach / TA / giảng viên · Khác | Có | Lọc đúng người dùng |
| 2 | Lần gần nhất bạn hỏi trợ giảng dưới video pre-class là khi nào? | Trắc nghiệm | Hôm nay · Trong tuần này · Tuần trước · Lâu hơn nữa · Chưa bao giờ hỏi | Có | Tần suất, persona |
| 3 | Lần gần nhất đó, sau khi nhận câu trả lời, bạn có kiểm lại trong bài không? | Trắc nghiệm | Có, và tìm được đúng đoạn trong bài · Có tìm, nhưng không biết đoạn nào nói ý đó · Không kiểm, tin luôn câu trả lời · Không kiểm, bỏ qua câu trả lời · Khác | Có | Pain chính: tự kiểm câu trả lời |
| 4 | Ngay sau câu trả lời đó, bạn có hỏi tiếp trợ giảng không? | Trắc nghiệm | Không hỏi tiếp · Có, vì câu trả lời chưa đủ ý · Có, vì không chắc câu trả lời đúng · Có, hỏi sang ý khác · Khác | Có | Kiểm tín hiệu C (40,1% hỏi tiếp trong 120 giây, `evidence/data-mining.md`) |
| 5 | Lần đó bạn mất khoảng bao lâu để hiểu được ý mình hỏi (kể cả hỏi lại, tìm lại trong bài)? | Trắc nghiệm | Dưới 5 phút · 5–15 phút · 15–30 phút · Trên 30 phút · Cuối cùng vẫn chưa hiểu | Có | Số phút mỗi lần, impact `spec.md` §2 |
| 6 | Trong 1 tuần qua, bạn hỏi trợ giảng dưới video khoảng mấy lần? (ghi một con số) | Trả lời ngắn (số ≥0) | — | Có | Số lần / tháng, `cost/personas.yaml` |
| 7 | Lần gần nhất, bạn đã gõ gì cho trợ giảng? (chép lại gần đúng nguyên câu, nếu nhớ) | Đoạn văn | — | Không | Câu thử `nguoi_dung` cho `eval/benchmark.csv` |
| 8 | Điều gì khó chịu nhất ở lần đó? | Đoạn văn | — | Không | Trích dẫn, `evidence/summary.md` |
| 9 | Khi chưa hiểu bài, ngoài trợ giảng bạn còn làm cách nào khác? (tua video, hỏi bạn, ChatGPT riêng, hỏi TA…) | Đoạn văn | — | Không | Cách đang xoay xở |

Mô tả đầu form: *"Nhóm Fightingggg (L3A) đang tìm hiểu cách học viên tự học bài pre-class. Khoảng 3 phút, hỏi về lần gần nhất bạn hỏi trợ giảng dưới video. Không thu tên, email hay mã học viên."*

## Lời mời đã gửi

> Chào cả lớp 👋
>
> Nhóm **Fightingggg (L3A)** đang tìm hiểu cách mọi người tự học bài pre-class trước giờ lên lớp, nhất là lúc **hỏi trợ giảng dưới video**. Các bạn giúp nhóm mình điền khảo sát ngắn này nhé:
>
> 👉 [link]
>
> - ⏱ Khoảng **3 phút**, 9 câu, phần lớn là chọn đáp án
> - 🔒 **Ẩn danh**: không hỏi tên, email hay mã học viên
> - Chỉ hỏi về **lần gần nhất** bạn hỏi trợ giảng. Bạn chưa từng hỏi lần nào thì vẫn điền giúp được, câu trả lời đó cũng có ích cho nhóm.
>
> Nhóm mong nhận được câu trả lời **trước 9:00 sáng mai (28/11)**. Cảm ơn mọi người nhiều! 🙏

## Sau khi chốt

- Xuất câu trả lời ra `evidence/survey/results.csv`. Bỏ cột dấu thời gian nếu cột đó có thể nhận ra người trả lời. Bỏ các dòng do thành viên nhóm điền thử.
- Câu 7: chép các câu hỏi nguyên văn vào `eval/benchmark.csv` với `source` = `nguoi_dung: khảo sát #<số dòng>`.
- Số chính và ≥3 câu trả lời nguyên văn: chép vào `evidence/summary.md`. Nếu dưới khoảng 10 người trả lời thì chỉ ghi x/n, không ghi %.
