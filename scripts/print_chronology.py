import os, email, email.policy, email.utils
from collections import defaultdict

source_dir = "source"
by_date = defaultdict(list)

for root, dirs, files in os.walk(source_dir):
    for f in files:
        if f.endswith((".zip", ".rar", ".pdf")):
            continue
        path = os.path.join(root, f)
        if os.path.getsize(path) == 0:
            continue
        with open(path, "rb") as fp:
            msg = email.message_from_binary_file(fp, policy=email.policy.default)
        dt = None
        date_str = msg.get("date", "")
        if date_str:
            try:
                dt = email.utils.parsedate_to_datetime(date_str)
            except:
                pass
        if not dt:
            for r in msg.get_all("received", []):
                parts = r.split(";")
                if len(parts) > 1:
                    try:
                        dt = email.utils.parsedate_to_datetime(parts[-1].strip())
                        break
                    except:
                        pass
        d_key = dt.strftime("%Y-%m-%d") if dt else "UNKNOWN"
        by_date[d_key].append({
            "subject": str(msg.get("subject", "")).strip(),
            "sender": str(msg.get("from", "")).strip(),
            "date": dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""
        })

for d in ["2026-11-21", "2026-11-22", "2026-11-23", "2026-11-24", "2026-11-25"]:
    print(f"\n=== {d} ({len(by_date[d])} emails) ===")
    seen = set()
    for m in sorted(by_date[d], key=lambda x: x["date"]):
        subj = m["subject"]
        if subj not in seen:
            seen.add(subj)
            snd = m["sender"][:30]
            dt_s = m["date"]
            print(f"  * {dt_s} | {snd:<30} | {subj[:70]}")
