#!/usr/bin/env python3
"""Add cold-boot startup timing controls to the K2 Pro motor-control extra.

This patch is applied after patch-k2-pro-motor-control.py.  It keeps the
validated K2 Pro X/Y/E topology while making startup tolerant of a CM5 host
booting before the original T113/RS-485 side is fully ready.
"""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
MOTOR_CONTROL = ROOT / "extras" / "motor_control.py"
MANIFEST = ROOT / "extras" / "manifest.json"


def replace_once(text, old, new):
    if old not in text:
        raise RuntimeError("expected motor_control marker not found: %r" % old[:120])
    return text.replace(old, new, 1)


def patch_motor_control(text):
    if 'startup_delay=config.getfloat(' in text and 'self.retry_delay' in text:
        return text

    text = replace_once(text, '''CONTROL_OPTIONS = (\n    "overcurrent_switch",\n    "switch",\n    "retries",\n    "motor_closed_loop",\n)''', '''CONTROL_OPTIONS = (\n    "overcurrent_switch",\n    "switch",\n    "retries",\n    "startup_delay",\n    "retry_delay",\n    "motor_closed_loop",\n)''')

    text = replace_once(text, '''    closed_loop_axes: tuple[str, ...]\n    startup_retries: int\n    switch: int''', '''    closed_loop_axes: tuple[str, ...]\n    startup_retries: int\n    startup_delay: float\n    retry_delay: float\n    switch: int''')

    text = replace_once(text, '''            closed_loop_axes=cls._parse_closed_loop_axes(config),\n            startup_retries=config.getint("retries", 3, minval=0, maxval=10),\n            switch=config.getint("switch", 1, minval=0, maxval=1),''', '''            closed_loop_axes=cls._parse_closed_loop_axes(config),\n            startup_retries=config.getint("retries", 8, minval=0, maxval=20),\n            startup_delay=config.getfloat(\n                "startup_delay", 5.0, minval=0.0, maxval=120.0),\n            retry_delay=config.getfloat(\n                "retry_delay", 3.0, minval=0.0, maxval=60.0),\n            switch=config.getint("switch", 1, minval=0, maxval=1),''')

    text = replace_once(text, 'STARTUP_AUTO_RETRY_DELAY = 2.0',
                        'DEFAULT_STARTUP_DELAY = 5.0\nDEFAULT_RETRY_DELAY = 3.0')

    text = replace_once(text, '''            "K2 Pro topology closed_loop=%s retries=%d switch=%d overcurrent_switch=%d",\n            ",".join(self.config_model.closed_loop_axes),\n            self.config_model.startup_retries,\n            self.config_model.switch,\n            self.config_model.overcurrent_switch,''', '''            "K2 Pro topology closed_loop=%s retries=%d startup_delay=%.1fs retry_delay=%.1fs switch=%d overcurrent_switch=%d",\n            ",".join(self.config_model.closed_loop_axes),\n            self.config_model.startup_retries,\n            self.config_model.startup_delay,\n            self.config_model.retry_delay,\n            self.config_model.switch,\n            self.config_model.overcurrent_switch,''')

    text = replace_once(text, '''        self.auto_retry = True\n        self.startup_retry_limit = self.config_model.startup_retries\n        self.cut_pos_offset = self.config_model.cut_pos_offset''', '''        self.auto_retry = True\n        self.startup_retry_limit = self.config_model.startup_retries\n        self.startup_delay = self.config_model.startup_delay\n        self.retry_delay = self.config_model.retry_delay\n        self.cut_pos_offset = self.config_model.cut_pos_offset''')

    text = replace_once(text, '''                            STARTUP_AUTO_RETRY_DELAY,\n                            next_retry,''', '''                            self.retry_delay,\n                            next_retry,''')
    text = replace_once(text,
                        'return self.reactor.monotonic() + STARTUP_AUTO_RETRY_DELAY',
                        'return self.reactor.monotonic() + self.retry_delay')

    text = replace_once(text, '''        when = self.reactor.monotonic()\n        _klog("scheduling startup sequence at %.3f", when)\n        self.reactor.update_timer(self._startup_timer, when)''', '''        now = self.reactor.monotonic()\n        when = now + self.startup_delay\n        _klog(\n            "scheduling startup sequence at %.3f (delay %.1fs)",\n            when, self.startup_delay)\n        self.reactor.update_timer(self._startup_timer, when)''')

    if 'STARTUP_AUTO_RETRY_DELAY' in text:
        raise RuntimeError('legacy startup retry delay still present')
    return text


def update_manifest():
    manifest = json.loads(MANIFEST.read_text())
    raw = MOTOR_CONTROL.read_bytes()
    entry = manifest["files"]["motor_control.py"]
    entry["sha256"] = hashlib.sha256(raw).hexdigest()
    entry["size"] = len(raw)
    manifest["version"] = "6.20"
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def main():
    original = MOTOR_CONTROL.read_text()
    patched = patch_motor_control(original)
    MOTOR_CONTROL.write_text(patched)
    update_manifest()
    print("patched" if patched != original else "already patched")
    print("motor_control.py size=%d sha256=%s" % (
        len(MOTOR_CONTROL.read_bytes()),
        hashlib.sha256(MOTOR_CONTROL.read_bytes()).hexdigest(),
    ))


if __name__ == "__main__":
    main()
