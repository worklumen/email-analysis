#!/usr/bin/env python3
"""
Analyze daily email volume and metadata from extracted archives in source/.
Consolidates statistics on total received emails, unique emails, and daily breakdown.
"""
import os
import email
import email.policy
import email.utils
from collections import defaultdict

def main():
    source_dir = "extracts" if os.path.exists("extracts") and len(os.listdir("extracts")) > 1 else "source"
    data = []
    skipped = []

    for root, dirs, files in os.walk(source_dir):
        for f in files:
            if f.endswith((".zip", ".rar", ".pdf")):
                continue
            path = os.path.join(root, f)
            if os.path.getsize(path) == 0:
                skipped.append((path, "Empty/Corrupted file (0 bytes)"))
                continue
            try:
                with open(path, "rb") as fp:
                    msg = email.message_from_binary_file(fp, policy=email.policy.default)
                dt = None
                date_str = msg.get("date", "")
                if date_str:
                    try:
                        dt = email.utils.parsedate_to_datetime(date_str)
                    except Exception:
                        pass
                if not dt:
                    for r in msg.get_all("received", []):
                        parts = r.split(";")
                        if len(parts) > 1:
                            try:
                                dt = email.utils.parsedate_to_datetime(parts[-1].strip())
                                break
                            except Exception:
                                pass
                d_key = dt.strftime("%Y-%m-%d") if dt else "UNKNOWN"
                data.append({
                    "date": d_key,
                    "datetime": dt.isoformat() if dt else "UNKNOWN",
                    "msg_id": str(msg.get("message-id", "")).strip(),
                    "subject": str(msg.get("subject", "")).strip(),
                    "sender": str(msg.get("from", "")).strip(),
                    "folder": os.path.basename(root),
                    "file": f,
                    "path": path
                })
            except Exception as e:
                skipped.append((path, str(e)))

    by_date = defaultdict(list)
    for item in data:
        by_date[item["date"]].append(item)

    print("==================================================")
    print("        DAILY EMAIL VOLUME ANALYSIS REPORT        ")
    print("==================================================")
    print(f"Total parsed emails: {len(data)}")
    print(f"Total skipped/unparsed items: {len(skipped)}")
    print("--------------------------------------------------")
    print(f"{'Date':<12} | {'Total Files':<12} | {'Unique Msg-IDs':<15} | {'Unique Subjects':<15}")
    print("--------------------------------------------------")
    
    total_files = 0
    total_unique_ids = set()
    total_unique_subs = set()

    for d in sorted(by_date.keys()):
        items = by_date[d]
        u_ids = set(i["msg_id"] for i in items if i["msg_id"])
        u_subs = set(i["subject"] for i in items)
        total_files += len(items)
        total_unique_ids.update(u_ids)
        total_unique_subs.update(u_subs)
        print(f"{d:<12} | {len(items):<12} | {len(u_ids):<15} | {len(u_subs):<15}")

    print("--------------------------------------------------")
    print(f"{'TOTAL':<12} | {total_files:<12} | {len(total_unique_ids):<15} | {len(total_unique_subs):<15}")
    print("==================================================\n")

    for d in sorted(by_date.keys()):
        items = by_date[d]
        print(f"\n--- {d} (Total: {len(items)} emails) ---")
        seen_subj = set()
        for it in sorted(items, key=lambda x: x["datetime"]):
            flag = " " if it["subject"] not in seen_subj else "*"
            seen_subj.add(it["subject"])
            print(f"  {flag} [{it['datetime'][11:16] if len(it['datetime'])>16 else '     '}] {it['sender'][:30]:<30} | {it['subject'][:60]}")

if __name__ == "__main__":
    main()
