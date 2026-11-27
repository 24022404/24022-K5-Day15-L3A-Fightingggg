# Đào số liệu pain từ nhật ký pre-class (bản đầu, CP2)

**Nguồn:** `data/preclass/chat.csv` (1.260 dòng; lọc `kind=question` và `agent_id=teaching_assistant`).
**Cách chạy lại:** `python scripts/mine_chat.py data/preclass/chat.csv`
**Giới hạn:** data chỉ có độ dài, không có nội dung câu hỏi/trả lời. Các con số dưới đây là tín hiệu gián tiếp, chưa chứng minh học viên không hài lòng. Cần phỏng vấn để xác nhận.

N = 1.091 câu hỏi gửi trợ giảng, từ 143 học viên.

| # | Tín hiệu | Kết quả | Cách đếm |
|---|---|---|---|
| A | Câu hỏi rất ngắn (<=10 ký tự), khó trả lời có căn cứ | 70/1091 = 6,4% | `do_dai_cau_hoi <= 10` |
| B | Trả lời tức thì (<0,5 giây), cả 26 câu đều có câu hỏi <=15 ký tự, độ dài trả lời lặp lại (171 ký tự xuất hiện 11 lần) nghi là câu mẫu chung | 26/1091 = 2,4% | `created_at - asked_at < 0.5s` |
| C | Học viên hỏi tiếp trong <=120 giây, cùng video | 438/1091 = 40,1% (91/143 học viên) | cùng `hv` và `transcript`, khoảng cách giữa 2 câu <=120s |

## Ví dụ (id dòng trong chat.csv)
C01056, C00321, C00962, C00910, C01182, C00920, C00344, C01149: đều là câu hỏi 2 ký tự, trả lời trong dưới 0,15 giây.

## Điều chưa biết (cần kiểm)
- C có thể là hỏi dồn tự nhiên chứ chưa chắc là không hài lòng: phỏng vấn 2-3 bạn trong lớp để hỏi vì sao hỏi liền nhau.
- Chưa biết câu trả lời có đúng căn cứ không, vì data không có nội dung. Đây là lý do nhóm tự đo bằng benchmark.
