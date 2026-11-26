import os
import email
import email.policy
import re
from datetime import datetime

source_dir = "source"
current_date = "2026-11-26"

deadline_keywords = [
    r"deadline", r"due date", r"positively by", r"by \d{1,2}[./-]\d{1,2}[./-]\d{2,4}",
    r"on or before", r"last date", r"urgent", r"immediately", r"target date", r"scheduled on",
    r"meeting on", r"submission by", r"latest by", r"cut[- ]off"
]

results = []

for root, dirs, files in os.walk(source_dir):
    for f in files:
        if f.endswith((".zip", ".rar", ".pdf")): continue
        path = os.path.join(root, f)
        if os.path.getsize(path) == 0: continue
        try:
            with open(path, "rb") as fp:
                msg = email.message_from_binary_file(fp, policy=email.policy.default)
            subj = str(msg.get("subject", "")).strip()
            sender = str(msg.get("from", "")).strip()
            date_hdr = str(msg.get("date", "")).strip()
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    if ctype == "text/plain":
                        try:
                            body += part.get_content()
                        except: pass
                    elif ctype == "text/html" and not body:
                        try:
                            b_html = part.get_content()
                            body += re.sub('<[^<]+?>', ' ', b_html)
                        except: pass
            else:
                try:
                    b_raw = msg.get_content()
                    body = re.sub('<[^<]+?>', ' ', b_raw) if "<" in b_raw else b_raw
                except: pass
            
            full_text = subj + "\n" + body
            found_deadlines = []
            for kw in deadline_keywords:
                matches = re.findall(rf".{{0,60}}{kw}.{{0,60}}", full_text, flags=re.IGNORECASE)
                if matches:
                    found_deadlines.extend(matches)
            
            if found_deadlines:
                results.append({
                    "subject": subj,
                    "sender": sender,
                    "date": date_hdr,
                    "file": f,
                    "matches": list(set(found_deadlines))[:5],
                    "body_snippet": body[:500]
                })
        except Exception as e:
            pass

print(f"Total emails with potential deadline/urgency keywords: {len(results)}")
seen = set()
for r in results:
    if r["subject"] in seen: continue
    seen.add(r["subject"])
    print(f"\n==================================================")
    print(f"Subject: {r['subject']}")
    print(f"Sender:  {r['sender']}")
    print(f"Date:    {r['date']}")
    print("Keyword excerpts:")
    for m in r["matches"]:
        clean_m = " ".join(m.split())
        print(f"  -> {clean_m}")

