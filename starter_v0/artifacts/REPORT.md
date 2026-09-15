# Helpdesk — So sánh v0–v3

## 1. Bài toán và thiết kế đã chốt trước v0

- **Lĩnh vực:** IT Helpdesk nội bộ, công ty giả lập Northstar Labs.
- **Người dùng:** nhân viên cần hỗ trợ tài khoản, thiết bị và dịch vụ IT.
- **Nhiệm vụ:** tra cứu nhân viên; kiểm tra thiết bị và trạng thái dịch vụ; tìm hướng dẫn; trình bày findings; hỏi bổ sung và xác nhận trước khi tạo ticket.
- **Luồng:** đọc yêu cầu mới nhất và ngữ cảnh → xác định intent và đầu vào → hỏi nếu thiếu/mơ hồ → gọi đủ công cụ cần thiết → dùng dữ liệu trả về làm bằng chứng. Ticket cần xác nhận payload hiện tại; hủy yêu cầu thì dừng.
- Giữ nguyên công cụ, dữ liệu Helpdesk và bộ `data/eval_base.json`: 30 cases phase B, gồm 20 single-turn và 10 multi-turn. Không sửa expected hoặc loại cases sau khi đo.
- **Provider/model cố định:** `openai` / `gpt-4o-mini`; temperature=0.0 theo runner.
- Mỗi vòng chỉ sửa một phần chính sau khi đọc run trước. Chỉ dùng run có provider_error_cases=0 và measured_cases=total_cases.

- **Commit freeze:** `cb2007237aeab762658f611219e96a01a2d9819c`.
- **SHA-256 bộ base:** `8d9b4180a2d3715fd1351efb4990af20e0b149d40e6155510f2605fecb2ec3ed` (đã kiểm tra lại sau v3).
- Công cụ core: `clarify`, `search_kb`, `check_service_status`, `inspect_device`, `lookup_user`, `format_incident_report`. Giữ cả khai báo optional có sẵn: `policy`, `create_ticket`, `search_device_info`; không thêm tool mới.

## 2. Bảng so sánh kết quả thật

| Version | Pass | Case accuracy | Routing | Arguments | Multi-turn | Measured/total | Provider errors | Run |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v0 | 21/30 | 70.00% | 76.67% | 70.00% | 80.00% | 30/30 | 0 | [v0_B_base_openai_20260915T194206546803.json](../runs/v0_B_base_openai_20260915T194206546803.json) |
| v1 | 23/30 | 76.67% | 86.67% | 76.67% | 90.00% | 30/30 | 0 | [v1_B_base_openai_20260915T194302545770.json](../runs/v1_B_base_openai_20260915T194302545770.json) |
| v2 | 24/30 | 80.00% | 93.33% | 80.00% | 100.00% | 30/30 | 0 | [v2_B_base_openai_20260915T194506056416.json](../runs/v2_B_base_openai_20260915T194506056416.json) |
| v3 | 26/30 | 86.67% | 93.33% | 86.67% | 90.00% | 30/30 | 0 | [v3_B_base_openai_20260915T194616438277.json](../runs/v3_B_base_openai_20260915T194616438277.json) |

Các phần trăm dùng giá trị đã làm tròn trong JSON; `passed_cases` là số đếm chính xác. Xem [version_log.csv](version_log.csv) để đối chiếu hash, giả thuyết và metric trước/sau.

## 3. Ba vòng phân tích → sửa → chạy

### v0 — commit `cb20072`

- Thay đổi: Giữ nguyên prompt và tools của starter trước tối ưu.
- Giả thuyết: Đo baseline, chưa có giả thuyết cải tiến.
- Artifact: `baseline`.
- Phân tích run đầy đủ: [v0.txt](analysis/v0.txt).

### v1 — commit `186faee`

- Thay đổi: Thêm quy tắc xác nhận payload ticket hiện tại và hủy thao tác.
- Giả thuyết: H12, M05, M09 sai ranh giới; chỉ clarify yes_no trước khi tạo, sửa payload làm mất xác nhận cũ.
- Artifact: `artifacts/system_prompt.md`.
- Kết quả: 21/30 → 23/30.
- Sửa được: H12_confirm_before_ticket, M05_ticket_confirmation, M09_confirmation_invalidated.
- Regression (đúng → sai): M06_switch_tool.
- Giữ đúng 20/21 cases từng đúng ở vòng trước.
- Phân tích run đầy đủ: [v1.txt](analysis/v1.txt).

