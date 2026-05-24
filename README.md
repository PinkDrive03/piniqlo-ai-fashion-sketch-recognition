# PINIQLO - AI Sketch Recognition

PINIQLO là một website ứng dụng trí tuệ nhân tạo để nhận dạng trang phục và phụ kiện thời trang từ nét vẽ chuột. Người dùng có thể phác thảo trực tiếp trên khung Canvas, sau đó hệ thống sẽ xử lý hình vẽ và đưa ra dự đoán món đồ phù hợp nhất.

## Giới thiệu

Dự án được xây dựng nhằm mô phỏng một hệ thống nhận dạng hình ảnh đơn giản trên nền tảng web. Thay vì tải ảnh có sẵn, người dùng có thể tự vẽ bằng chuột ngay trên giao diện. Sau khi nhấn nút nhận dạng, mô hình AI sẽ phân tích nét vẽ và trả về kết quả dự đoán cùng mức độ tin cậy.

Website có giao diện trực quan, màu sắc nhẹ nhàng, dễ sử dụng và phù hợp để trình bày trong bài báo cáo môn học về trí tuệ nhân tạo hoặc học máy.

## Chức năng chính

- Vẽ phác thảo trực tiếp bằng chuột trên khung Canvas.
- Điều chỉnh cỡ nét vẽ.
- Xóa khung vẽ để nhập lại hình mới.
- Nhận dạng hình vẽ bằng mô hình AI.
- Hiển thị nhãn dự đoán phù hợp nhất.
- Hiển thị độ tin cậy của kết quả.
- Hiển thị xác suất dự đoán cho từng loại trang phục/phụ kiện.
- Hỗ trợ nhận dạng 10 nhóm đối tượng thời trang.

## Các nhóm đối tượng hỗ trợ

Website hỗ trợ nhận dạng các loại trang phục và phụ kiện sau:

1. Áo thun
2. Quần dài
3. Áo khoác
4. Quần short
5. Áo len
6. Giày
7. Tất
8. Đồ lót
9. Mũ
10. Ba lô

## Cách hoạt động

Quy trình nhận dạng của hệ thống gồm các bước chính:

1. Người dùng vẽ một món đồ thời trang trên khung Canvas.
2. Hệ thống lấy dữ liệu hình ảnh từ Canvas.
3. Hình vẽ được tiền xử lý để phù hợp với đầu vào của mô hình AI.
4. Mô hình dự đoán xác suất của từng lớp trang phục/phụ kiện.
5. Website chọn lớp có xác suất cao nhất làm kết quả cuối cùng.
6. Kết quả được hiển thị kèm độ tin cậy và biểu đồ phần trăm.

## Giao diện website

Giao diện gồm các phần chính:

- Phần giới thiệu hệ thống nhận dạng.
- Khu vực vẽ phác thảo bằng chuột.
- Nút nhận dạng và nút xóa khung vẽ.
- Bảng kết quả dự đoán từ mô hình.
- Danh sách xác suất của từng loại trang phục/phụ kiện.

## Công nghệ sử dụng

Dự án sử dụng các công nghệ chính:

- HTML, CSS, JavaScript cho giao diện web.
- Canvas API để xử lý khu vực vẽ bằng chuột.
- Mô hình AI/Machine Learning để nhận dạng hình ảnh.
- TensorFlow/Keras hoặc TensorFlow.js để huấn luyện và sử dụng mô hình dự đoán.

## Hướng dẫn chạy dự án

Clone project về máy:

```bash
git clone https://github.com/your-username/pingo-ai-fashion-sketch-recognition.git
cd pingo-ai-fashion-sketch-recognition
