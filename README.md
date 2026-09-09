# Tsubogawa Watch — PWA Lite cho iPhone

Bản này được làm theo hướng đơn giản nhất:
- Không cần Xcode.
- Không cần Apple Developer.
- Không cần mua domain.
- Không cần đăng ký API Gifu.
- Mở bằng Safari rồi Add to Home Screen.
- Hiển thị mực nước trạm 関 (Seki), xu hướng ↑/↓/→, ngưỡng cảnh báo và camera 津保川・関.
- Tự làm mới mỗi 60 giây.

## Cách dùng nhanh
PWA cần được đưa lên một địa chỉ HTTPS để iPhone cài vào Home Screen đầy đủ.
Bạn có thể dùng hosting miễn phí như GitHub Pages / Cloudflare Pages / Netlify / Vercel.
Tên miền riêng là KHÔNG bắt buộc; nền tảng sẽ cấp một link miễn phí.

Sau khi có link:
1. Mở link bằng Safari trên iPhone.
2. Bấm nút Share (ô vuông có mũi tên lên).
3. Chọn Add to Home Screen / Thêm vào Màn hình chính.
4. Bấm Add.

## Nguồn
- Mực nước chính thức: https://www.kasen.pref.gifu.lg.jp/h/Valley_6_450.html
- Camera chính thức: https://www.kasen.pref.gifu.lg.jp/h/Camera513_S.html

## Lưu ý kỹ thuật
Trang Gifu không cung cấp CORS trực tiếp cho bản PWA tĩnh, nên phần số mực nước thử lần lượt các dịch vụ đọc trang công khai không cần đăng ký.
Nếu dịch vụ trung gian lỗi, app có nút mở thẳng trang Gifu.
Ảnh camera được thử tải trực tiếp từ URL ảnh chính thức theo các mốc 10 phút gần nhất.

Không dùng app này như nguồn cảnh báo khẩn cấp duy nhất.