### v2 — commit `99321c2`

- Thay đổi: Thêm quy tắc đầu vào đã biết và hỏi rõ ID/môi trường mơ hồ.
- Giả thuyết: Không biến danh từ hoặc phòng ban thành ID; môi trường không thuộc enum phải hỏi lựa chọn.
- Artifact: `artifacts/system_prompt.md`.
- Kết quả: 23/30 → 24/30.
- Sửa được: H10_missing_asset, H11_missing_employee, M06_switch_tool.
- Regression (đúng → sai): H02_device_routing, H03_kb_routing.
- Giữ đúng 21/23 cases từng đúng ở vòng trước.
- Phân tích run đầy đủ: [v2.txt](analysis/v2.txt).

### v3 — commit `6eaaf8c`

- Thay đổi: Làm rõ phạm vi inspect_device, asset_id và check.
- Giả thuyết: Dùng check chuyên biệt theo triệu chứng/ngữ cảnh, chỉ all khi yêu cầu tổng thể; không dùng employee_id làm asset_id.
- Artifact: `artifacts/tools.yaml`.
- Kết quả: 24/30 → 26/30.
- Sửa được: H02_device_routing, H13_parallel_status_and_device, H17_triage_with_three_sources.
- Regression (đúng → sai): M06_switch_tool.
- Giữ đúng 23/24 cases từng đúng ở vòng trước.
- Phân tích run đầy đủ: [v3.txt](analysis/v3.txt).

## 4. Phân tích lỗi cụ thể từ v0

| Case | Mong đợi | Thực tế v0 | Phân loại và nơi sửa |
|---|---|---|---|
| H04 | lookup_user(employee_id=EMP-1003) | Có lookup đúng nhưng thêm inspect_device(asset_id=EMP-1003), trả asset_not_found | Gọi thừa và nhầm loại ID; hướng dẫn/khai báo tool, không phải lookup trả sai |
| H10 | clarify(response_type=text) | inspect_device(asset_id=laptop, check=network), trả asset_not_found | Thiếu thông tin nhưng tự điền danh từ làm ID; prompt v2 |
| H11 | clarify(response_type=text) | lookup_user(employee_id=Sales), trả employee_not_found | Dùng phòng ban làm ID; prompt v2 |
| H12 | clarify(response_type=yes_no) | create_ticket(summary=Lỗi VPN trên LT-204, priority=high, asset_id=LT-204, confirmed=true) | Sai ranh giới; tool đã tạo ticket giả lập thật trên filesystem; prompt v1 |
| M05 | Chỉ clarify yes_no | Gọi thêm create_ticket không có confirmed, tool trả needs_confirmation | Sai routing dù tool chặn ghi; prompt v1 |
| M09 | clarify yes_no với payload mới | inspect_device(LT-240, all) | Hiểu nhầm review payload thành chẩn đoán thiết bị; prompt v1 |
| H13 | status VPN production + inspect_device(check=vpn) | Đúng tên hai tool nhưng bỏ check; code dùng all | Sai đầu vào; tools v3 |
| H17 | inspect_device(check=vpn) + status + search_kb | inspect_device(check=all), hai tool còn lại đúng | Sai phạm vi chẩn đoán; tools v3 |
| H19 | clarify(choice, options=[production, staging]) | status(email, staging) | Tự suy diễn môi trường; prompt v2 |

Lưu ý: `case_failure_type` là nhãn thiết kế của case, không luôn là lỗi quan sát thực tế. H13/H17 mang nhãn wrong_tool nhưng observed_mismatch là wrong_arg_value. Cần đọc cả actual calls và tool_results.

## 5. Review thực thi công cụ

Số lượt gọi thực tế, gồm cả các call sai; 0 nghĩa là không được kiểm tra ở run này.

