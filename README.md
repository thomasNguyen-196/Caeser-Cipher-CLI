# Caesar Cipher CLI Tool

## Giới thiệu

Đây là một công cụ dòng lệnh (CLI) giúp mã hóa và giải mã văn bản sử dụng thuật toán Caesar Cipher. Dự án cung cấp mã nguồn minh họa cách hoạt động của thuật toán mã hóa cổ điển này.

## Tính năng

- Mã hóa văn bản sử dụng thuật toán Caesar Cipher với khóa dịch chuyển tùy chọn
- Giải mã văn bản đã mã hóa bằng Caesar Cipher
- Hỗ trợ nhập văn bản và khóa dịch chuyển từ dòng lệnh
- Hiển thị kết quả mã hóa hoặc giải mã trực tiếp trên màn hình
- Xử lý ký tự chữ cái, giữ nguyên ký tự không phải chữ cái
- Giao diện dòng lệnh thân thiện, dễ sử dụng

## Yêu cầu

- Python 3.7+ (được định nghĩa trong `pyproject.toml`)

## Hướng dẫn cài đặt và sử dụng

Dự án này được đóng gói để có thể cài đặt như một công cụ dòng lệnh.

1. **Cài đặt dự án:**

   Mở terminal ở thư mục gốc và chạy lệnh sau. Lệnh này sẽ cài đặt gói ở chế độ "editable" (có thể chỉnh sửa), đồng thời tự động cài đặt các thư viện phụ thuộc:

    ```bash
    pip install -e .
    ```

2. **Chạy chương trình:**

   Sau khi cài đặt thành công, bạn có thể gọi trực tiếp công cụ từ bất kỳ đâu bằng lệnh:
    ```bash
    caesar
    ```

3. Làm theo hướng dẫn trên màn hình để mã hóa hoặc giải mã văn bản.

## Đóng góp

Mọi đóng góp hoặc phản hồi vui lòng tạo issue hoặc pull request trên repository này.