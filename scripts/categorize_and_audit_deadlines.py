import os
import email
import email.policy
import email.utils
import re
from datetime import datetime

source_dir = "source"
current_time = datetime(2026, 11, 26, 11, 37, 56)

# Categories
# 1. Projects, Mapping & Drone Operations
# 2. Network Infrastructure & Vendor SLAs
# 3. Finance, Procurement & Billing
# 4. HR, Establishment, Training & Governance
# 5. Security, Advisories & Routine Circulars

categories = {
    "Projects, Mapping & Drone Operations": [],
    "Network Infrastructure & Vendor SLAs": [],
    "Finance, Procurement & Billing": [],
    "HR, Establishment, Training & Governance": [],
    "Security, Advisories & Routine Circulars": []
}

def classify(subj, sender, body):
    s = (subj + " " + sender).lower()
    
    # 2. Network Infrastructure & SLAs
    if any(k in s for k in ["cors", "hexagon", "leica", "uptime report"]):
        return "Network Infrastructure & Vendor SLAs"
    
    # 1. Projects, Mapping & Drone
    if any(k in s for k in ["naksha", "ntdb", "drone", "trinity", "geoid", "gnss observation", 
                           "invrf", "political map", "dsm to dtm", "amrut", "svamitva", "aai.aero", 
                           "red/yellow zone", "nas box", "milestone"]):
        return "Projects, Mapping & Drone Operations"
    
    # 3. Finance, Procurement & Billing
    if any(k in s for k in ["bsnl", "telephone bill", "bill information", "deposit slip", 
                           "ntrp", "pfms", "bills passed", "insurance coverage quotation", 
                           "rd subscription invoice", "eosl extension", "stop deduction", "ad-hoc bonus"]):
        return "Finance, Procurement & Billing"
    
    # 4. HR, Establishment, Training & Governance
    if any(k in s for k in ["leave", "cl", "apar", "training", "course", "exam", "ups registration", 
                           "vc link", "pension", "confirmation of", "nil pendency", "tour programme", 
                           "appeal numbered", "handing over-taking over", "mou", "faculty lecture", 
                           "screening committee", "vacancy circulation", "relieving order", 
                           "talk series", "yashada", "materiality assessment"]):
        return "HR, Establishment, Training & Governance"
    
    # 5. Security, Advisories & Routine Circulars
    return "Security, Advisories & Routine Circulars"

emails = []
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
            date_str = str(msg.get("date", "")).strip()
            msg_id = str(msg.get("message-id", "")).strip()
            
            # extract body preview
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    if ctype == "text/plain":
                        try:
                            body += part.get_content()
                        except:
                            pass
            else:
                try:
                    body = msg.get_content()
                except:
                    pass
            
            cat = classify(subj, sender, body)
            categories[cat].append({
                "subject": subj,
                "sender": sender,
                "date_str": date_str,
                "msg_id": msg_id,
                "file": f,
                "path": path,
                "body": body
            })
        except Exception as e:
            pass

print("=== CATEGORY COUNT SUMMARY ===")
total = 0
for cat, items in categories.items():
    u_subs = len(set(i["subject"] for i in items))
    u_ids = len(set(i["msg_id"] for i in items if i["msg_id"]))
    total += len(items)
    print(f"* {cat}: {len(items)} files | {u_ids} unique msg-ids | {u_subs} unique subjects")
print(f"Total: {total}\n")

