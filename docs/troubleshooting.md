# Troubleshooting

## Device offline or unauthorized

Wake the TV, verify its current local address, and accept the debugging prompt on the TV. Reconnect the exact target. Do not blindly run against another device. ADB access can disappear temporarily during boot.

## Partial apply

The script stops on the first failed or unverifiable change. It prints the restore-journal path before any mutation and saves prior state before each operation. Restore that journal to undo the attempted batch. A journal entry may describe a change that failed before taking effect; restore is intended to tolerate that case.

Do not apply more changes to hide a failure. Keep the error output and journal locally; redact identifiers before reporting an issue.

## App stopped working after debloat

Restore the last journal, then test again. Core services and third-party apps are excluded, but manufacturers can add dependencies that this one-device profile cannot predict. In particular, PatchWall can contain input controls.

## DNS filtering broke an app or internet access

Restore the journal. If only DNS needs emergency recovery, restore the original values recorded in that journal. `settings delete global private_dns_mode` and `settings delete global private_dns_specifier` remove explicit overrides, but are appropriate only if the previous values were absent; do not overwrite an existing custom DNS configuration blindly.

DNS blocking cannot remove every video ad. Passing a ping test for one site is not proof all streaming apps work. Test your own apps after each batch.

## TizenTube fails to load

The reference device showed two different symptoms: an unreachable script CDN and Google's unusual-traffic redirect on a VPN address. Record the exact message. A successful DNS lookup alone does not prove HTTPS access works. Do not clear account data or disable ad filtering without evidence. Changing VPN servers may help an address-related Google challenge, but changes network privacy/routing; decide that explicitly. The toolkit never changes VPN settings.

## Still laggy

Compare similar workloads after boot settles. Check storage, temperature, and memory pressure rather than treating all cached RAM as waste. Playing high-resolution/high-frame-rate video can increase decoding load. A 60 Hz panel does not create 60 fps video frames. Avoid forced GPU switches, background-process limits, and memory-clearing loops as generic fixes.
