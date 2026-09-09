# V3.0 — SỬA TRIỆT ĐỂ CẢNH BÁO GITHUB CŨ

## Lỗi V2.9
V2.9 có last-good, nhưng khi app tải xong `latest.json` từ GitHub cũ,
nó lại gọi `saveLastGood(ghLatest)` và có thể ghi đè last-good mới hơn.

## V3.0
- Last-good chỉ được cập nhật nếu timestamp mới hơn hoặc bằng bản đang lưu.
- Mở app: so sánh iPhone và GitHub, bản mới hơn thắng.
- Sau đó kiểm tra LIVE Gifu.
- Không hiện cảnh báo GitHub cũ ngay lúc mở; chỉ hiển thị trạng thái đồng bộ.

## Cập nhật
Upload đè toàn bộ ZIP -> Commit -> chờ Pages deploy.
Nếu PWA vẫn giữ JS cũ: xóa icon Home Screen rồi Add to Home Screen lại.
