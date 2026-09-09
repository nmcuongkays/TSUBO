# V2.6 — SỬA NÚT LÀM MỚI

## Lỗi cũ
Ví dụ:
- App/GitHub: 15:40
- Website Gifu: 15:50

V2.5 chỉ thử LIVE khi dữ liệu GitHub cũ hơn 12 phút, nên 15:40 vẫn chưa vượt ngưỡng.
Bấm Làm mới vì thế chỉ đọc lại 15:40.

## V2.6
Khi bấm `Kiểm tra dữ liệu mới ngay`:
1. Xóa cache LIVE cũ trong app.
2. Gọi nguồn Gifu ngay lập tức.
3. So timestamp với GitHub.
4. Nếu LIVE mới hơn thì đổi màn hình và ghép điểm mới vào timeline.

Tự động:
- App kiểm tra 20 giây/lần.
- Khi timestamp GitHub cũ hơn 6 phút, app bắt đầu thử LIVE Gifu.

## Cập nhật
Upload đè toàn bộ file lên repo -> Commit.
Sau đó mở Safari refresh. Nếu PWA vẫn giữ code cũ, xóa icon Home Screen và thêm lại.
