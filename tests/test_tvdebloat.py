import argparse
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import tvdebloat as tv


def options(**overrides):
    values = dict(patchwall=False, disable_casting=False, disable_voice=False,
                  animations_off=False, adguard_dns=False, flauncher=False)
    values.update(overrides)
    return argparse.Namespace(**values)


class FakeAdb:
    def __init__(self):
        self.installed = {'com.netflix.ninja', 'user.app'}
        self.states = {'com.netflix.ninja': 0}
        self.settings = {}
        self.fail_setting = False

    def shell(self, *args):
        if args[:3] == ('pm', 'list', 'packages'):
            names = {'user.app'} if '-3' in args else self.installed
            return '\n'.join('package:' + name for name in sorted(names))
        if args[:2] == ('dumpsys', 'package'):
            return f'User 0: installed=true hidden=false enabled={self.states[args[2]]}'
        if args[:2] == ('pm', 'uninstall'):
            self.installed.remove(args[-1])
            return 'Success'
        if args[:3] == ('cmd', 'package', 'install-existing'):
            self.installed.add(args[-1])
            return 'installed'
        if args[0] == 'pm' and args[1] in ['default-state', 'enable', 'disable', 'disable-user', 'disable-until-used']:
            self.states[args[-1]] = ['default-state', 'enable', 'disable', 'disable-user', 'disable-until-used'].index(args[1])
            return 'new state'
        if args[:2] == ('settings', 'get'):
            return self.settings.get(args[3], 'null')
        if args[:2] == ('settings', 'put'):
            if self.fail_setting:
                raise RuntimeError('simulated disconnection')
            self.settings[args[3]] = args[4]
            return ''
        if args[:2] == ('settings', 'delete'):
            self.settings.pop(args[3], None)
            return ''
        raise AssertionError(args)


class PlanTests(unittest.TestCase):
    def info(self):
        return dict(manufacturer='Xiaomi', model='MiTV-AESP0', serial='fake-serial',
                    installed=['com.netflix.ninja', 'user.app'],
                    system=['com.netflix.ninja'], third_party=['user.app'])

    def test_never_targets_third_party_even_with_matching_name(self):
        info = self.info()
        info['system'] = []
        self.assertEqual(tv.build_plan(info, options()), [])

    def test_non_xiaomi_rejected(self):
        info = self.info()
        info['manufacturer'] = 'Other'
        with self.assertRaises(ValueError):
            tv.build_plan(info, options())

    def test_missing_launcher_fails_before_changes(self):
        with self.assertRaises(ValueError):
            tv.build_plan(self.info(), options(flauncher=True))

    def test_optional_features_opt_in(self):
        plan = tv.build_plan(self.info(), options())
        self.assertEqual(plan, [dict(kind='package', package='com.netflix.ninja', action='uninstall')])

    def test_full_profile_never_targets_core_services(self):
        packages = tv.OPTIONAL_APPS + tv.STOCK + [tv.LAUNCHER, 'com.android.systemui',
                    'com.google.android.gms', 'com.android.vending', 'com.android.bluetooth',
                    'com.xiaomi.mitv.updateservice', 'com.google.android.katniss',
                    'com.google.android.apps.mediashell', 'com.mitv.tvhome.atv']
        info = dict(self.info(), installed=packages, system=[p for p in packages if p != tv.LAUNCHER])
        plan = tv.build_plan(info, options(patchwall=True, disable_casting=True,
                             disable_voice=True, animations_off=True, adguard_dns=True, flauncher=True))
        targeted = {op.get('package') for op in plan}
        self.assertFalse(targeted & {'com.android.systemui', 'com.google.android.gms',
                         'com.android.vending', 'com.android.bluetooth',
                         'com.xiaomi.mitv.updateservice', tv.LAUNCHER})

    @patch('tvdebloat.time.sleep')
    def test_restore_preserves_preexisting_disabled_state(self, sleep):
        adb, info = FakeAdb(), self.info()
        adb.states['com.netflix.ninja'] = 3
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tv.apply(adb, info, tv.build_plan(info, options()), root)
            tv.restore(adb, info, next(root.glob('*.json')))
            self.assertEqual(adb.states['com.netflix.ninja'], 3)

    @patch('tvdebloat.time.sleep')
    def test_apply_then_restore_preserves_default_state(self, sleep):
        adb, info = FakeAdb(), self.info()
        operations = tv.build_plan(info, options(animations_off=True, adguard_dns=True))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tv.apply(adb, info, operations, root)
            journal = next(root.glob('*.json'))
            self.assertTrue(json.loads(journal.read_text())['complete'])
            self.assertNotIn('com.netflix.ninja', adb.installed)
            tv.restore(adb, info, journal)
            self.assertIn('com.netflix.ninja', adb.installed)
            self.assertEqual(adb.states['com.netflix.ninja'], 0)
            self.assertEqual(adb.settings, {})

    @patch('tvdebloat.time.sleep')
    def test_partial_failure_is_restorable(self, sleep):
        adb, info = FakeAdb(), self.info()
        adb.fail_setting = True
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(RuntimeError):
                tv.apply(adb, info, tv.build_plan(info, options(animations_off=True)), root)
            journal = next(root.glob('*.json'))
            self.assertFalse(json.loads(journal.read_text())['complete'])
            tv.restore(adb, info, journal)
            self.assertIn('com.netflix.ninja', adb.installed)

    @patch('tvdebloat.time.sleep')
    def test_restore_rejects_other_device(self, sleep):
        adb, info = FakeAdb(), self.info()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tv.apply(adb, info, [], root)
            info = dict(info, serial='another-device')
            with self.assertRaises(ValueError):
                tv.restore(adb, info, next(root.glob('*.json')))


if __name__ == '__main__':
    unittest.main()
