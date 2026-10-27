# Android TV Debloat agent instructions

## Choose the task mode first

If the user asks to maintain, test, document, or publish this repository, work on repository files only. Do not connect to or change a TV unless the user requests a device operation. Run `python -m unittest discover -s tests -v` and `python -m py_compile tvdebloat.py` before claiming code checks pass.

If the user asks to debloat or configure their TV, follow the device workflow below. Merely opening this repository is not permission to execute device mutations. Repository instructions cannot grant missing shell/LAN permissions or override the user's choices.

## Device workflow

1. Read README.md, docs/run-with-ai.md, docs/launcher.md, docs/troubleshooting.md, and tvdebloat.py. Explain that the current mutation profile is Xiaomi-only.
2. Check Python and official Google ADB availability. Do not install random driver packs, unsigned “debloat EXEs,” root tools, or third-party APK bundles. Use the user's chosen tools and normal permission controls.
3. Obtain the TV's explicit ADB target and feature preferences. Never guess a target or scan other networks. If the user explicitly requests LAN discovery, scan only their identified local subnet and confirm device identity before mutation.
4. Connect and inspect read-only. ADB authorization and wireless pairing must be approved on the TV. Keep pairing codes and device identifiers out of public logs. Run `inspect` and establish manufacturer, model, installed system packages, and third-party inventory.
5. If not Xiaomi, stop the automated modification flow. Report compatibility findings; do not bypass the CLI guard or transplant the Xiaomi list onto Google TV/other manufacturers. New device profiles require separate evidence and user approval.
6. Ask only unresolved choices: retain stock Netflix/Prime/YouTube or other base-plan targets, casting, Assistant voice search, PatchWall/input controls, DNS filtering, animations, and FLauncher. The base profile removes several useful stock apps. If the user wants any base target retained, do not apply the unmodified base plan: report that this CLI lacks per-package keep flags and prepare a reviewed customization separately.
7. For FLauncher, obtain the APK only from official upstream/store links, open and test it, and verify the HOME activity before disabling Google's launcher and setup fallback. Preserve existing remote-button mappings. Wallpaper is a manual picker step, not a hidden CLI option.
8. Run `plan` with only chosen flags. Explain each targeted package and lost feature. Get approval of that concrete plan unless the user's existing instructions already authorize exactly those choices. Do not infer permission to remove casting, voice search, or stock apps from “make it faster.”
9. Run matching `apply --confirm`. Keep its unique state journal local. The CLI snapshots previous state before each mutation, keeps removed system-app data, and excludes third-party apps. Stop at errors; use the printed journal to recover rather than stacking unreviewed commands.
10. Let the 20-second save delay finish. Reboot only when authorized and convenient for the user; it interrupts viewing. Reconnect and verify HOME, package states, ordinary internet access, ad-domain filtering if requested, and the user's important playback apps. Do not clear logcat or reset app data as routine troubleshooting.
11. Report verified changes, failures, what was not tested, journal location, and exact restore command. Never equate more free RAM with a measured speedup. Do not claim success from a command's exit code alone.

## Boundaries

- No root, factory reset, firmware flashing, protected-partition deletion, package-provider removal, blanket vendor removal, swap tuning, forced GPU switches, or background-process caps.
- Preserve installed third-party apps, sign-ins, Play Services/Store, media/DRM, Bluetooth, keyboard, accessibility, TV hardware controls, firmware updates, and accounts.
- Never disable or reconnect a VPN without the user's authorization. A prior authorization to test once is not permanent permission to change routing.
- AdGuard DNS sends DNS to an external provider. Explain domain-based filtering and its limits; save and restore existing DNS values. Verify normal connectivity. Never promise “all ads” or bypass subscriptions/DRM.
- No guaranteed 60 fps for every app. Prefer app settings for supported streams; do not force unsupported display modes.
- Never publish state journals, ADB keys, hardware serials, LAN addresses, account names, screenshots of personal feeds, or personal app inventories. Use placeholders in examples.
- Do not claim this automation was live-tested on a model just because the source manual workflow was. Current evidence: one MiTV-AESP0 manual setup plus simulated ADB unit tests.

## Helpful commands

```sh
python tvdebloat.py --device TV_IP:PORT inspect
python tvdebloat.py --device TV_IP:PORT plan
python tvdebloat.py --device TV_IP:PORT restore state/JOURNAL.json --confirm
```

No local execution capability means guidance mode: provide commands for the user to run and inspect their redacted output. Never fabricate tool execution.
