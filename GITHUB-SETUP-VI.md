# CẬP NHẬT V2.4 — SỬA LỖI ĐỨNG DỮ LIỆU

## Vì sao bản trước có thể đứng?
Có hai lớp có thể chậm:
1. GitHub Actions có thể chạy trễ.
2. Yêu cầu tới trang Gifu có thể nhận bản cache cũ.

## V2.4 sửa thế nào?
- Script GitHub thêm cache-busting khi gọi Gifu.
- PWA vẫn đọc dữ liệu GitHub trước.
- Nếu timestamp mực nước cũ hơn khoảng 12 phút, PWA tự thử đọc trang Gifu qua
  dịch vụ CORS dự phòng.
- App so sánh timestamp và chỉ lấy bản mới hơn.
- Ví dụ GitHub đang 15:10 nhưng nguồn dự phòng đọc được 15:40 thì màn hình đổi
  ngay sang 15:40 và ghép 15:20/15:30/15:40 vào timeline.

## Cách cập nhật
1. Giải nén ZIP.
2. Upload đè toàn bộ lên repo cũ, gồm `.github/workflows/update.yml`.
3. Commit.
4. Actions -> Update Tsubogawa data -> Run workflow.
5. Mở GitHub Pages bằng Safari và refresh.
6. Nếu PWA Home Screen vẫn giữ bản cũ, xóa icon rồi Add to Home Screen lại.

## Quyền Actions
Settings -> Actions -> General -> Workflow permissions ->
`Read and write permissions`.

## Dấu hiệu hoạt động đúng
Màn hình sẽ hiện một trong hai:
- `✓ GitHub hoạt động ...`
- `✓ ĐANG DÙNG NGUỒN LIVE Gifu ... GitHub đang chậm`

Và dòng trên cùng hiện riêng:
- timestamp dữ liệu Gifu,
- timestamp GitHub lấy,
- giờ app vừa kiểm tra.
