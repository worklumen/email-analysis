# Email Analysis Project

An analytical project examining email communications and travel/service transaction records extracted from mailbox exports.

## Repository Overview

This repository contains automated analysis, extracted artifacts, and documentation generated from email communications stored in the [`source/`](file:///home/zenhome/Projects/email-analysis/source) directory.

### Structure

```
├── LICENSE                                # Project License
├── README.md                              # Repository overview and instructions
├── mails.md                               # Comprehensive analysis and breakdown of all emails
├── travel_summary.md                      # Consolidated travel and expenditure log
├── nic_services.md                        # NIC Government IT infrastructure & migration advisory summary
├── pdf_emails/                            # Rendered PDFs with email message + attachments
│   ├── 20261029_225623.pdf                # IRCTC Booking Confirmation
│   ├── 20261029_230026.pdf                # UIIC PA Insurance + Attached PDF Policy
│   ├── 20261029_234311.pdf                # IndiGo Email + Attached PDF Tax Invoice
│   ├── 20261030_194241.pdf                # NIC GovDrive Migration Notice
│   └── 20261031_092400.pdf                # IRCTC Ticket Cancellation Confirmation
└── source/                                # Source email archive and extracted messages
    ├── email458144603.zip                 # Original email bundle archive
    └── 1795020946849032300/               # Extracted .eml messages
        ├── Booking Confirmation on IRCTC...eml
        ├── Congratulations your PA Insurance...
        ├── TaxInvoice - DL1262710CK30612.eml
        ├── Important Message : GovDrive Migration...eml
        └── Cancel Ticket.eml
```

---

## Detailed Documentation

- **[mails.md](file:///home/zenhome/Projects/email-analysis/mails.md)**: Full metadata, textual breakdown, attachment details, financial audits, and chronological event sequence for every email in the dataset.
- **[travel_summary.md](file:///home/zenhome/Projects/email-analysis/travel_summary.md)**: Consolidated ledger of all travel bookings (IRCTC Rail and IndiGo Air), insurance coverage details, financial expenditure, and cancellation/refund reconciliation.
- **[nic_services.md](file:///home/zenhome/Projects/email-analysis/nic_services.md)**: National Informatics Centre (NIC) email and cloud storage transition guide (GovDrive decommission & WorkDrive rollout).

---

## Key Highlights & Findings

1. **Travel Bookings & Timeline**:
   - **IndiGo Flight 6E-826 (DEL → TRV)**: Booked on 25-Oct-2026 for Passenger Rukmangadan D (PNR `NBSZJZ`). Total cost: **₹13,889.00**.
   - **IRCTC Train 16320 TVCN Humsafar (SMVB → TVCN)**: 3rd AC reservation booked on 29-Oct-2026 for journey date 01-Nov-2026 (PNR `4447240224`). Total fare paid: **₹1,399.05**.
   - **United India Insurance (UIIC)**: Group travel policy issued for IRCTC PNR `4447240224` on 29-Oct-2026 for ₹0.45 premium. Policy No. `44472402240129102026`.
   - **Train Cancellation**: The IRCTC train booking was cancelled on 31-Oct-2026. Refund of **₹1,030.36** credited (Cancellation fee / non-refundable deduction: ₹368.69).

2. **Enterprise / Government IT Advisory**:
   - **NIC GovDrive Migration**: National Informatics Centre mandate decommissioning GovDrive by 31-Dec-2026 and migrating all active user files to WorkDrive starting 01-Nov-2026.

---

## Analysis Methodology & Scripting

The analysis was performed using native Python standard libraries (`zipfile`, `email`, `email.policy`) along with `pypdf` and `beautifulsoup4` to inspect raw MIME structures, parse embedded HTML tables, and extract PDF ticket attachments without altering original records.
