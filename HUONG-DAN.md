# Bản cuối: web học tập AI20K (21 trang, 3 module, 3 quiz, đăng nhập)

Áp dụng SAU KHI nộp CP2 (19:30 Thứ Sáu). Trong thư mục repo:

```bash
unzip -o cp2-final.zip
pip install -r requirements-web.txt
uvicorn server:app --port 8000       # mở http://localhost:8000
python run.py check
python run.py eval                   # 30 câu, chấm tay như cũ
```

Đăng nhập demo: tên `hocvien`, mật khẩu `ai20k2026` (hoặc "Vào với tư cách khách").
Đổi tài khoản: biến môi trường `DEMO_USERS="ten:matkhau,ten2:matkhau2"`.

Deploy Render (miễn phí, không Docker): New > Blueprint, chọn repo (đã có render.yaml). Điền MODEL_PROVIDER, MODEL_NAME, API_KEY (và DEMO_USERS nếu muốn). Mở link trước giờ demo 1 phút vì máy chủ miễn phí ngủ khi không có người dùng.

Lưu ý:
- Bài trắc nghiệm chấm ở máy chủ (data/quiz.json), đáp án chỉ trả về sau khi nộp. Trợ giảng AI ở bên phải bài quiz không đưa đáp án (đúng quy tắc từ chối trong bộ câu thử B11, B25).
- Tài khoản demo là mật khẩu dùng chung, không phải xác thực thật; trong DATA_CARD/README nên ghi rõ như vậy.
- eval/metric_spec.yaml và spec §7 không đổi. Bài p09 đến p21 cần 1 người đọc đối chiếu với sách nguồn trước CP3.
