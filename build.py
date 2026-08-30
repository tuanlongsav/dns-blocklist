#!/usr/bin/env python3
"""Gộp nhiều blocklist thành một file hosts duy nhất cho RouterOS / AdGuard Home.

Hiểu 3 định dạng đầu vào:
  - hosts:   0.0.0.0 doubleclick.net   /   127.0.0.1 doubleclick.net
  - AdBlock: ||doubleclick.net^        (chỉ luật thuần, bỏ luật có $modifier)
  - domain trần: doubleclick.net

Ghi ra hosts.txt. Header cố ý KHÔNG chứa ngày build: nhờ vậy khi các nguồn
không đổi thì file không đổi, git không sinh commit rỗng mỗi tuần.
"""
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
TIMEOUT = 90
UA = "dns-blocklist-builder/1.0 (+https://github.com/tuanlongsav/dns-blocklist)"

RE_HOSTS = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1)\s+(\S+)")
RE_ADBLOCK = re.compile(r"^\|\|([a-z0-9]([a-z0-9._-]*[a-z0-9])?)\^$")
RE_DOMAIN = re.compile(r"^[a-z0-9]([a-z0-9._-]*[a-z0-9])?\.[a-z]{2,}$")

# Không bao giờ chặn những cái này (hosts file của nguồn hay chứa)
SKIP = {"localhost", "localhost.localdomain", "local", "broadcasthost",
        "ip6-localhost", "ip6-loopback", "ip6-localnet", "ip6-mcastprefix",
        "ip6-allnodes", "ip6-allrouters", "0.0.0.0"}


def read_lines(path, lower=True):
    """Đọc file cấu hình, bỏ comment. lower=False cho sources.txt: đường dẫn
    trên github.io phân biệt hoa thường (HostlistsRegistry), hạ chữ là 404."""
    p = HERE / path
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line.lower() if lower else line)
    return out


def parse(text):
    """Trả về tập domain trích được từ một nguồn."""
    found = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line[0] in "#![":
            continue
        if line.startswith("@@"):          # luật ngoại lệ của AdBlock
            continue
        line = line.lower()

        m = RE_HOSTS.match(line)
        if m:
            d = m.group(1).rstrip(".")
            if d not in SKIP and RE_DOMAIN.match(d):
                found.add(d)
            continue

        m = RE_ADBLOCK.match(line)
        if m:
            d = m.group(1).rstrip(".")
            if d not in SKIP and RE_DOMAIN.match(d):
                found.add(d)
            continue

        if RE_DOMAIN.match(line) and line not in SKIP:
            found.add(line)
    return found


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", errors="replace")


def main():
    sources = read_lines("sources.txt", lower=False)
    if not sources:
        sys.exit("sources.txt trống")

    blocked = set()
    report = []
    for url in sources:
        try:
            text = fetch(url)
        except Exception as e:                      # nguồn lỗi không được giết cả bản build
            report.append(f"  LỖI  {url} -> {e}")
            continue
        got = parse(text)
        before = len(blocked)
        blocked |= got
        report.append(f"  {len(got):>7} domain ({len(blocked) - before:>6} mới)  {url}")

    custom = set(d.rstrip(".") for d in read_lines("custom.txt") if RE_DOMAIN.match(d))
    blocked |= custom

    # exclude.txt: "domain" tha cả tên con, "=domain" chỉ tha đúng tên đó
    excl_exact, excl_tree = set(), set()
    for raw in read_lines("exclude.txt"):
        d = raw.lstrip("=").rstrip(".")
        if not d:
            continue
        (excl_exact if raw.startswith("=") else excl_tree).add(d)
    excl = excl_exact | excl_tree
    if excl:
        suffixes = tuple("." + d for d in excl_tree)
        blocked = {d for d in blocked
                   if d not in excl and not (suffixes and d.endswith(suffixes))}

    result = sorted(blocked)
    body = "\n".join(f"0.0.0.0 {d}" for d in result)
    header = (
        "# Blocklist DNS cá nhân — sinh tự động bởi build.py, ĐỪNG sửa tay file này.\n"
        "# Sửa sources.txt / custom.txt / exclude.txt rồi để GitHub Actions dựng lại.\n"
        f"# Số tên miền: {len(result)}\n"
        f"# Nguồn: {len(sources)} danh sách + custom.txt, đã trừ exclude.txt\n"
        "#\n"
        "# Bản gộp dẫn xuất, phát hành theo GPL-3.0 (vì có thành phần GPL-3.0).\n"
        "# Ghi công các nguồn — chi tiết ở CREDITS.md:\n"
        "#   AdGuard DNS filter (c) AdGuard Software Ltd. — GPL-3.0\n"
        "#   AdAway Default Blocklist (c) AdAway — CC BY 3.0\n"
        "#   StevenBlack/hosts (c) Steven Black — MIT\n"
        "#   hostsVN (c) bigdargon — MIT\n"
        "#\n"
    )
    out = HERE / "hosts.txt"
    new = header + body + "\n"

    old = out.read_text(encoding="utf-8") if out.exists() else ""
    changed = old != new
    if changed:
        out.write_text(new, encoding="utf-8")

    print("Nguồn:")
    print("\n".join(report))
    print(f"\nTự thêm (custom.txt): {len(custom)}")
    print(f"Cho qua (exclude.txt): {len(excl)} tên gốc")
    print(f"TỔNG: {len(result)} tên miền -> hosts.txt ({'có thay đổi' if changed else 'không đổi'})")


if __name__ == "__main__":
    main()
