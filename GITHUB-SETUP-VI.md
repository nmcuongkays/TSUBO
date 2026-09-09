# CÀI Tsubogawa Watch V2 LÊN GITHUB PAGES

## 1. Tạo repository
Tạo repo PUBLIC, ví dụ: `tsubogawa-watch`.

## 2. Upload
Giải nén ZIP này và upload TOÀN BỘ nội dung vào nhánh `main`.
Phải có cả thư mục `.github/workflows/`.

## 3. Cho phép bot ghi dữ liệu
GitHub repo -> Settings -> Actions -> General -> Workflow permissions
chọn **Read and write permissions** -> Save.

## 4. Chạy lần đầu
Vào tab **Actions** -> `Update Tsubogawa data` -> `Run workflow`.
Sau khi chạy xong, thư mục `data/` sẽ có ảnh camera mới nhất và số liệu mới.

## 5. Bật GitHub Pages
Settings -> Pages -> Build and deployment:
- Source: Deploy from a branch
- Branch: main
- Folder: /(root)
-> Save.

Link thường là:
`https://TEN-CUA-BAN.github.io/tsubogawa-watch/`

## 6. Cài trên iPhone
Mở link bằng Safari -> Share -> Add to Home Screen.

## Timeline hoạt động thế nào?
- File ban đầu có khoảng 24 giờ lịch sử từ trang công khai Gifu.
- GitHub Actions kiểm tra mỗi 5 phút.
- Nguồn Gifu thường phát mực nước mới theo mốc 10 phút.
- Mỗi số mới được giữ trong `data/history.json`.
- App có 24 giờ / 7 ngày / 30 ngày.
- Sau khi chạy, timeline 7/30 ngày sẽ tự đầy dần. Hệ thống giữ 45 ngày.

## Camera
V2 lấy ảnh `_fenl.jpg` từ trang camera lớn của Gifu và lưu thành
`data/camera-latest.jpg`. Giao diện giới hạn ảnh ở 320 px để tránh kéo giãn
nguồn camera vốn có độ phân giải thấp.

## Nguồn chính thức
Mực nước: https://www.kasen.pref.gifu.lg.jp/h/Valley_6_450.html
Camera lớn: https://www.kasen.pref.gifu.lg.jp/h/Camera513_B.html

## Lưu ý
GitHub Actions cho lịch tối thiểu 5 phút, nhưng lịch có thể bị trễ khi hệ thống
GitHub tải cao. App không thay thế cảnh báo thiên tai chính thức.
