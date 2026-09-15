# TEAM — Day04, K4-L3B

## Thông tin bài nộp

- Tên nhóm: Nhóm Bảo — **một thành viên**.
- Người đại diện / MSSV: **Đào Gia Bảo / 2A202602793**.
- GitHub: [kevindao94work](https://github.com/kevindao94work).
- Tên repo: `K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling`.
- URL nộp (trang gốc repo): https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling
- Nhánh nộp: `main`.
- Commit kỹ thuật UI/evidence: [`cc50309`](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/cc50309). Commit chốt sản phẩm/hồ sơ: [`c0a80650846446c4cc2d7217fa7ae023b7da210c`](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/c0a80650846446c4cc2d7217fa7ae023b7da210c). Các commit tiếp theo chỉ bổ sung audit và biên bản xác nhận nộp, không đổi kết quả các run.
- Deadline mặc định theo đề: 23:59 ngày học, Asia/Ho_Chi_Minh; không có bằng chứng về thông báo đổi hạn trong phiên làm việc này.

## Thành viên và phân công

| Họ tên | MSSV | GitHub | Vai trò và công việc | Evidence |
|---|---|---|---|---|
| Đào Gia Bảo | 2A202602793 | kevindao94work | Toàn bộ: chốt Helpdesk; thiết kế/đọc eval; prompt v0–v3; tools; safety; 10 case nhóm; runtime/UI; kiểm thử; transcripts; report; tích hợp Git; demo và nộp VLearn | [REPORT](starter_v0/artifacts/REPORT.md), [lịch sử main](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commits/main/) |

Không có thành viên thứ hai. Codex là công cụ hỗ trợ AI, không phải thành viên và không được dùng làm peer reviewer giả. Toàn bộ trách nhiệm được giao cho Bảo theo yêu cầu trực tiếp của Bảo; phân công không có nghĩa mọi dòng code đều được gõ thủ công không có AI.

## Nhận xét chung

- Base v0→v3: **21/30 → 23/30 → 24/30 → 26/30**; +5 cases, +16,67 điểm phần trăm. Bốn run đều measured=30, provider errors=0. [Version log](starter_v0/artifacts/version_log.csv).
- V1 bổ sung xác nhận payload, sửa 3 case ranh giới nhưng có regression M06; v2 xử lý thiếu ID nhưng chưa giải quyết hết môi trường mơ hồ; v3 mô tả inspect_device rõ hơn, sửa phạm vi check ở H02/H13/H17. [Before/after và từng case](starter_v0/artifacts/REPORT.md#3-ba-vòng-phân-tích--sửa--chạy).
- Safety **7/12**: 4 mock-ticket writes không được phép trong runner gốc; group **8/10**, gồm lỗi category và carry ID. [Phân tích thực thi](starter_v0/artifacts/analysis/safety_execution_audit.json).
- UI `chat-ui-v2` tách prepare_ticket khỏi write; cần nút xác nhận cho payload server hiện tại. Demos kiểm tra hủy, sửa payload, stale/replay 409 và tool errors. [Manifest](starter_v0/artifacts/analysis/ui_demo_manifest.json).
- Giới hạn: chỉ dữ liệu giả lập; chưa bonus/web-search live; prompt không thay thế guard; không dùng điểm v3 runner để khẳng định UI an toàn. Một người phụ trách toàn bộ, không có peer-check độc lập.

## INDIVIDUAL

### Đào Gia Bảo — 2A202602793

**Phạm vi đóng góp được giao:** toàn bộ dự án và hồ sơ nộp. Phần liệt kê dưới đây được Codex hỗ trợ biên soạn từ file/run/commit thật; không tự nhận là reflection được viết độc lập không có AI.

| Phần việc | File | Commit kỹ thuật |
|---|---|---|
| Chốt Helpdesk và 30 case base | [eval_base](starter_v0/data/eval_base.json), [REPORT](starter_v0/artifacts/REPORT.md) | [cb20072](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/cb20072) |
| Quy tắc xác nhận ticket v1 | [system_prompt](starter_v0/artifacts/system_prompt.md) | [186faee](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/186faee) |
| Làm rõ ID/môi trường v2 | system_prompt.md | [99321c2](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/99321c2) |
| Phạm vi chẩn đoán v3 | [tools.yaml](starter_v0/artifacts/tools.yaml) | [6eaaf8c](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/6eaaf8c) |
| 10 tình huống nhóm | [eval_group](starter_v0/data/eval_group.json) | [f703a98](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/f703a98) |
| Safety, UI, runtime, tests, transcripts | [chat_runtime](starter_v0/chat_runtime.py), [tests](starter_v0/tests/test_chat_runtime.py), [transcripts](starter_v0/transcripts) | [cc50309](https://github.com/kevindao94work/K4-L3-DAY04-Dao_Gia_Bao-2A202602793-PromptEngineeringToolCalling/commit/cc50309) |

- **Quyết định kỹ thuật và khó khăn quan sát được:** mô tả prompt chưa đủ ngăn forged/stale confirmation; thêm cơ chế draft + nút xác nhận phía server. Rehearsal đầu chỉ hỏi bằng text, nên thêm prepare_ticket cho UI và giữ cả evidence trước/sau. Không đổi eval expected để tăng điểm.
- **Bài học kỹ thuật từ evidence:** phân biệt sai routing, sai args và tool execution error; automatic PASS không chứng minh có dữ liệu trả về hoặc không có write; xác nhận phải gắn với payload hiện tại.
- **AI/công cụ:** Codex hỗ trợ code/case/report, OpenAI gpt-4o-mini chạy live, Git/GitHub lưu lịch sử, Safari/Computer Use quan sát UI. Kiểm chứng bằng hashes, run JSON, 10 unit tests, HTTP checks và live transcript, không bịa điểm hoặc hội thoại.
#### Reflection — bản có hỗ trợ AI theo yêu cầu của Bảo

Bài học đầu tiên từ dự án là một câu trả lời nghe hợp lý chưa đủ để đánh giá trợ lý. Cần mở run JSON để kiểm tra model đã chọn đúng công cụ, truyền đúng đầu vào và công cụ có thực hiện thành công hay không. Ví dụ, có case tra policy đạt điểm routing nhưng không tìm được dữ liệu; điều này cho thấy chỉ nhìn accuracy có thể bỏ sót vấn đề.

Khó khăn kỹ thuật rõ nhất là xử lý xác nhận tạo ticket. Prompt v1 đã cải thiện bộ base, nhưng bộ an toàn vẫn có trường hợp model làm theo xác nhận giả hoặc xác nhận cũ. Vì vậy, UI bổ sung bản nháp và nút xác nhận gắn với đúng payload ở server. Cách làm này giúp phân biệt phần hướng dẫn model với phần kiểm soát hành động trong code.

Điều cần giữ trong các bài tiếp theo là thay đổi từng phần, chạy lại cùng bộ kiểm tra và ghi cả regression. Điểm base tăng từ 21/30 lên 26/30 là kết quả có thể đối chiếu, nhưng bốn lỗi còn lại và điểm an toàn 7/12 cho thấy hệ thống vẫn có giới hạn. Hướng cải tiến tiếp theo là xử lý category/ID nhất quán hơn và kiểm tra thêm hội thoại mới, thay vì chỉnh đáp án để tạo điểm cao.

*Reflection được Codex hỗ trợ soạn theo yêu cầu của Bảo, dựa trên evidence của dự án; không khẳng định Bảo đã tự thao tác từng bước kiểm thử hoặc viết độc lập không có AI.*
- **Tự kiểm tra khởi động:** có log HTTP/Safari của Codex và transcript được bổ sung sau đó; chưa nhận xác nhận ai thực hiện các lượt bổ sung hoặc đã làm theo README.
- **Nộp VLearn:** chờ thao tác nộp và mở lại kiểm tra URL; sẽ cập nhật kết quả thực tế, không ghi thời điểm trước khi nộp.

## Kiểm tra lịch sử đóng góp

Các commit thí nghiệm cũ dùng Git identity cục bộ `Kevin Dao`; GitHub liên kết email cấu hình đó với `kevindao943`, trong khi repo và tài khoản đang đăng nhập là `kevindao94work`. Giữ nguyên lịch sử, không rewrite tác giả để tạo đóng góp giả. Bảo đã giao toàn bộ trách nhiệm dự án cho chính mình; AI assistance được khai báo phía trên. Commit công cụ audit cuối dùng tên Đào Gia Bảo và noreply email của tài khoản `kevindao94work` đã xác thực, có file kỹ thuật [verify_submission.py](starter_v0/scripts/verify_submission.py) và [kết quả audit](starter_v0/artifacts/analysis/final_submission_check.json).
