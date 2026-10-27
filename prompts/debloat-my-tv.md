# Prompt: debloat my Android TV with Claude Code or ChatGPT/Codex

Paste the following into an agent with local shell and LAN access. Replace placeholders; do not include Wi-Fi passwords, pairing codes, or streaming credentials. If you do not know a preference, leave it as “ask me.”

```text
Help me reproduce the low-RAM Xiaomi Android TV setup documented at:
https://github.com/AlphadogRSA/android-tv-debloat

Read AGENTS.md, README.md, docs/run-with-ai.md, docs/launcher.md,
docs/troubleshooting.md, and tvdebloat.py before acting. If the repo is not
local, clone it into a new folder without overwriting my files. First confirm
that you have local shell and LAN access. A web-only/cloud-only chat should
guide me through commands rather than pretend to access my TV.

My device:
- TV brand/model: ASK ME OR IDENTIFY THROUGH AUTHORIZED ADB
- ADB target: TV_IP:PORT
- Stock apps I want to KEEP: ASK ME
- Phone casting: ASK ME
- Google Assistant voice search: ASK ME
- PatchWall/Xiaomi input controls: ASK ME
- FLauncher ad-free home screen: YES, if compatible and tested first
- Solid-black FLauncher wallpaper: YES
- Disable menu animations: YES
- AdGuard DNS ad/tracker filtering: YES, after explaining provider/limitations
- VPN: KEEP CURRENT CONNECTION AND SETTINGS

Start with read-only inspection. Preserve all my installed third-party apps,
accounts, Bluetooth remote, DRM/media services, Play Store/Services,
accessibility, firmware updates, and core TV functions. Never root, flash,
factory-reset, clear app data, or blindly remove every Xiaomi package.

Use the existing Xiaomi CLI only on a matching manufacturer. For another
Android TV or Google TV, provide an inspection/compatibility report and do
not apply or bypass the Xiaomi profile. If I want to keep any stock app that
the base plan removes, explain that limitation and prepare a reviewed
customization rather than silently removing it.

Resolve only missing details. Show the package-by-package plan and feature
tradeoffs before applying it. After I approve that plan, run the same flags
with apply --confirm. Save the journal locally and tell me its path. Stop on
errors and restore when appropriate. Do not change the VPN to fix playback.

Install FLauncher only from official upstream/store sources, test it first,
and use the documented stock-launcher-plus-setup-fallback approach. Allow
Android time to save state. Apply the included black image using the Custom
wallpaper picker; don't invent an automatic wallpaper command.

When I authorize a restart, verify the default HOME activity after boot,
disabled/uninstalled package states, internet access, DNS filtering, and my
important streaming apps. Report what is proven and what needs my testing.
No guaranteed speedup, all-ad blocking, or forced 60 fps claims. Give me the
exact restore command and leave my personal information out of public files.
```

For the original reference choices, specify no retained stock media apps, disable casting and Assistant, opt into PatchWall removal with its input-control tradeoff, enable FLauncher, black wallpaper, animations off, and AdGuard DNS. These are preferences to choose deliberately, not defaults suitable for every household.
