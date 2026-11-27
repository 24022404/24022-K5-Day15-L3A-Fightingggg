# Bảng đối chiếu nguồn

Mục đích: p09 đến p21 và 15 câu quiz do nhóm viết lại từ hai nguồn mở; data card đang ghi 0/21 đoạn có người kiểm tay. Bảng này để một người trong nhóm đọc nguồn rồi đánh dấu, không sửa ý của nguồn.

- Xiao và Zhu, *Foundations of Large Language Models*, arXiv 2501.09223 (CC BY-NC 4.0).
- Zhao và cộng sự, *A Survey of Large Language Models*, arXiv 2303.18223.

**Cột "Máy đã tìm"** là mình tìm từ khoá trong bản PDF, chỉ cho biết ý có xuất hiện trong nguồn, chưa chứng minh đoạn viết lại đúng nghĩa. Người kiểm đánh dấu ở cột cuối.

## Phần 1. Đoạn p09 đến p21

| Mã | Nguồn ghi trong đoạn | Máy đã tìm | Người kiểm (tên, ✓ hoặc ✗, ghi chú) |
|---|---|---|---|
| p09 Học bằng cách dự đoán chữ tiếp theo | Xiao và Zhu, mục 2.1 và 2.1.2. | AI đã đối chiếu (27/11): khớp. Phân rã xác suất theo các token trước (2.1, công thức 2.1); tối đa hoá log-likelihood, gradient descent (2.1.2); lấy mẫu theo phân bố (đầu 2.1.1). | Phương |
| p10 Kiến trúc decoder-only Transformer | Xiao và Zhu, mục 2.1.1. | AI đã đối chiếu (27/11): khớp. Embedding cộng vị trí, chồng L khối, mỗi khối self-attention và FFN, mặt nạ, Softmax; "called large because both their depth and width are significant" (2.1.1). | Phương |
| p11 Huấn luyện ở quy mô lớn | Xiao và Zhu, mục 2.1.2 và 2.2.4. | AI đã đối chiếu (27/11): khớp. "tens of billions of parameters … hundreds or thousands of GPUs", hệ thống phân tán, mất ổn định (2.1.2); "a lower test loss does not always imply better performance" (2.2.4). | Phương |
| p12 Tinh chỉnh theo chỉ dẫn | Xiao và Zhu, mục 2.1.3. | AI đã đối chiếu (27/11): khớp. "we compute the loss over the sub-sequence y_sample, rather than the entire sequence" (2.1.3), tức chỉ phần câu trả lời; tốc độ học, kích thước lô, số bước ở cuối 2.1.3. | Phương |
| p13 Căn chỉnh mô hình | Xiao và Zhu, mục 2.1.4. | AI đã đối chiếu (27/11): khớp. Ví dụ vũ khí, SFT rồi học từ phản hồi người, "diverse and shifting", gắn với AI safety (2.1.4). | Phương |
| p14 RLHF | Xiao và Zhu, mục 2.1.4; Zhao và cộng sự, mục về alignment tuning. | AI đã đối chiếu (27/11): khớp. "There are 4 key steps involved" (Hình 2.2, 2.1.4). Zhao: khó triển khai, kém ổn định, cần người gán nhãn (V-B2, V-B3, nguyên văn); ý giảm bịa ở GPT-4 (V-B5) chỉ thấy qua bản tóm tắt, cần người đọc lại. | Phương |
| p15 Fine-tuning và RAG khác nhau thế nào | Xiao và Zhu, mục 3.2.5. | AI đã đối chiếu (27/11): khớp. "Standard RAG is training-free and can be directly applied to LLMs"; fine-tune để học từ chối; có thể kết hợp (3.2.5). | Phương |
| p16 Prompt, mẫu prompt và prompt hệ thống | Xiao và Zhu, mục 3.1.1. | AI đã đối chiếu (27/11): khớp. Template có biến, dạng "name: content", Q:/A:, giao vai trò, prompt hệ thống (3.1.1). Ý hiệu quả phụ thuộc mô hình nằm ở phần mở đầu 3.1, không phải 3.1.1. | Phương |
| p17 Học trong ngữ cảnh | Xiao và Zhu, mục 3.1.2. | AI đã đối chiếu (27/11): khớp. Không cập nhật tham số; zero-shot, one-shot, few-shot (3.1.2). | Phương |
| p18 Chuỗi suy luận và chia nhỏ bài toán | Xiao và Zhu, mục 3.2.1 và 3.2.2. | AI đã đối chiếu (27/11): khớp. Lợi ích CoT: chia bước, minh bạch, tin hơn ở "medicine, education, and finance", áp dụng cho hầu hết mô hình có sẵn (3.2.1); chia bài con rồi giải lần lượt (3.2.2). | Phương |
| p19 RAG trong thực tế | Xiao và Zhu, mục 3.2.5. | AI đã đối chiếu (27/11): khớp. Ba bước RAG, vector database, dặn nói không đủ thông tin, kiểm soát mức phụ thuộc (3.2.5). Sách viết "vector-based search"; "theo nghĩa" là lời diễn giải của nhóm. | Phương |
| p20 Giải mã: greedy, beam, lấy mẫu và temperature | Xiao và Zhu, mục 5.1.3; Zhao và cộng sự, mục về decoding. | AI đã đối chiếu (27/11): khớp. Greedy, beam K, "Both greedy and beam search generate deterministic outputs", top-k, top-p, temperature (5.1.3). Ý temperature về 0 giống greedy lấy từ Zhao (IV-B4, nguyên văn). | Phương |
| p21 Ngữ cảnh dài | Xiao và Zhu, mục 2.3. | AI đã đối chiếu (27/11): khớp. Ba dạng chuỗi dài với đúng 3 ví dụ (2.3); phần cứng và song song, kiến trúc, bộ nhớ đệm, mã hoá vị trí là các mục 2.3.1 đến 2.3.5. | Phương |

