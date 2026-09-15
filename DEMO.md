# Demo Day04 — Đào Gia Bảo / 2A202602793

Nhóm một thành viên; Bảo trình bày toàn bộ. Khung demo chung theo đề: **20:25–21:00**. Kịch bản này được chuẩn bị từ evidence thật; không phải biên bản đã trình bày trước lớp.

## Kịch bản 5–7 phút

| Thời lượng | Nội dung cần mở | Điều cần giải thích |
|---|---|---|
| 0:00–0:45 | [REPORT: lĩnh vực](starter_v0/artifacts/REPORT.md) | Helpdesk nội bộ giả lập; cùng 30 case, OpenAI/gpt-4o-mini qua v0–v3 |
| 0:45–1:45 | [Fallback JSON](starter_v0/artifacts/demo_fallback.json), case H12 v0 | Mong đợi clarify yes_no; thực tế create_ticket confirmed=true và ghi mock ticket — đây là lỗi hành động thật |
| 1:45–2:45 | [Prompt diff v0→v1](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/compare/cb20072...186faee), H12 v1 | Thêm quy tắc xác nhận payload, chỉ clarify trước khi tạo; run mới sửa case này |
| 2:45–3:30 | [Bảng kết quả](starter_v0/artifacts/REPORT.md#2-bảng-so-sánh-kết-quả-thật) | 21→23→24→26/30, có regressions; 0 provider errors; không đổi bộ câu |
| 3:30–5:30 | UI + [D04](starter_v0/transcripts/c2c570842d7049dc8ea8cea6f06753ef.transcript.json) | Draft low → sửa high → xác nhận cũ vô hiệu → đúng payload mới mới được ghi; xem tool args/result |
| 5:30–6:30 | [D05](starter_v0/transcripts/01d08f1e70094efea6fc57a6d5d7d8b8.transcript.json) + [safety audit](starter_v0/artifacts/analysis/safety_execution_audit.json) | Tool error phải hiện; safety v3 chỉ 7/12, prompt chưa đủ; UI guard là lớp riêng, không gán điểm eval cũ cho UI |

## Mở UI

Từ repository, theo [README](README.md):

```bash
cd starter_v0
source .venv/bin/activate
python ui_server.py --port 8765
```

Mở http://127.0.0.1:8765. Nếu cổng đang được server dùng, mở trang sẵn có; không chạy thêm server cùng cổng.

1. Gửi `Soạn ticket summary Máy in không nhận lệnh, priority low, asset_id PR-404 để tôi xem trước.`
2. Gửi `Đổi priority thành high và summary thành Máy in chặn cả nhóm; giữ asset_id PR-404. Cho tôi xem payload mới trước khi tạo.`
3. Chỉ bấm Xác nhận sau khi đã kiểm tra payload. Tác vụ này tạo một ticket **giả lập cục bộ**; không thao tác hệ thống thật.
4. Hoặc chọn Hủy để demo không ghi dữ liệu.
5. Gửi `Kiểm tra tổng thể thiết bị giả lập LT-99999. Nếu không tìm thấy thì nói rõ lỗi.` để thấy asset_not_found.

## Fallback khi mất mạng/API lỗi

- [demo_fallback.json](starter_v0/artifacts/demo_fallback.json): trích nguyên case H12 v0/v1, summary 4 run và đường dẫn nguồn; không sửa điểm.
- [REPORT](starter_v0/artifacts/REPORT.md): phân tích trước/sau, group/an toàn, giới hạn.
- [D02 nhiều lượt](starter_v0/transcripts/26a6343c13124070b1b22122b6db1298.transcript.json), [D03 hủy](starter_v0/transcripts/5eae04927ec0477586bdcae7245a5394.transcript.json), D04/D05 ở trên.
- [Manifest HTTP](starter_v0/artifacts/analysis/ui_demo_manifest.json): 409 cho xác nhận cũ/replay, 200 tạo đúng một mock ticket.

Các file này mở offline bằng VS Code hoặc trình đọc JSON. Nói rõ đây là evidence đã chạy trước đó, không giả là live demo vừa chạy. Không mở .env trong lúc chia sẻ màn hình.
