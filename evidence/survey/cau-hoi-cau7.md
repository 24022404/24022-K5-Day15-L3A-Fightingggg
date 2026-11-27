# Câu hỏi thật của học viên (câu 7 khảo sát) để làm câu thử `nguoi_dung`

> Nguồn: `evidence/survey/results.csv`, câu 7 "Lần gần nhất, bạn đã gõ gì cho trợ giảng?". Học viên tự nhớ và chép lại "gần đúng nguyên câu", không phải log hệ thống.
> Chép **nguyên văn** từ form (giữ lỗi chính tả, viết hoa, dấu câu). Không sửa câu cho đẹp.
> Cột "Gợi ý loại" do Phương đề xuất theo bài mẫu p01–p21 (chủ đề nền tảng LLM). Long quyết định `type`, `expected`, `pass_criterion`. Cột `source` ghi `nguoi_dung: khảo sát R__`.

## Dùng được (17 câu)

| Mã | Câu nguyên văn | Gợi ý loại | Vì sao |
|---|---|---|---|
| R23 | LLM là gì | thuong | Bài có p01 "LLM là gì" |
| R01 | Container và Image khác nhau như nào | kho | Ngoài bài (Docker) → nói không có trong bài |
| R09 | Gap giữa DEV và production là gì, như thế nào? | kho | Ngoài bài |
| R13 | Dạ cho em hỏi, trợ lý lấy con số ba mươi ngày từ tài liệu đổi hàng, vậy sao nó không lấy đúng mười bốn ngày ở chính sách hoàn tiền ạ? | kho | Ngoài bài (bài lab khác) |
| R15 | Guardrails là gì? | kho | Bài không có guardrails |
| R18 | Double diamond là gì? | kho | Ngoài bài |
| R19 | PRD là gì? | kho | Ngoài bài |
| R20 | SLO là gì? | kho | Ngoài bài |
| R21 | GenAI là gì? MCP là gì? | kho | Hai ý, bài không có định nghĩa MCP |
| R22 | Khoan thầy ơi, dashboard vẫn xanh mà tỉ lệ gọi issue_refund lại tăng từ mười lên mười ba phần trăm, vậy HTTP 200 nó khác gì "đúng" ạ? | kho | Ngoài bài |
| R10 | phần guard rail này còn thêm tài liệu hay hướng dẫn nào cụ thể hơn không | kho | Ngoài bài, xin thêm tài liệu |
| R05 | Đoạn phút thứ 5 giảng viên nhắc đến khái niệm này nghĩa là gì vậy ạ? Mình chưa rõ cách áp dụng vào bài tập. | kho | Mơ hồ ("khái niệm này") → hỏi lại |
| R06 | Em thấy đoạn này trên slide khá khó hiểu, anh có ví dụ nào mô tả ko | kho | Mơ hồ ("đoạn này") → hỏi lại |
| R16 | nhiệm vụ chính của bài hôm nay là gì | kho | Mơ hồ / ngoài phạm vi bài mẫu |
| R24 | tóm tắt cực ngắn video này | kho | Không có video, chỉ có bài mẫu → nhóm tự quyết hành vi mong muốn |
| R03 | Em làm theo hướng dẫn nhưng bị báo lỗi và ra kết quả khác với ví dụ, có thể xem giúp em chỗ này em đang hiểu sai ở đâu không ạ | kho | Thiếu thông tin (lỗi gì, ví dụ nào) → hỏi lại |
| R12 | hỏi nội dung bài học lec14 | kho | ⚠️ Có thể là mô tả chứ không phải nguyên câu; dùng thì ghi rõ trong `source` |

## Không dùng (7 phiếu)

R02 (chưa từng hỏi), R04 (để trống), R07 ("Không nhớ"), R08 (nói không hỏi gì), R11 ("."), R14 ("Mad Don"), R17 ("18 lần"): không phải câu hỏi.

## Lưu ý cho bộ câu thử

- Bộ hiện có 30 câu `tu_viet`. Muốn đạt **≥1/3 từ người dùng**: thêm 15 câu trên thì 15/45; hoặc thêm 10 câu thì cần thay bớt câu `tu_viet` (không xoá câu đã chạy trượt).
- Phần lớn câu thật là câu **ngoài bài**: học viên hỏi về nhiều ngày học khác (Docker, guardrails, PRD, SLO…), trong khi bài mẫu chỉ có nền tảng LLM. Đây là thông tin thật về cách học viên dùng trợ giảng, nên giữ.
