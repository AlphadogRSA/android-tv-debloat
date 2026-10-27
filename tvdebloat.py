#!/usr/bin/env python3
"""Reversible, explicit Android TV changes using an already-authorized ADB device."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import time
from datetime import datetime, timezone

OPTIONAL_APPS = [
    'com.netflix.ninja', 'com.amazon.amazonvideo.livingroom',
    'com.google.android.youtube.tv', 'com.google.android.music',
    'com.google.android.youtube.tvmusic', 'com.google.android.play.games',
    'com.android.camera2', 'com.android.gallery3d', 'com.mitv.videoplayer',
    'com.mitv.tvhome.mitvplus', 'com.mitv.tvhome.michannel', 'com.xm.webcontent',
    'com.google.android.tvrecommendations', 'com.android.printspooler',
    'com.miui.tv.analytics', 'com.xiaomi.statistic',
    'com.google.android.feedback', 'com.google.android.tv.bugreportsender',
]
LAUNCHER = 'me.efesser.flauncher'
HOME = LAUNCHER + '/.MainActivity'
STOCK = ['com.google.android.tungsten.setupwraith', 'com.google.android.tvlauncher']
ANIMATIONS = ['window_animation_scale', 'transition_animation_scale', 'animator_duration_scale']


class Adb:
    def __init__(self, executable, device):
        self.executable, self.device = executable, device

    def run(self, *args):
        result = subprocess.run([self.executable, '-s', self.device, *args],
                                capture_output=True, text=True, timeout=90)
        output = (result.stdout + result.stderr).strip()
        if result.returncode or re.search(r'(^|\n)(Failure|Error|Security exception)', output):
            raise RuntimeError(output or f'ADB exited {result.returncode}')
        return output

    def shell(self, *args):
        return self.run('shell', *args)


def package_names(output):
    return {line.removeprefix('package:').strip() for line in output.splitlines()
            if line.startswith('package:')}


def inventory(adb):
    if adb.run('get-state').strip() != 'device':
        raise RuntimeError('Authorize this computer on the TV first.')
    manufacturer = adb.shell('getprop', 'ro.product.manufacturer').strip()
    return {
        'manufacturer': manufacturer,
        'model': adb.shell('getprop', 'ro.product.model').strip(),
        'android': adb.shell('getprop', 'ro.build.version.release').strip(),
        'serial': adb.shell('getprop', 'ro.serialno').strip(),
        'installed': sorted(package_names(adb.shell('pm', 'list', 'packages', '--user', '0'))),
        'system': sorted(package_names(adb.shell('pm', 'list', 'packages', '-s', '--user', '0'))),
        'third_party': sorted(package_names(adb.shell('pm', 'list', 'packages', '-3', '--user', '0'))),
    }


def build_plan(info, options):
    if 'xiaomi' not in info['manufacturer'].lower():
        raise ValueError('This profile is for Xiaomi TVs only; inspect is available for other devices.')
    installed, system = set(info['installed']), set(info['system'])
    packages = list(OPTIONAL_APPS)
    if options.patchwall:
        packages.append('com.mitv.tvhome.atv')
    operations = []
    for package in packages:
        # A matching package name is not enough: only touch manufacturer/system apps.
        if package in installed and package in system:
            operations.append({'kind': 'package', 'package': package, 'action': 'uninstall'})
    for flag, package in [(options.disable_casting, 'com.google.android.apps.mediashell'),
                          (options.disable_voice, 'com.google.android.katniss')]:
        if flag and package in installed and package in system:
            operations.append({'kind': 'package', 'package': package, 'action': 'disable'})
    if options.animations_off:
        operations.extend({'kind': 'setting', 'key': key, 'value': '0'} for key in ANIMATIONS)
    if options.adguard_dns:
        operations += [
            {'kind': 'setting', 'key': 'private_dns_specifier', 'value': 'dns.adguard-dns.com'},
            {'kind': 'setting', 'key': 'private_dns_mode', 'value': 'hostname'},
        ]
    if options.flauncher:
        if LAUNCHER not in installed:
            raise ValueError('Install and test official FLauncher first; see docs/launcher.md.')
        # Check this before altering either stock package.
        if not all(package in installed and package in system for package in STOCK):
            raise ValueError('Expected stock launcher/fallback pair not found. No launcher changes planned.')
        operations.extend({'kind': 'package', 'package': package, 'action': 'disable'} for package in STOCK)
        # Do not replace Android role/preference records: disabled stock packages let HOME resolve
        # to FLauncher, and restoring those packages retains the original preference records.
    return operations


def enabled_state(adb, package):
    dump = adb.shell('dumpsys', 'package', package)
    match = re.search(r'User 0:.*?installed=(\w+).*?enabled=(\d+)', dump)
    if not match or match.group(1) != 'true':
        raise RuntimeError(f'Cannot establish current user-0 state for {package}')
    state = int(match.group(2))
    if state not in range(5):
        raise RuntimeError(f'Unsupported enabled state: {state}')
    return state


def save(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def verify_package(adb, operation):
    names = package_names(adb.shell('pm', 'list', 'packages', '--user', '0'))
    package = operation['package']
    if operation['action'] == 'uninstall':
        if package in names:
            raise RuntimeError(f'{package} remains installed')
    elif enabled_state(adb, package) != 3:
        raise RuntimeError(f'{package} was not disabled')


def apply(adb, info, operations, output):
    # A journal is written BEFORE each mutation, so partial failures remain restorable.
    output.mkdir(parents=True, exist_ok=True)
    path = output / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    journal = {'schema': 1, 'device': info, 'entries': [], 'complete': False}
    save(path, journal)
    print(f'Restore journal: {path.resolve()}', flush=True)
    try:
        for operation in operations:
            entry = dict(operation)
            if entry['kind'] == 'setting':
                old = adb.shell('settings', 'get', 'global', entry['key']).strip()
                entry['previous'] = None if old == 'null' else old
            else:
                entry['previous'] = enabled_state(adb, entry['package'])
            journal['entries'].append(entry)
            save(path, journal)
            if entry['kind'] == 'setting':
                adb.shell('settings', 'put', 'global', entry['key'], entry['value'])
                if adb.shell('settings', 'get', 'global', entry['key']).strip() != entry['value']:
                    raise RuntimeError(f'Setting verification failed: {entry["key"]}')
            elif entry['action'] == 'uninstall':
                # Keep user data for reversibility. Factory APKs remain on system partitions.
                result = adb.shell('pm', 'uninstall', '-k', '--user', '0', entry['package'])
                if result.strip() != 'Success':
                    raise RuntimeError(result)
                verify_package(adb, entry)
            else:
                adb.shell('pm', 'disable-user', '--user', '0', entry['package'])
                verify_package(adb, entry)
            entry['verified'] = True
            save(path, journal)
            print('Verified:', entry.get('package', entry.get('key')))
        after = package_names(adb.shell('pm', 'list', 'packages', '-3', '--user', '0'))
        if after != set(info['third_party']):
            raise RuntimeError('Third-party app inventory changed; inspect the journal.')
        if all(any(op.get('package') == package for op in operations) for package in STOCK):
            resolved = adb.shell('cmd', 'package', 'resolve-activity', '--brief',
                                 '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.HOME')
            if HOME not in resolved:
                raise RuntimeError('FLauncher did not become HOME. Restore the journal before rebooting.')
        # Package restrictions may be written asynchronously. Never reboot immediately.
        if operations:
            print('Allowing 20 seconds for Android to save package state...', flush=True)
            time.sleep(20)
        journal['complete'] = True
        save(path, journal)
    except Exception:
        print(f'Apply stopped. Restore with: restore {path.resolve()}', flush=True)
        raise


def restore(adb, info, path):
    journal = json.loads(path.read_text(encoding='utf-8'))
    if journal.get('schema') != 1:
        raise ValueError('Unknown journal format')
    old = journal['device']
    if (info['manufacturer'], info['model']) != (old['manufacturer'], old['model']):
        raise ValueError('Journal belongs to another device model')
    if not info['serial'] or not old['serial'] or info['serial'] != old['serial']:
        raise ValueError('A matching, nonempty hardware serial is required for restore')
    commands = {0: 'default-state', 1: 'enable', 2: 'disable', 3: 'disable-user', 4: 'disable-until-used'}
    for entry in reversed(journal['entries']):
        if entry['kind'] == 'setting':
            if entry['previous'] is None:
                adb.shell('settings', 'delete', 'global', entry['key'])
            else:
                adb.shell('settings', 'put', 'global', entry['key'], entry['previous'])
            actual = adb.shell('settings', 'get', 'global', entry['key']).strip()
            expected = 'null' if entry['previous'] is None else entry['previous']
            if actual != expected:
                raise RuntimeError('Restore verification failed: ' + entry['key'])
        else:
            package = entry['package']
            present = package_names(adb.shell('pm', 'list', 'packages', '--user', '0'))
            if package not in present:
                adb.shell('cmd', 'package', 'install-existing', '--user', '0', package)
            adb.shell('pm', commands[entry['previous']], '--user', '0', package)
            if enabled_state(adb, package) != entry['previous']:
                raise RuntimeError('Restore verification failed: ' + package)
        print('Restored:', entry.get('package', entry.get('key')))
    time.sleep(20)
    print('Restored and verified. Reboot manually if desired.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', default='adb', help='Path to official Google adb executable')
    parser.add_argument('--device', required=True, help='Explicit ADB serial or IP:port; never auto-selects')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('inspect')
    for name in ['plan', 'apply']:
        child = sub.add_parser(name)
        for option in ['patchwall', 'disable-casting', 'disable-voice', 'animations-off', 'adguard-dns', 'flauncher']:
            child.add_argument('--' + option, action='store_true')
        if name == 'apply':
            child.add_argument('--confirm', action='store_true', help='Required to change the TV')
            child.add_argument('--state-dir', type=Path, default=Path('state'))
    child = sub.add_parser('restore')
    child.add_argument('journal', type=Path)
    child.add_argument('--confirm', action='store_true')
    args = parser.parse_args()
    adb = Adb(args.adb, args.device)
    info = inventory(adb)
    if args.command == 'inspect':
        print(json.dumps(info, indent=2))
    elif args.command == 'restore':
        if not args.confirm:
            parser.error('Restore changes the TV; pass --confirm after reviewing the journal.')
        restore(adb, info, args.journal)
    else:
        operations = build_plan(info, args)
        print(json.dumps(operations, indent=2))
        if args.command == 'apply':
            if not args.confirm:
                parser.error('Preview only. Pass --confirm to apply the listed changes.')
            if not info['serial']:
                raise ValueError('No hardware serial available; cannot create a restorable journal.')
            if args.flauncher:
                resolved = adb.shell('cmd', 'package', 'resolve-activity', '--brief',
                                     '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.HOME', LAUNCHER)
                if HOME not in resolved:
                    raise RuntimeError('FLauncher HOME activity not found; no changes applied.')
            apply(adb, info, operations, args.state_dir)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(str(error))
