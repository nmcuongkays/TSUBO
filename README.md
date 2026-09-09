# Tsubogawa Watch V2.9 — INSTANT LAST GOOD

Sửa hiện tượng vừa mở app thấy dữ liệu GitHub cũ + lỗi giả
`waiting-for-first-github-action-run`, rồi một lúc sau mới nhảy sang LIVE.

V2.9:
- Không còn seed health ở trạng thái lỗi.
- Mỗi khi app thấy dữ liệu mới tốt (GitHub hoặc LIVE), nó lưu vào localStorage trên iPhone.
- Lần mở sau, dữ liệu tốt gần nhất hiện ngay lập tức.
- Sau đó app mới kiểm tra GitHub/LIVE ở nền và cập nhật nếu có mốc mới.
- Giữ nút CẬP NHẬT NGAY ở đầu trang.
