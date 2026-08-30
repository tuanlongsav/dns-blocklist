# Nguồn và giấy phép

`hosts.txt` trong kho này là **bản gộp dẫn xuất** từ các danh sách dưới đây.
Mỗi nguồn giữ nguyên giấy phép của nó; phần gộp phát hành theo **GPL-3.0**
(bắt buộc, vì có thành phần GPL-3.0 — xem `LICENSE`).

| Nguồn | Tác giả | Giấy phép |
|---|---|---|
| [AdGuard DNS filter](https://github.com/AdguardTeam/AdguardSDNSFilter) | AdGuard Team | **GPL-3.0** |
| [AdAway Default Blocklist](https://github.com/AdAway/adaway.github.io) | AdAway | **CC BY 3.0** |
| [StevenBlack/hosts](https://github.com/StevenBlack/hosts) | Steven Black | **MIT** |
| [Malicious URL Blocklist (URLhaus)](https://urlhaus.abuse.ch/) | abuse.ch | dữ liệu URLhaus, dùng lại có ghi nguồn |
| [hostsVN](https://github.com/bigdargon/hostsVN) | bigdargon | **MIT** |

## Ghi công bắt buộc

- **AdGuard DNS filter** © AdGuard Software Ltd. — phát hành theo GNU GPL v3.
  Bản gộp này là tác phẩm phái sinh nên cũng theo GPL v3; mã dựng (`build.py`)
  và toàn bộ kho đi kèm giấy phép đó.
- **AdAway Default Blocklist** © AdAway — CC Attribution 3.0
  (https://creativecommons.org/licenses/by/3.0/).
- **StevenBlack/hosts** © Steven Black — giấy phép MIT, giữ nguyên thông báo
  bản quyền của tác giả.
- **hostsVN** © bigdargon — giấy phép MIT.
- **URLhaus** © abuse.ch — dữ liệu tên miền độc hại, ghi nguồn theo yêu cầu của
  abuse.ch.

## Nếu muốn tránh ràng buộc GPL

Bỏ dòng `filter_1.txt` (AdGuard DNS filter) khỏi `sources.txt`. Khi đó bản gộp
chỉ còn MIT + CC BY + dữ liệu URLhaus, nhẹ ràng buộc hơn nhiều — đổi lại mất
khoảng 178k tên miền.
