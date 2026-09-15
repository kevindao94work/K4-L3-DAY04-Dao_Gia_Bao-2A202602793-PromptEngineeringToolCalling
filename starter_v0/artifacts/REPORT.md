# Helpdesk — So sánh v0–v3

## 1. Bài toán và thiết kế đã chốt trước v0

- **Lĩnh vực:** IT Helpdesk nội bộ, công ty giả lập Northstar Labs.
- **Người dùng:** nhân viên cần hỗ trợ tài khoản, thiết bị và dịch vụ IT.
- **Nhiệm vụ:** tra cứu nhân viên; kiểm tra thiết bị và trạng thái dịch vụ; tìm hướng dẫn; trình bày findings; hỏi bổ sung và xác nhận trước khi tạo ticket.
- **Luồng:** đọc yêu cầu mới nhất và ngữ cảnh → xác định intent và đầu vào → hỏi nếu thiếu/mơ hồ → gọi đủ công cụ cần thiết → dùng dữ liệu trả về làm bằng chứng. Ticket cần xác nhận payload hiện tại; hủy yêu cầu thì dừng.
- Giữ nguyên công cụ, dữ liệu Helpdesk và bộ `data/eval_base.json`: 30 cases phase B, gồm 20 single-turn và 10 multi-turn. Không sửa expected hoặc loại cases sau khi đo.
- **Provider/model cố định:** `openai` / `gpt-4o-mini`; temperature=0.0 theo runner.
- Commit chứa phần chốt này là commit freeze trước v0; mã commit và SHA-256 sẽ được bổ sung sau khi commit.
- Mỗi vòng chỉ sửa một phần chính sau khi đọc run trước. Chỉ dùng run có provider_error_cases=0 và measured_cases=total_cases.

## 2. Kết quả

Đang thực hiện; chưa có điểm được công bố.

## 3. Phạm vi

Báo cáo này đáp ứng pha chốt bài toán và so sánh bốn phiên bản trên bộ base. Không tuyên bố đã làm bộ adversarial, 10 case tự viết, UI demo, mở rộng, reflection cá nhân hoặc nộp repository.
