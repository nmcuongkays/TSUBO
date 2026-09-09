# V2.9 — MỞ APP HIỆN DỮ LIỆU TỐT NGAY

## Vì sao bản cũ hiện 'Số GitHub đang cũ ... waiting-for-first-github-action-run'?
Trong ZIP cũ có file health mẫu mang trạng thái lỗi, và latest.json có thể là dữ liệu
seed cũ. App vẽ hai file đó trước, rồi vài giây sau mới đọc LIVE.

## V2.9
- Xóa lỗi mẫu khỏi health.json.
- Lưu dữ liệu tốt gần nhất trên chính iPhone.
- Mở app lần sau: hiện dữ liệu tốt gần nhất ngay.
- Kiểm tra LIVE Gifu chạy sau ở nền.

## Cập nhật
Upload đè ZIP lên repo -> Commit -> chờ Pages deploy -> refresh Safari.
Nếu PWA vẫn giữ code cũ, xóa icon Home Screen rồi Add to Home Screen lại.