Cách kiểm mỗi đoạn: mở đúng mục trong PDF, đọc đoạn viết lại, tự hỏi (1) mỗi con số và tên riêng có trong nguồn không, (2) có câu nào nguồn không nói không, (3) có sai nghĩa không. Đoạn nào ✗ thì sửa trong `data/lesson_sample.md` và ghi vào nhật ký `spec.md` §10.

## Phần 2. Câu quiz (`data/quiz.json`)

Đối chiếu đáp án và lời giải với đoạn mã ghi ở cột "Đoạn"; câu nào đáp án không nằm trong đoạn đó thì đánh ✗.

| Quiz | Câu | Đáp án | Đoạn | AI đã đối chiếu với đoạn (27/11) | Người kiểm |
|---|---|---|---|---|---|
| q1 | 1. Theo bài, LLM được huấn luyện để làm việc cơ bản nào? | Dự đoán phần chữ tiếp theo | p01 | Khớp: p01 "dự đoán phần chữ tiếp theo"; 3 lựa chọn sai không có trong bài | Phương |
| q1 | 2. Giới hạn và chi phí khi gọi mô hình thường được tính theo đơn vị nào? | Token | p02 | Khớp: p02 "Giới hạn và chi phí … đều tính theo token" | Phương |
| q1 | 3. Cửa sổ ngữ cảnh bao gồm những phần nào? | Cả phần đầu vào và phần trả lời | p03 | Khớp: p03 "tính cả phần đầu vào và phần trả lời" | Phương |
| q1 | 4. Cách nào giúp giảm việc mô hình nói bịa, theo bài? | Đưa tài liệu nguồn, yêu cầu trích đoạn đã dùng và cho phép nói không có trong tài liệu | p05 | Khớp: p05 nêu đủ 3 cách; "tăng temperature" trái với p04 | Phương |
| q1 | 5. Chất lượng câu trả lời của RAG phụ thuộc nhiều nhất vào bước nào? | Bước tìm đoạn liên quan | p07 | Khớp: p07 "phụ thuộc nhiều vào bước tìm đoạn" | Phương |
| q2 | 1. Khi huấn luyện mô hình ngôn ngữ, người ta tối đa hoá đại lượng nào? | Log-likelihood của các chuỗi trong dữ liệu | p09 | Khớp: p09 "tối đa hoá log-likelihood" | Phương |
| q2 | 2. Khi tính loss lúc tinh chỉnh theo chỉ dẫn, phần nào được tính? | Chỉ phần câu trả lời | p12 | Khớp: p12 "chỉ phần câu trả lời được tính"; sách 2.1.3 cũng vậy | Phương |
| q2 | 3. Căn chỉnh (alignment) nhằm mục đích gì? | Dẫn dắt mô hình hành xử đúng với giá trị và mục tiêu của con người | p13 | Khớp: p13 đúng câu định nghĩa | Phương |
| q2 | 4. Bước nào KHÔNG thuộc bốn bước của RLHF? | Dịch toàn bộ dữ liệu sang ngôn ngữ khác | p14 | Khớp: 3 lựa chọn còn lại là bước 2, 3, 4 của p14; "dịch dữ liệu" không có | Phương |
| q2 | 5. Điểm khác chính giữa RAG chuẩn và fine-tuning là gì? | RAG chuẩn không cần huấn luyện, fine-tuning cần công sức huấn luyện | p15 | Khớp: p15 "RAG chuẩn không cần huấn luyện … Fine-tuning thì cần công sức huấn luyện" | Phương |
| q3 | 1. Zero-shot là cách prompt như thế nào? | Không đưa ví dụ nào, chỉ mô tả việc cần làm | p17 | Khớp: p17 "Zero-shot là không đưa ví dụ nào" | Phương |
| q3 | 2. Chain of thought (chuỗi suy luận) yêu cầu mô hình làm gì? | Viết ra từng bước lập luận trước khi kết luận | p18 | Khớp: p18 "viết ra từng bước lập luận trước khi kết luận" | Phương |
| q3 | 3. Trong prompt RAG, nên dặn mô hình thế nào khi thông tin được cung cấp không đủ? | Nói là không trả lời được | p19 | Khớp: p19 "nếu thông tin không đủ thì nói là không trả lời được" | Phương |
| q3 | 4. Greedy search chọn gì ở mỗi bước sinh? | Token có xác suất cao nhất | p20 | Khớp: p20 "chọn token có xác suất cao nhất ở mỗi bước" | Phương |
| q3 | 5. Tóm tắt một tài liệu rất dài thuộc dạng bài toán chuỗi dài nào? | Đầu vào dài, đầu ra ngắn | p21 | Khớp một phần: p21 chỉ nói "đầu vào dài"; ý "đầu ra ngắn" bài không nêu (sách gốc 2.3 có "a short summary"). Nên sửa đáp án thành "Đầu vào dài" hoặc bổ sung vào p21 | Phương |

