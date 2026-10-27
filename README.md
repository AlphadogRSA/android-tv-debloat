# Android TV Debloat: Xiaomi ADB Toolkit for Claude & ChatGPT

[![Tests](https://github.com/AlphadogRSA/android-tv-debloat/actions/workflows/tests.yml/badge.svg)](https://github.com/AlphadogRSA/android-tv-debloat/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Debloat a Xiaomi Android TV without root using ADB, with optional Claude Code or ChatGPT/Codex assistance.** Preview preinstalled-app removals, keep personal apps, configure an ad-free FLauncher home screen, and restore changes from local journals. The included guide also explains how to inspect other Android TV and Google TV devices without applying the Xiaomi profile blindly.

Maintained by [AlphadogRSA](https://github.com/AlphadogRSA). Updated **27 October 2026**: added local AI-agent setup, copy-and-paste prompts, recovery instructions, and an explicit device-compatibility guide.

## Start here: how do I debloat Android TV with AI?

1. Install Python 3.10+, Git, and [Google Android Platform Tools](https://developer.android.com/tools/releases/platform-tools) on the computer beside your TV.
2. Enable developer options and debugging on the TV. Put the TV and computer on the same trusted LAN. Find the TV's local IP address in its network settings.
3. Clone this repository:

   ```sh
   git clone https://github.com/AlphadogRSA/android-tv-debloat.git
   cd android-tv-debloat
   ```

4. Connect ADB and approve the computer on the TV. Use the port actually shown by your device; 5555 is a common older-TV example:

   ```sh
   adb connect TV_IP:5555
   adb devices -l
   ```

   If your TV requires wireless pairing, use `adb pair TV_IP:PAIRING_PORT` first and enter the TV's pairing code interactively. Then connect to its separate debugging port. Never publish the pairing code.

5. Start **Claude Code** with `claude`, or **Codex signed in with ChatGPT** with `codex`, from this folder. You can also open this folder in the local Codex desktop app. These tools need local shell and LAN access; a normal web chat or cloud coding sandbox cannot automatically reach your TV.
6. Paste the [ready-to-use agent prompt](prompts/debloat-my-tv.md), replacing the device target and choosing your feature preferences. Claude reads [CLAUDE.md](CLAUDE.md); Codex reads [AGENTS.md](AGENTS.md). The prompt also tells other agents to read those instructions explicitly.
7. Let the agent inspect the TV and show the proposed changes. Review which stock apps and features you want to keep before approving apply.
8. Keep the printed restore journal locally, let the save delay finish, and test playback, remote buttons, and the Home screen after a manual reboot.

**Full walkthrough:** [Run with Claude Code, ChatGPT/Codex, or a normal web chat](docs/run-with-ai.md). **No AI needed:** use the CLI commands below.

### Which Android TV and Google TV devices are supported?

| Device | Current scope |
| --- | --- |
| Xiaomi MiTV-AESP0, Android 10 | Reference manual setup; CLI unit-tested with simulated ADB |
| Other Xiaomi Android TV models | Xiaomi profile available, but review package dependencies and keep journals; not live-tested here |
| Google TV, Chromecast, Sony, TCL, Hisense, Nvidia Shield, onn. | Read-only `inspect`; this CLI rejects automated Xiaomi plans on non-Xiaomi manufacturers |
| Samsung Tizen or LG webOS | Unsupported; these are not Android TV |

Google TV uses Android, but manufacturer packages and launcher identifiers differ. A search for “Google TV debloat” should not be treated as proof that a Xiaomi removal list is suitable for that device.

### Copy this short prompt into your local AI agent

```text
Use https://github.com/AlphadogRSA/android-tv-debloat to help debloat my TV.
Read AGENTS.md, README.md, docs/run-with-ai.md, and prompts/debloat-my-tv.md first.
Work on my local computer, inspect the authorized TV, and show a package-by-package
plan before changing it. Preserve my installed apps, accounts, Bluetooth remote,
updates, DRM and core Android/Google services. Ask which optional features I use.
Use the journaled CLI only on a matching Xiaomi device. On another Android TV or
Google TV, inspect and report compatibility; do not apply the Xiaomi profile.
Never root, reset, clear app data, alter my VPN, or promise all ads disappear.
If you have no local shell/LAN access, guide me through the commands instead.
```

A small, dependency-free ADB toolkit based on a real Xiaomi MiTV-AESP0 / Android 10 cleanup. It previews optional preinstalled-app removals, preserves third-party apps, records every change, and restores the previous package and settings states.

Inspired by [seun-novodev/android-tv-debloat-toolkit](https://github.com/seun-novodev/android-tv-debloat-toolkit). This is an independent CLI implementation, not an official Xiaomi product or a fork of the upstream GUI.

## What it does

- Removes selected optional **system apps from user 0**, retaining their data for restoration.
- Optionally disables casting and Google Assistant voice search.
- Optionally turns off window, transition, and animator animations.
- Optionally configures AdGuard's public encrypted DNS for domain-based ad/tracker filtering.
- Optionally disables Google's launcher **and its setup fallback**, after FLauncher is installed and tested.
- Writes a restore journal before each change and verifies each result.
- Requires an explicit device target. It never scans your network, auto-selects another TV, roots a device, or automatically reboots it.

The automated profile is Xiaomi-only. Matching package names are acted on only when Android identifies them as system apps. Core TV services, Play Store, Play Services, Bluetooth, firmware updates, accessibility, and third-party apps are not removal targets.

## Requirements

1. Python 3.10+ on Windows, macOS, or Linux. No pip packages required.
2. [Google's official Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools). Put `adb` on PATH, or supply `--adb /path/to/adb` before the command.
3. Enable developer options and debugging on your own TV. Connect the computer and TV to the same trusted network. Some devices use wireless pairing with a changing port rather than port 5555.
4. Connect and approve the computer on the TV:

```sh
adb connect TV_IP:5555
adb devices -l
```

Replace `TV_IP:5555` throughout with the exact authorized ADB target. Check that only the intended TV is targeted. No root is required.

## Preview before changing anything

```sh
python tvdebloat.py --device TV_IP:5555 inspect
python tvdebloat.py --device TV_IP:5555 plan
```

`inspect` includes a local hardware serial and app inventory. Do not publish its output or the `state/` directory: journals contain device identifiers and your installed-app list. `.gitignore` excludes `state/`.

The base plan includes stock Netflix/Prime Video/YouTube, legacy music/games, camera/gallery/printing, Xiaomi video/promotional apps, recommendations, and analytics/reporting packages **when installed as system apps**. Review the printed package list. Do not apply it if you want to keep those stock apps. Apps absent from user 0 are skipped and will not be reinstalled during restore.

## Reproduce the final low-RAM profile

Install and test FLauncher first using [the launcher guide](docs/launcher.md). Then preview all optional changes:

```sh
python tvdebloat.py --device TV_IP:5555 plan --patchwall --disable-casting --disable-voice --animations-off --adguard-dns --flauncher
```

Apply that same reviewed selection:

```sh
python tvdebloat.py --device TV_IP:5555 apply --patchwall --disable-casting --disable-voice --animations-off --adguard-dns --flauncher --confirm
```

You can omit **any optional flag**. To preserve casting and Assistant, omit `--disable-casting` and `--disable-voice`. For the base app cleanup only:

```sh
python tvdebloat.py --device TV_IP:5555 apply --confirm
```

PatchWall is optional because it contains Xiaomi input-source and TV controls on the reference device; removal may affect those features. Casting removal prevents phone-to-TV casting through Google's receiver; voice removal disables Assistant/Google voice search. External apps may provide their own independent casting features.

The command prints a unique local JSON restore-journal path and waits 20 seconds after changes to allow Android to save package restrictions. After it finishes successfully, you may reboot manually:

```sh
adb -s TV_IP:5555 reboot
```

The wait is a precaution, not a guarantee of persistence on every firmware. After boot, confirm your apps work and HOME still resolves correctly:

```sh
adb -s TV_IP:5555 shell cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME
```

## Restore

Use the exact journal printed by your run, on the same TV:

```sh
python tvdebloat.py --device TV_IP:5555 restore state/YOUR_JOURNAL.json --confirm
```

Restore reinstalls only the system packages that this run removed and restores their exact prior enabled state. It restores settings values or deletes overrides that did not previously exist. Hardware serial and model must match the journal. Restore is also available after a partially failed apply. Keep the journal; do not edit it or restore untrusted journals.

Run journals in reverse chronological order if undoing several runs. The script does not clear app data, so restoration preserves retained data where Android permits. A factory reset, firmware upgrade, or unrelated package change can affect recovery. The script does not replace a full device backup.

## Black wallpaper and app-specific settings

Select `assets/black-wallpaper.png` in FLauncher → Settings → Wallpaper → Custom. The wallpaper change is manual and is not part of the restore journal. Copy it to the TV first:

```sh
adb -s TV_IP:5555 push assets/black-wallpaper.png /sdcard/Download/black-wallpaper.png
```

SmartTube: Settings → Player → Video presets → **720p 60fps AVC** was the selected preset in the reference setup. This is a preference, not frame generation: lower-frame-rate videos remain lower-frame-rate. TizenTube exposes a preferred resolution, but we found no separate universal force-60fps setting. These app settings are manual and not automated by this CLI.

## Ad filtering and playback

`--adguard-dns` sends system DNS queries to [AdGuard's public DNS service](https://adguard-dns.io/en/public-dns.html), subject to that provider's policies. It can block many advertising/tracking domains, not every in-app ad or video ad. Some apps or VPNs use their own DNS. Verify both normal internet access and filtering after changing DNS. Strict private DNS can interrupt internet access if the provider is unreachable; restore the journal to undo it.

TizenTube was observed redirecting to Google's unusual-traffic page on a NordVPN address. That was separate from frame-rate preferences. This toolkit does not disconnect your VPN, solve Google challenges, or promise that unofficial clients will always load. See [troubleshooting](docs/troubleshooting.md).

## Evidence and limits

The **manual changes this project is based on** were exercised on one MiTV-AESP0 running Android 10, with roughly 1 GB usable RAM. The user reported smoother performance and working DStv and TizenTube after cleanup. These are observations, not benchmark results or compatibility guarantees. TizenTube later encountered an intermittent VPN-related Google block.

The new automation has unit tests with a fake ADB device; it has **not been reapplied to the live TV**. The repository does not claim proven support for every Xiaomi model. Disabling casting/Assistant reduces their background work, but RAM usage varies. Black wallpaper is cosmetic. No swap tuning, forced GPU rendering, aggressive background-process limits, or RAM-booster apps are used.

Factory APKs remain in protected firmware partitions. User-profile uninstall is different from deleting firmware files. A factory reset can restore preinstalled apps.

## Development

```sh
python -m unittest discover -s tests -v
python -m py_compile tvdebloat.py
```

No downloaded APKs, ADB binaries, personal package inventories, network addresses, or device journals are distributed in this repo. See [CONTRIBUTING.md](CONTRIBUTING.md) before adding device profiles.

MIT licensed. Third-party projects and downloaded apps retain their own licenses.

## Frequently asked questions about Android TV debloating

### Can I remove Android TV bloatware without root?

ADB can uninstall supported preinstalled packages from an Android user profile without root. Their factory APKs remain in firmware. This project uses user-0 uninstall with retained data and a restore journal; it does not modify system partitions.

### Can ChatGPT or Claude automatically connect to my TV from a GitHub link?

A repository link supplies instructions, not local network access. Use a local tool such as Claude Code or Codex with authorized shell/LAN access. A web-only assistant can explain commands and review output but cannot claim it changed your TV. [Step-by-step AI setup](docs/run-with-ai.md).

### Will debloating make a 1 GB RAM TV faster?

Removing unused background apps can reduce work on low-memory TVs. The reference user reported smoother navigation, but this project has no controlled speed benchmark. Free RAM varies with caches and workload. No percentage speedup is claimed.

### Will AdGuard DNS block YouTube ads?

DNS filtering blocks many ad/tracking domains, but cannot reliably remove ads that share delivery infrastructure with videos. No “block all ads” promise is made. The toolkit does not patch apps, intercept DRM, or modify streaming subscriptions.

### Does disabling animations enable 60 fps in every app?

No. Animation duration, display refresh rate, and a video's frame rate are separate. SmartTube can prefer a 60 fps stream when available; a 30 fps source remains 30 fps. TizenTube's preferred-resolution menu is not a universal forced-frame-rate switch.

### How do I undo Android TV debloating?

Run `restore` with the JSON journal printed by apply and `--confirm`, on the same device. Restore operations run in reverse order and verify the saved settings and package states. Keep journals private and restore multiple runs newest first.

### Will this preserve DStv and other streaming apps?

The toolkit excludes third-party packages and core Google/Android services. DStv playback worked in the reference manual setup. Firmware, app versions, DRM requirements, and package dependencies vary; test your own apps and restore the last batch if something breaks.

## Sources and project discovery

- [Original Android TV debloat toolkit](https://github.com/seun-novodev/android-tv-debloat-toolkit)
- [Android Debug Bridge documentation](https://developer.android.com/tools/adb)
- [Official FLauncher setup](https://gitlab.com/flauncher/flauncher)
- [Official Claude Code quickstart](https://code.claude.com/docs/en/quickstart)
- [Official Codex CLI guide](https://learn.chatgpt.com/docs/cli)
- [Agent-readable project index](llms.txt)

Documentation uses descriptive headings, direct answers, real compatibility limits, and original setup observations. Public availability does not guarantee Google indexing, a first-place ranking, or citations in any AI answer. No search-volume or ranking measurements are claimed. See [publication and discovery notes](docs/discoverability.md).
