# Bài mẫu: Nền tảng LLM (do nhóm Fightingggg tự viết, không chép tài liệu khoá)

> Bài này thay cho lời giảng của video khi chạy thử. Mỗi đoạn có mã để trợ giảng trích dẫn.

**p01 · LLM là gì.** Mô hình ngôn ngữ lớn (LLM) được huấn luyện trên lượng văn bản rất lớn để dự đoán phần chữ tiếp theo. Khi trả lời, nó sinh từng mẩu chữ một, mỗi lần chọn mẩu có khả năng cao dựa trên những gì đã có.

**p02 · Token.** Mô hình không đọc theo từ mà theo token, là các mẩu chữ nhỏ hơn hoặc bằng một từ. Giới hạn và chi phí khi gọi mô hình đều tính theo token, nên cùng một nội dung viết dài hơn thì tốn nhiều hơn. Tiếng Việt thường tốn nhiều token hơn tiếng Anh cho cùng ý.

**p03 · Cửa sổ ngữ cảnh.** Cửa sổ ngữ cảnh là số token tối đa mô hình nhìn thấy trong một lần gọi, tính cả phần đầu vào và phần trả lời. Điều gì nằm ngoài cửa sổ thì mô hình không biết, nên tài liệu quá dài phải cắt nhỏ hoặc chỉ đưa phần liên quan.

**p04 · Temperature.** Temperature điều chỉnh mức ngẫu nhiên khi chọn mẩu chữ tiếp theo. Giá trị thấp cho kết quả ổn định, ít khác nhau giữa các lần chạy. Giá trị cao cho kết quả đa dạng hơn nhưng dễ lệch ý. Việc cần chính xác nên dùng giá trị thấp.

**p05 · Bịa thông tin.** Mô hình có thể nói điều nghe rất hợp lý nhưng sai, vì nó dự đoán chữ chứ không tra cứu sự thật. Cách giảm: đưa tài liệu nguồn vào, yêu cầu trích dẫn đoạn đã dùng, và cho phép mô hình nói "không có trong tài liệu" thay vì đoán.

**p06 · Prompt.** Prompt hệ thống đặt vai trò và quy tắc cho mô hình, prompt người dùng là yêu cầu cụ thể. Nêu rõ định dạng đầu ra, đưa một vài ví dụ mẫu và nói rõ điều không được làm sẽ cho kết quả đều tay hơn.

**p07 · RAG.** RAG là cách tìm trước các đoạn liên quan trong kho tài liệu, rồi đưa chúng vào prompt để mô hình trả lời có căn cứ. Chất lượng câu trả lời phụ thuộc nhiều vào bước tìm đoạn: tìm sai đoạn thì mô hình trả lời sai dù viết rất trôi chảy.

**p08 · Đánh giá.** Không nên tin vào cảm giác "có vẻ ổn". Hãy dựng bộ câu thử có đáp án mong đợi, chạy lại sau mỗi lần sửa và đếm tỉ lệ đạt. Phải có cả câu khó và câu cần từ chối, vì chỉ thử câu dễ sẽ cho điểm cao giả.