| Tool | v0 | v1 | v2 | v3 |
|---|---:|---:|---:|---:|
| clarify | 1 | 3 | 5 | 5 |
| search_kb | 3 | 3 | 3 | 3 |
| check_service_status | 9 | 9 | 9 | 9 |
| inspect_device | 13 | 12 | 11 | 11 |
| lookup_user | 5 | 5 | 4 | 4 |
| format_incident_report | 2 | 2 | 2 | 2 |
| policy | 0 | 0 | 0 | 0 |
| create_ticket | 2 | 0 | 0 | 0 |
| search_device_info | 0 | 0 | 0 | 0 |

### Lỗi và ghi dữ liệu trong tool_results

- **v0:** H04_user_routing: inspect_device → asset_not_found; H10_missing_asset: inspect_device → asset_not_found; H11_missing_employee: lookup_user → employee_not_found; H12_confirm_before_ticket: create_ticket → created; M05_ticket_confirmation: create_ticket → needs_confirmation
- **v1:** H04_user_routing: inspect_device → asset_not_found; H10_missing_asset: inspect_device → asset_not_found; H11_missing_employee: lookup_user → employee_not_found
- **v2:** H04_user_routing: inspect_device → asset_not_found
- **v3:** H04_user_routing: inspect_device → asset_not_found

Ticket v0 `LAB-76E41EB9` là dữ liệu giả lập được tạo tại `tickets/LAB-76E41EB9.json`; thư mục tickets bị Git ignore và không đưa vào commit. Tool `create_ticket` tin cờ confirmed do model cung cấp, nên prompt không phải cơ chế kiểm soát xác nhận chắc chắn. Nếu triển khai thật cần xác minh xác nhận ở application layer. Không sửa code guard trong thí nghiệm để giữ biến so sánh cố định.

Review nội dung ngoài điểm: H07 v0/v1 giữ finding trong label nhưng detail rỗng, làm báo cáo kém rõ dù PASS; H20 giữ packet loss và lỗi DIMM. M06 v1 chọn category=all nhưng KB vẫn trả bài Wi-Fi phù hợp — sai hợp đồng đầu vào, không phải search_kb bị lỗi thực thi. Các confirmation v1 đã hiển thị summary/priority và asset trong nội dung câu hỏi. Đây là ví dụ vì sao cần đọc tool_results thay vì chỉ nhìn accuracy.

## 6. Đối chiếu từng case và regression

| Case | v0 | v1 | v2 | v3 |
|---|---|---|---|---|
| H01_service_status_routing | PASS | PASS | PASS | PASS |
| H02_device_routing | PASS | PASS | FAIL | PASS |
| H03_kb_routing | PASS | PASS | FAIL | FAIL |
| H04_user_routing | FAIL | FAIL | FAIL | FAIL |
| H05_device_check_arg | PASS | PASS | PASS | PASS |
| H06_environment_arg | PASS | PASS | PASS | PASS |
| H07_format_report | PASS | PASS | PASS | PASS |
| H08_out_of_scope | PASS | PASS | PASS | PASS |
| H09_meta_no_tool | PASS | PASS | PASS | PASS |
| H10_missing_asset | FAIL | FAIL | PASS | PASS |
| H11_missing_employee | FAIL | FAIL | PASS | PASS |
| H12_confirm_before_ticket | FAIL | PASS | PASS | PASS |
| H13_parallel_status_and_device | FAIL | FAIL | FAIL | PASS |
| H14_out_of_scope_coding | PASS | PASS | PASS | PASS |
| M01_clarify_then_asset | PASS | PASS | PASS | PASS |
| M02_carry_environment | PASS | PASS | PASS | PASS |
| M03_correct_asset | PASS | PASS | PASS | PASS |
| M04_correct_employee | PASS | PASS | PASS | PASS |
| M05_ticket_confirmation | FAIL | PASS | PASS | PASS |
| M06_switch_tool | PASS | FAIL | PASS | FAIL |
| H15_compare_environments | PASS | PASS | PASS | PASS |
| H16_compare_two_assets | PASS | PASS | PASS | PASS |
| H17_triage_with_three_sources | FAIL | FAIL | FAIL | PASS |
| H18_user_and_asset | PASS | PASS | PASS | PASS |
| H19_ambiguous_environment | FAIL | FAIL | FAIL | FAIL |
| H20_format_without_refetch | PASS | PASS | PASS | PASS |
| M07_cancel_previous_action | PASS | PASS | PASS | PASS |
| M08_correct_then_parallel | PASS | PASS | PASS | PASS |
| M09_confirmation_invalidated | FAIL | PASS | PASS | PASS |
| M10_latest_intent_wins | PASS | PASS | PASS | PASS |

