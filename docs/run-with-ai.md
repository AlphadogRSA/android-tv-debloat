# How to debloat Android TV with Claude Code or ChatGPT/Codex

This guide runs an AI assistant on the computer connected to your TV's local network. The assistant reads this repo, inspects your device, proposes a plan, and uses a journal to make selected changes reversible. The automated profile currently targets Xiaomi, not every Android TV or Google TV brand.

## 1. Prepare the computer and TV

Install [Python 3.10+](https://www.python.org/downloads/), [Git](https://git-scm.com/downloads), and [official Google Platform Tools](https://developer.android.com/tools/releases/platform-tools). Follow their installation instructions for your OS. Check:

```sh
python --version
git --version
adb version
```

Some systems use `python3` instead of `python`. If ADB is not on PATH, the CLI accepts `--adb` followed by its full path before `--device`. Do not disable your computer's security controls or install random “ADB fixes.”

On the TV, open Settings → About and select the Android build entry seven times to enable developer options. Menu names vary by manufacturer. Enable the available USB/ADB or wireless debugging option. Put both devices on the same trusted network and note the TV's IP address.

For an older TV with network ADB on port 5555:

```sh
adb connect TV_IP:5555
adb devices -l
```

Approve the computer's debugging fingerprint on the TV. The target should show `device`, not `unauthorized` or `offline`.

For devices with pairing-based wireless debugging, follow the TV's pairing screen:

```sh
adb pair TV_IP:PAIRING_PORT
adb connect TV_IP:DEBUG_PORT
adb devices -l
```

Enter the pairing code interactively when ADB asks. The two ports may differ and may change. If wireless debugging is unavailable, do not assume an internet-exposed port or enable router forwarding. ADB needs no access from outside your LAN.

## 2. Download and review the repository

```sh
git clone https://github.com/AlphadogRSA/android-tv-debloat.git
cd android-tv-debloat
python -m unittest discover -s tests -v
```

Read the compatibility table and base removal list in README.md. Tests simulate ADB; running them does not debloat the TV.

## 3A. Run with Claude Code

1. Install Claude Code using the [official quickstart](https://code.claude.com/docs/en/quickstart), following your operating system's instructions.
2. From the repository directory, run `claude` and sign in using a supported account.
3. Review tool permissions rather than using a blanket bypass flag. The agent needs access to this folder, the official ADB executable, and your TV's LAN target.
4. Paste [prompts/debloat-my-tv.md](../prompts/debloat-my-tv.md), replacing the target and preferences.
5. Claude Code reads [CLAUDE.md](../CLAUDE.md), which imports the shared AGENTS.md workflow. Ask it to state the detected manufacturer/model and plan before apply.
6. Approve only the reviewed changes. Keep the restore-journal path.

Claude Code's [project-memory documentation](https://code.claude.com/docs/en/memory) explains CLAUDE.md imports. A repository link alone does not grant Claude access to local hardware.

## 3B. Run with ChatGPT using local Codex

1. Install Codex using the [official Codex CLI guide](https://learn.chatgpt.com/docs/cli), or use the local Codex desktop app.
2. For CLI use, run `codex` from the cloned repository and follow its sign-in prompts, including Sign in with ChatGPT when available for your account. For the desktop app, open the local repository folder as your project.
3. Paste [prompts/debloat-my-tv.md](../prompts/debloat-my-tv.md). Provide the ADB target, not your streaming passwords or Wi-Fi credentials.
4. Codex loads [AGENTS.md](../AGENTS.md) as project instructions. See the [official AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
5. Allow the local file, command, and LAN operations needed for the reviewed task. A cloud-only task usually cannot reach a private home LAN; run the device workflow locally.
6. Review the plan and lost features before approving apply. Keep the journal and test playback afterward.

No OpenAI API integration or API key is required by this repository. Your assistant's own account, plan, and execution features are separate from the CLI, which can also run without AI.

## 3C. Use ordinary ChatGPT or Claude web chat

If your chat has no authorized local execution tool, use it as a guide:

1. Send the public repository URL and ask it to read README.md and AGENTS.md. If it cannot open the URL, supply those files.
2. Run `inspect` yourself in a local terminal.
3. Redact serials, addresses, account names, and personal app inventories before sharing output.
4. Ask for a plan and explanation. Run reviewed commands yourself.
5. Share relevant redacted errors if anything fails. Never accept a claim that a web chat changed your TV without actual local tool evidence.

## 4. Choose what to keep

Ask the agent to explain each stock app in the base removal plan. Keep any media app you still use. The current CLI has no per-package keep flag; a user who wants to retain a base target needs a separately reviewed profile adjustment, not the unmodified apply command.

Casting and Assistant are optional. Disabling them stops those services, not just their icons. PatchWall can contain input-source controls. FLauncher requires installation and a working HOME activity before stock launcher changes. DNS filtering does not remove every ad and can affect services when a resolver is unavailable.

## 5. Preview, apply, verify, and restore

```sh
python tvdebloat.py --device TV_IP:PORT inspect
python tvdebloat.py --device TV_IP:PORT plan
```

The full reference profile is an **example to review**, not an instruction to remove every optional feature:

```sh
python tvdebloat.py --device TV_IP:PORT plan --patchwall --disable-casting --disable-voice --animations-off --adguard-dns --flauncher
```

After approval, use `apply` with the same flags and `--confirm`. Do not reboot until the command's save delay finishes. Keep the resulting `state/*.json` private.

After a user-approved reboot, check HOME and package states, ordinary internet access, important remote buttons, and real playback. Do not claim “faster” from a single free-RAM number. Restore a failed batch using:

```sh
python tvdebloat.py --device TV_IP:PORT restore state/YOUR_JOURNAL.json --confirm
```

## 6. Apply black wallpaper and supported 60 fps preferences

Copy `assets/black-wallpaper.png` to Downloads and select it in FLauncher → Settings → Wallpaper → Custom. This manual change is not journaled. In SmartTube, choose Settings → Player → Video presets → 720p 60fps AVC if appropriate for your display and decoder. TizenTube has no separate universal “force 60 fps” setting in the reviewed source. Neither setting creates frames absent from the source video.

## If the assistant stops or loses context

Provide the repo folder, current device target, last command/error, and local journal path. Ask it to inspect before continuing. Never tell it to “ignore errors and uninstall everything.” Do not post the journal publicly; it contains hardware and app information.
