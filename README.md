# dns-blocklist

Blocklist DNS cá nhân, gộp từ nhiều nguồn thành **một file `hosts.txt`** dùng
chung cho RouterOS (`/ip dns adlist`) và AdGuard Home.

## Dùng ở đâu

- **MikroTik RB5009 (nhà)** và **hEX S RB760iGS (quê)** — `/ip dns adlist`
- **AdGuard Home trên minix (quê)** — có thể thêm cùng URL nếu muốn một nguồn duy nhất

```
https://raw.githubusercontent.com/tuanlongsav/dns-blocklist/main/hosts.txt
```

## Sửa danh sách

| File | Việc |
|---|---|
| `sources.txt` | các blocklist nguồn (hosts hoặc AdBlock đều được) |
| `custom.txt` | tên miền **tự chặn thêm** |
| `exclude.txt` | tên miền **luôn cho qua** — ghi domain gốc là tha luôn mọi tên con |

Sửa xong đẩy lên là GitHub Actions tự dựng lại `hosts.txt` và commit.
Không sửa tay `hosts.txt` — lần build sau sẽ ghi đè.

## Tự chạy lại

Actions chạy **mỗi tuần** (03:00 thứ Hai giờ VN), chạy tay được bằng
*Actions → build blocklist → Run workflow*. Dựng thử ở máy: `python3 build.py`.

Header của `hosts.txt` cố ý **không ghi ngày build**, nên khi các nguồn không đổi
thì file không đổi và không sinh commit rỗng hàng tuần.

## Giấy phép và ghi công

`hosts.txt` là **bản gộp dẫn xuất** từ 5 danh sách của người khác. Một trong số
đó (AdGuard DNS filter) phát hành theo **GPL-3.0**, nên toàn bộ kho này — kể cả
danh sách gộp — cũng theo **GPL-3.0** (`LICENSE`). Danh sách nguồn, tác giả và
nghĩa vụ ghi công của từng cái nằm ở [CREDITS.md](CREDITS.md); phần ghi công
cũng được nhúng ngay trong header của `hosts.txt`.

Muốn tránh ràng buộc GPL: bỏ `filter_1.txt` khỏi `sources.txt` (mất ~178k tên,
phần còn lại là MIT + CC BY + dữ liệu URLhaus).
