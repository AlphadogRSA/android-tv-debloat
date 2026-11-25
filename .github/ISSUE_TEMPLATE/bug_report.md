---
name: Bug report
about: Report a reproducible toolkit problem with redacted diagnostic details
title: ""
labels: ""
assignees: ""
---

## What happened?

Describe the problem, what you expected, and any affected TV features.

## Environment

- Toolkit commit or version:
- Computer operating system:
- Python version:
- ADB version:
- TV manufacturer and model:
- Android / Google TV version:

Include model names and software versions only. Do not include hardware serials,
LAN addresses, account names, or personal app inventories.

## Steps to reproduce

1.
2.
3.

Use `TV_IP:PORT` instead of your real device target in commands. Describe the
command and optional flags you already used; do not repeat an apply or restore
operation just to produce a report.

## Redacted error

Paste only the relevant error message below. Replace device targets, hardware
serials, account names, and personal package names with placeholders.

```text
PASTE_REDACTED_ERROR_HERE
```

Do not attach the `state/` directory, restore journals, ADB keys, pairing codes,
full inspect output, or screenshots containing personal information.

## Recovery and current state

- Did apply make any changes before the error?
- Was a restore journal created? Answer yes/no; do not upload it.
- If you already attempted restore, what happened?
- Which functions still work, and which are affected?

Keep the original journal locally. Do not edit it or restore an untrusted journal.

## Before submitting

- [ ] I checked README.md and docs/troubleshooting.md.
- [ ] I removed private identifiers and personal app inventories.
- [ ] I understand that automated Xiaomi plans are not supported on other manufacturers.
- [ ] I have distinguished a real-device result from a simulated test result.
