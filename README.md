# Tsubogawa Watch V2.6 — FORCE LIVE REFRESH

Sửa lỗi web Gifu đã có mốc mới nhưng bấm Làm mới trong app vẫn giữ mốc cũ.

Nguyên nhân V2.5:
- App chỉ gọi nguồn LIVE khi timestamp GitHub cũ hơn ~12 phút.
- Nếu GitHub = 15:40 và Gifu = 15:50 thì chênh chỉ 10 phút, nên app chưa gọi LIVE.

V2.6:
- Nút `Kiểm tra dữ liệu mới ngay` luôn ép đọc LIVE Gifu.
- Xóa direct-cache cũ trước khi refresh thủ công.
- Auto refresh thử LIVE Gifu sớm hơn: khi timestamp GitHub cũ hơn 6 phút.
- Luôn so sánh timestamp và chỉ dùng bản mới hơn.