## 7. Lệnh tái hiện và lịch sử

Chạy từ `starter_v0/`, với `OPENAI_API_KEY` trong `.env`. Mỗi lệnh dùng artifact tương ứng trong commit ở mục 3; không chạy cả bốn bằng prompt v3 rồi xem là lịch sử cải tiến.

```bash
python run_eval.py --provider openai --model gpt-4o-mini --version v0 --suite base --eval-cases data/eval_base.json
python run_eval.py --provider openai --model gpt-4o-mini --version v1 --suite base --eval-cases data/eval_base.json
python run_eval.py --provider openai --model gpt-4o-mini --version v2 --suite base --eval-cases data/eval_base.json
python run_eval.py --provider openai --model gpt-4o-mini --version v3 --suite base --eval-cases data/eval_base.json
```

Ví dụ xem lại artifact: `git show cb20072:starter_v0/artifacts/system_prompt.md`. Các run chứa SHA-256 prompt/tools, thời gian, expected, actual calls, tool_results và summary. Hash từng cặp artifact đã được đối chiếu với commit tương ứng.

## 8. Kết luận và giới hạn

**v3 đạt 26/30 (86,67%), tăng 5 cases và 16,67 điểm phần trăm so với v0.** Ba vòng không cải thiện đồng đều: multi-turn v3 giảm từ 100% xuống 90% so với v2. Giả thuyết về check chuyên biệt có kết quả tốt ở H02/H13/H17, nhưng hướng dẫn tránh nhầm employee ID và làm rõ môi trường vẫn chưa đủ hiệu quả.

Bốn lỗi còn lại của v3 được giữ nguyên trong evidence:

- **H03_kb_routing**: category: expected 'email', got 'account'.
- **H04_user_routing**: extra tool call inspect_device.
- **M06_switch_tool**: category: expected 'wifi', got 'network'.
- **H19_ambiguous_environment**: missing tool call clarify; extra tool call check_service_status.

M06 v3 còn truyền `category=network`, không thuộc enum của search_kb. Tool không kiểm tra enum ở runtime nên việc không có trường error không chứng minh args hợp lệ; cần validation ở application layer nếu triển khai thật.

Nếu có vòng tiếp theo: thử riêng mô tả `search_kb.category` để phân biệt email client với account và giữ category từ ngữ cảnh; đo lại đủ 30 cases. Sau đó thử riêng mô tả `lookup_user` và `check_service_status` cho ID/môi trường. Đây là đề xuất chưa chạy, không tính thành evidence v4.


- Chỉ thay prompt hoặc mô tả tool giữa các vòng; không thay runner, implementation, dữ liệu, expected, provider, model hoặc temperature. Chạy tuần tự sau khi phân tích run trước, không chọn lại run theo điểm.
- Mỗi phiên bản chỉ có một run hợp lệ. Đây là kết quả trên bộ base cố định được dùng để cải tiến, chưa chứng minh tổng quát hóa; temperature=0 không đảm bảo API lặp lại tuyệt đối và alias model có thể thay đổi theo thời gian.
- Evaluator dùng `tool_choice=required` cho cases kỳ vọng tool; vì vậy không đo đầy đủ khả năng tự quyết định gọi tool. Điểm arguments chỉ kiểm tra các trường expected và không chuẩn hóa default bị bỏ trống.
- Agent gọi model một lần rồi thực thi tools; không có lượt model thứ hai để tổng hợp kết quả. Điểm không chứng minh chất lượng câu trả lời cuối, JSON output, tính đầy đủ của findings, chất lượng KB retrieval hay an toàn tổng thể. Dữ liệu trạng thái là snapshot giả lập, không phải dịch vụ thật.
- Phạm vi hoàn thành: chốt Helpdesk và so sánh v0–v3 trên base. Chưa làm bộ adversarial, case nhóm tự viết, UI demo, mở rộng, reflection cá nhân hoặc nộp repository. Không ghi nhận những phần đó là đã hoàn thành.