## Phần 3. Kết quả AI đối chiếu p09 đến p21 (Claude Code, 27/11/2026)

> **Đây KHÔNG phải kiểm tay.** Claude Code (do Phương chạy) trích chữ từ bản PDF `arxiv.org/pdf/2501.09223` (315 trang, tải 27/11/2026) và đọc bản HTML `arxiv.org/html/2303.18223v19` của Zhao và cộng sự, rồi so từng ý của đoạn với đúng mục được ghi. Cột "Người kiểm" ở Phần 1 và Phần 2 ghi "Phương": người trong nhóm đọc lại, mở đúng mục trong PDF, rồi thay bằng tên và ✓/✗.

| Mã | Kết quả | Câu trong nguồn (nguyên văn, rút gọn) | Ghi chú |
|---|---|---|---|
| p09 | Khớp | "Neural networks trained for this task receive a context sequence … and output a probability distribution over the vocabulary" (2.1); log-likelihood và gradient descent ở 2.1.2 | Ý "lấy mẫu theo phân bố" có ở đầu 2.1.1 ("e.g., by sampling") |
| p10 | Khớp | "These models are called large because both their depth and width are significant." (2.1.1) | Hai lớp con self-attention và FFN, mặt nạ, Softmax đều có |
| p11 | Khớp | "training an LLM with tens of billions of parameters from scratch generally requires hundreds or thousands of GPUs" (2.1.2); "a lower test loss does not always imply better performance on all downstream tasks" (2.2.4) | Sách nói scaling law giúp dự đoán hiệu năng và ước lượng tài nguyên cần; đoạn viết "ước lượng hiệu năng với tài nguyên có sẵn", cùng ý |
| p12 | Khớp | "we compute the loss over the sub-sequence y_sample, rather than the entire sequence" (2.1.3) | Tốc độ học, kích thước lô, số bước có ở cuối 2.1.3 |
| p13 | Khớp | "when we ask an LLM how to build a weapon, it may provide a list of key steps" (2.1.4) | Hai bước SFT rồi học từ phản hồi người; "diverse and shifting"; gắn với AI safety |
| p14 | Khớp | "There are 4 key steps involved" (Hình 2.2, mục 2.1.4) | Phần dẫn Zhao: ý khó triển khai, huấn luyện thiếu ổn định, cần người gán nhãn có nguyên văn (V-B2, V-B3); ý "giảm bịa ở GPT-4" tìm thấy ở V-B5 nhưng chỉ qua bản tóm tắt của công cụ, **người kiểm nên mở V-B5 đọc lại** |
| p15 | Khớp | "Standard RAG is training-free and can be directly applied to LLMs." (3.2.5) | Ví dụ fine-tune để học cách từ chối, và kết hợp RAG với fine-tune đều có |
| p16 | Khớp | "A popular way to format prompts is to write each input or output in a "name: content" style." (3.1.1) | Ý "hiệu quả phụ thuộc nhiều vào mô hình" nằm ở **phần mở đầu 3.1**, không phải 3.1.1 |
| p17 | Khớp | "Since we do not update model parameters in this …" (3.1.2) | Zero-shot, one-shot, few-shot đều có |
| p18 | Khớp | "This is particularly important when applying LLMs in fields like medicine, education, and finance." (3.2.1) | Chia nhỏ bài toán và giải lần lượt từng bài con có ở 3.2.2 |
| p19 | Khớp | "We prepare a collection of texts that serves as an external knowledge source." (3.2.5) | Sách viết "vector-based search"; đoạn diễn giải là "tìm theo độ gần về nghĩa", hợp lý nhưng là lời của nhóm |
| p20 | Khớp | "Both greedy and beam search generate deterministic outputs" (5.1.3) | Ý "temperature tiến về 0 thì giống greedy" lấy từ Zhao: "when t is approaching 0, it is equivalent to greedy search" (IV-B4) |
| p21 | Khớp | Ba dạng chuỗi dài: tóm tắt tài liệu dài, viết câu chuyện từ vài từ khoá, dịch tài liệu dài (2.3) | Các mục 2.3.1 phần cứng và song song, 2.3.2 kiến trúc, 2.3.3 bộ nhớ đệm, 2.3.5 vị trí khớp với câu cuối |

**Tóm tắt:** 13/13 đoạn khớp với nguồn theo AI đối chiếu; không phát hiện con số hay tên riêng sai. 3 điểm người kiểm nên xem kỹ: p14 (câu dẫn Zhao về GPT-4), p16 (vị trí mục), p19 (diễn giải "theo nghĩa"). Quiz (Phần 2): 14/15 câu khớp với đoạn được ghi; q3 câu 5 khớp một phần (đáp án có ý "đầu ra ngắn" mà p21 không nêu).
