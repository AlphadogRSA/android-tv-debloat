# FLauncher setup and recovery

FLauncher provides an ad-free app grid. Get it from the [official project](https://gitlab.com/flauncher/flauncher) or its linked Google Play listing. The reference setup used 0.18.0. This toolkit intentionally does not download or install APKs for you.

1. Install official FLauncher and open it. Confirm it displays your apps and can open Android settings.
2. Preview this toolkit's `--flauncher` option. It expects both `com.google.android.tvlauncher` and `com.google.android.tungsten.setupwraith`, and the FLauncher HOME activity.
3. Apply the reviewed plan. It disables the stock launcher and setup fallback without uninstalling them or modifying your button mappings. It checks that HOME resolves to `me.efesser.flauncher/.MainActivity`.
4. Let the command finish its save delay, then reboot manually and verify again.

The [official FLauncher instructions](https://gitlab.com/flauncher/flauncher/-/blob/master/README.md) explain that the setup fallback can re-enable Google's launcher. Their examples target Chromecast, so package names vary by device. Our reference Xiaomi uses `com.google.android.tvlauncher`, not the Google TV `launcherx` package.

Earlier manual trials rebooted immediately and the original launcher returned. A later trial disabled both packages, allowed 20 seconds for state to save, and verified FLauncher after boot. This does not isolate which factor caused persistence, and is not proof every firmware will behave identically.

If HOME fails and ADB is still authorized, restore the printed journal. Emergency recovery for this **known launcher pair**:

```sh
adb -s TV_IP:5555 shell pm enable --user 0 com.google.android.tvlauncher
adb -s TV_IP:5555 shell pm enable --user 0 com.google.android.tungsten.setupwraith
adb -s TV_IP:5555 shell am start -n com.google.android.tvlauncher/.MainActivity
```

Emergency commands enable the packages; journal restore preserves their original enabled state more precisely. Do not disable a launcher before testing the replacement. Some dedicated remote buttons may behave differently. Existing Buttons Remapper mappings are never modified by this toolkit.
