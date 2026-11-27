# Bảng đối chiếu nguồn (cho Long)

Mục đích: p09 đến p21 và 15 câu quiz do nhóm viết lại từ hai nguồn mở; data card đang ghi 0/21 đoạn có người kiểm tay. Bảng này để một người trong nhóm đọc nguồn rồi đánh dấu, không sửa ý của nguồn.

- Xiao và Zhu, *Foundations of Large Language Models*, arXiv 2501.09223 (CC BY-NC 4.0).
- Zhao và cộng sự, *A Survey of Large Language Models*, arXiv 2303.18223.

**Cột "Máy đã tìm"** là mình tìm từ khoá trong bản PDF, chỉ cho biết ý có xuất hiện trong nguồn, chưa chứng minh đoạn viết lại đúng nghĩa. Người kiểm đánh dấu ở cột cuối.

## Phần 1. Đoạn p09 đến p21

| Mã | Nguồn ghi trong đoạn | Máy đã tìm | Người kiểm (tên, ✓ hoặc ✗, ghi chú) |
|---|---|---|---|
| p09 Học bằng cách dự đoán chữ tiếp theo | Xiao và Zhu, mục 2.1 và 2.1.2. | Chưa đối chiếu máy. |  |
| p10 Kiến trúc decoder-only Transformer | Xiao và Zhu, mục 2.1.1. | Đã tìm thấy: kiến trúc decoder-only, mặt nạ nhìn các token trước. |  |
| p11 Huấn luyện ở quy mô lớn | Xiao và Zhu, mục 2.1.2 và 2.2.4. | Đã tìm thấy: "hàng trăm hoặc hàng nghìn GPU" (Xiao và Zhu); scaling law. |  |
| p12 Tinh chỉnh theo chỉ dẫn | Xiao và Zhu, mục 2.1.3. | Tìm thấy câu "chỉ tính loss cho các token được che" trong Xiao và Zhu; Long đọc lại mục 2.1.3 xem đúng với "chỉ phần câu trả lời tính loss". |  |
| p13 Căn chỉnh mô hình | Xiao và Zhu, mục 2.1.4. | Đã tìm thấy: ví dụ hỏi cách chế tạo vũ khí (Xiao và Zhu). |  |
| p14 RLHF | Xiao và Zhu, mục 2.1.4; Zhao và cộng sự, mục về alignment tuning. | Đã tìm thấy trong Zhao và cộng sự: RLHF giảm bịa ở GPT-4, nhưng có nhược điểm (huấn luyện kém ổn định, cần người đánh giá). |  |
| p15 Fine-tuning và RAG khác nhau thế nào | Xiao và Zhu, mục 3.2.5. | Chưa đối chiếu máy. |  |
| p16 Prompt, mẫu prompt và prompt hệ thống | Xiao và Zhu, mục 3.1.1. | Chưa đối chiếu máy. |  |
| p17 Học trong ngữ cảnh | Xiao và Zhu, mục 3.1.2. | Chưa đối chiếu máy. |  |
| p18 Chuỗi suy luận và chia nhỏ bài toán | Xiao và Zhu, mục 3.2.1 và 3.2.2. | Đã tìm thấy: "medicine, education, and finance" ở phần lợi ích của chain of thought (Xiao và Zhu). |  |
| p19 RAG trong thực tế | Xiao và Zhu, mục 3.2.5. | Chưa đối chiếu máy. |  |
| p20 Giải mã: greedy, beam, lấy mẫu và temperature | Xiao và Zhu, mục 5.1.3; Zhao và cộng sự, mục về decoding. | Đã tìm thấy trong Zhao và cộng sự: đặt temperature = 0 là greedy search; top-k, top-p. |  |
| p21 Ngữ cảnh dài | Xiao và Zhu, mục 2.3. | Đã tìm thấy: ba dạng chuỗi dài (đầu vào dài, đầu ra dài, cả hai). |  |

Cách kiểm mỗi đoạn: mở đúng mục trong PDF, đọc đoạn viết lại, tự hỏi (1) mỗi con số và tên riêng có trong nguồn không, (2) có câu nào nguồn không nói không, (3) có sai nghĩa không. Đoạn nào ✗ thì sửa trong `data/lesson_sample.md` và ghi vào nhật ký `spec.md` §10.

## Phần 2. Câu quiz (`data/quiz.json`)

Đối chiếu đáp án và lời giải với đoạn mã ghi ở cột "Đoạn"; câu nào đáp án không nằm trong đoạn đó thì đánh ✗.

| Quiz | Câu | Đáp án | Đoạn | Người kiểm |
|---|---|---|---|---|
| q1 | 1. Theo bài, LLM được huấn luyện để làm việc cơ bản nào? | Dự đoán phần chữ tiếp theo | p01 |  |
| q1 | 2. Giới hạn và chi phí khi gọi mô hình thường được tính theo đơn vị nào? | Token | p02 |  |
| q1 | 3. Cửa sổ ngữ cảnh bao gồm những phần nào? | Cả phần đầu vào và phần trả lời | p03 |  |
| q1 | 4. Cách nào giúp giảm việc mô hình nói bịa, theo bài? | Đưa tài liệu nguồn, yêu cầu trích đoạn đã dùng và cho phép nói không có trong tài liệu | p05 |  |
| q1 | 5. Chất lượng câu trả lời của RAG phụ thuộc nhiều nhất vào bước nào? | Bước tìm đoạn liên quan | p07 |  |
| q2 | 1. Khi huấn luyện mô hình ngôn ngữ, người ta tối đa hoá đại lượng nào? | Log-likelihood của các chuỗi trong dữ liệu | p09 |  |
| q2 | 2. Khi tính loss lúc tinh chỉnh theo chỉ dẫn, phần nào được tính? | Chỉ phần câu trả lời | p12 |  |
| q2 | 3. Căn chỉnh (alignment) nhằm mục đích gì? | Dẫn dắt mô hình hành xử đúng với giá trị và mục tiêu của con người | p13 |  |
| q2 | 4. Bước nào KHÔNG thuộc bốn bước của RLHF? | Dịch toàn bộ dữ liệu sang ngôn ngữ khác | p14 |  |
| q2 | 5. Điểm khác chính giữa RAG chuẩn và fine-tuning là gì? | RAG chuẩn không cần huấn luyện, fine-tuning cần công sức huấn luyện | p15 |  |
| q3 | 1. Zero-shot là cách prompt như thế nào? | Không đưa ví dụ nào, chỉ mô tả việc cần làm | p17 |  |
| q3 | 2. Chain of thought (chuỗi suy luận) yêu cầu mô hình làm gì? | Viết ra từng bước lập luận trước khi kết luận | p18 |  |
| q3 | 3. Trong prompt RAG, nên dặn mô hình thế nào khi thông tin được cung cấp không đủ? | Nói là không trả lời được | p19 |  |
| q3 | 4. Greedy search chọn gì ở mỗi bước sinh? | Token có xác suất cao nhất | p20 |  |
| q3 | 5. Tóm tắt một tài liệu rất dài thuộc dạng bài toán chuỗi dài nào? | Đầu vào dài, đầu ra ngắn | p21 |  |
