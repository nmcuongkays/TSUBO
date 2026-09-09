# Tsubogawa Watch V2.4 — LIVE FIX

Sửa lỗi app đứng ở dữ liệu cũ.

- Timeline 24 giờ.
- Chạm timeline để xem ảnh camera gần thời điểm đã chọn.
- GitHub Actions tiếp tục lưu lịch sử + camera.
- Collector Gifu có cache-busting.
- Nếu `data/latest.json` cũ hơn ~12 phút, PWA tự thử đọc trang Gifu qua nguồn CORS dự phòng.
- App so sánh timestamp và luôn ưu tiên dữ liệu mới hơn.
- Điểm 10 phút mới đọc trực tiếp được ghép ngay vào timeline.
- Nút VỀ REALTIME cho camera.

Không dùng app như nguồn cảnh báo thiên tai duy nhất.
