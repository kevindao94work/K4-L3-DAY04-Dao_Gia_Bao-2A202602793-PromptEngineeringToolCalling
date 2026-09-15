# Kiểm tra Safari bởi Codex (không phải teammate)

- Môi trường: macOS, Safari, http://127.0.0.1:8765.
- Server được mở bằng `.venv/bin/python ui_server.py --port 8765` từ starter_v0; HTML/JS/CSS HTTP 200.
- Computer Use ban đầu chờ Accessibility/Screen Recording; sau đó đã truy cập được Safari và mở tab mới.
- Đã nhìn thấy header Helpdesk, ô nhập, version/hash/model, và gửi yêu cầu SSO production bằng nút mẫu + Gửi.
- Đã nhìn thấy `check_service_status`, args service=sso/environment=production, result operational và timestamp snapshot.
- Reload bản chat-ui-v2; gửi yêu cầu ticket mẫu, nhìn thấy `prepare_ticket`, payload và hai nút Xác nhận/Hủy.
- Phát hiện preview ban đầu bỏ asset_id (chuỗi rỗng dù summary có PR-404). Sửa rõ asset_id=PR-404, priority=high qua lượt mới; nhìn thấy payload cập nhật và thông báo xác nhận cũ hết hiệu lực. Đây là lỗi trích args cần người dùng review, không được che.
- Nhấn Hủy; UI hiện cancelled, Không tạo ticket, Không gọi công cụ, preview biến mất.
- Sau đó Computer Use gặp lỗi clipboard/noWindowsAvailable và input không cập nhật, nên chưa xác minh trực tiếp màu lỗi hoặc download bằng click cuối. D05 HTTP transcript xác minh error result và reply; source UI hiển thị result.error bằng lớp error. Không ghi các kiểm tra browser chưa thực hiện là đã đạt.
- Không có thành viên khác thực hiện theo README trong bằng chứng này; teammate check vẫn pending.
