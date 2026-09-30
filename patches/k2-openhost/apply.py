#!/usr/bin/env python3
"""Apply the hardware-validated K2-OpenHost Jacobean 6.18 patchset.

This applicator intentionally uses exact source replacements plus SHA-256
checks instead of fuzzy patch matching. It aborts if an unpatched upstream
file differs from the hardware-validated Jacobean 6.18 base.
"""

from __future__ import annotations

import hashlib
import py_compile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOX_PROTOCOL = ROOT / "extras" / "box_protocol.py"
BOX = ROOT / "extras" / "box.py"

BOX_PROTOCOL_SHA256 = (
    "78eedb979c21a64e42e3ea31f0906c3"
    "e8a129ddff903a5484ed1adc8371930ac"
)
BOX_SHA256 = (
    "6377ad449f9ce10ed3577ba9ffe390905"
    "7b61fa0806f25f7ef483b55537dd7a1"
)

BOX_PROTOCOL_MARKER = "K2-OpenHost: K2 Pro 4-byte BOX_STATE compatibility"
BOX_MARKER = "# K2-OpenHost observation mode"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def prepare(path: Path, expected_sha: str, marker: str) -> tuple[str, bool]:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"already patched: {path.relative_to(ROOT)}")
        return text, False

    actual = sha256(path)
    if actual != expected_sha:
        raise RuntimeError(
            f"refusing to patch {path.relative_to(ROOT)}\n"
            f"expected SHA-256: {expected_sha}\n"
            f"actual SHA-256:   {actual}"
        )

    backup = path.with_name(path.name + ".k2-openhost.orig")
    if not backup.exists():
        shutil.copy2(path, backup)
    return text, True


def patch_box_protocol() -> None:
    text, needs_patch = prepare(
        BOX_PROTOCOL, BOX_PROTOCOL_SHA256, BOX_PROTOCOL_MARKER
    )
    if not needs_patch:
        return

    text = replace_once(
        text,
        '''@dataclass(frozen=True)
class BoxStateReply(Reply):
    temp_c: object
    humidity_pct: object
    box_state: object
    downstream_mask: object
    slot_events: object
''',
        '''@dataclass(frozen=True)
class BoxStateReply(Reply):
    temp_c: object
    humidity_pct: object
    box_state: object
    downstream_mask: object
    slot_events: object

    # K2-OpenHost: K2 Pro 4-byte BOX_STATE compatibility
    firmware_base: object = None
    substatus: object = None
    load_flag: object = None
''',
        "BoxStateReply extension",
    )

    text = replace_once(
        text,
        '''    empty = (None, None, None, None)
''',
        '''    empty = (None, None, None, None)
    firmware_base = None
    substatus = None
    load_flag = None
''',
        "BOX_STATE optional fields",
    )

    text = replace_once(
        text,
        '''    elif len(reply.payload) == 6:
''',
        '''    elif reply.status == STATUS_OK and len(reply.payload) == 4:
        firmware_base = (
            (reply.payload[0] << 8)
            | reply.payload[1]
        )
        substatus = reply.payload[2]
        load_flag = reply.payload[3]

        values = empty
        events = None

    elif len(reply.payload) == 6:
''',
        "K2 Pro 4-byte BOX_STATE branch",
    )

    text = replace_once(
        text,
        '''    return BoxStateReply(
        reply.address, reply.command, reply.status, reply.payload, reply.raw,
        *values, events,
    )
''',
        '''    return BoxStateReply(
        reply.address, reply.command, reply.status, reply.payload, reply.raw,
        *values, events,
        firmware_base, substatus, load_flag,
    )
''',
        "BoxStateReply return fields",
    )

    BOX_PROTOCOL.write_text(text, encoding="utf-8")
    print(f"patched: {BOX_PROTOCOL.relative_to(ROOT)}")


def patch_box() -> None:
    text, needs_patch = prepare(BOX, BOX_SHA256, BOX_MARKER)
    if not needs_patch:
        return

    text = replace_once(
        text,
        '''class BoxError(RuntimeError):
    pass


@dataclass(frozen=True)
class BoxSnapshot:
''',
        '''class BoxError(RuntimeError):
    pass


# K2-OpenHost observation mode
class _ReadOnlyCFSProxy:
    """Block mutating CFS functions before they reach serial_485."""

    ALLOWED_FUNCTIONS = frozenset((
        0x02,  # RFID/material records
        0x03,  # remaining
        0x05,  # buffer
        0x08,  # slot/hub mask
        0x0A,  # box state
        0x0E,  # encoder
        0x14,  # version/SN
        0xF0,  # firmware version
        0xA1,  # discovery
        0xA2,  # online check
        0xA3,  # address table
    ))

    def __init__(self, transport):
        self.transport = transport
        self.allowed_requests = 0
        self.blocked_requests = 0
        self.blocked_functions = []

    def cmd_send_data_with_response(
            self, data, timeout=1.0, attempts=1):
        body = bytes(data)

        if len(body) < 4:
            self.blocked_requests += 1
            raise PermissionError(
                "CFS observation guard: malformed request blocked"
            )

        address = body[0]
        function = body[3]

        if function not in self.ALLOWED_FUNCTIONS:
            self.blocked_requests += 1
            self.blocked_functions.append((address, function))
            raise PermissionError(
                "CFS observation guard: "
                "blocked addr=0x%02X func=0x%02X"
                % (address, function)
            )

        self.allowed_requests += 1
        return self.transport.cmd_send_data_with_response(
            data, timeout, attempts=attempts,
        )


@dataclass(frozen=True)
class BoxSnapshot:
''',
        "read-only CFS proxy",
    )

    text = replace_once(
        text,
        '''        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object("gcode")
        self.pause_resume = self.printer.load_object(config, "pause_resume")
        self.box_count = config.getint(
            "box_count", MAX_ADDRESSES, minval=1, maxval=MAX_ADDRESSES)
        self.store = BoxStore(config.get(
            "state_path", "/mnt/UDISK/printer_data/filament_box.json"))
''',
        '''        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object("gcode")

        # K2-OpenHost observation mode
        self.observation_mode = config.getboolean(
            "observation_mode", False)

        self.pause_resume = self.printer.load_object(
            config, "pause_resume")

        self.box_count = config.getint(
            "box_count", MAX_ADDRESSES,
            minval=1, maxval=MAX_ADDRESSES)

        default_state_path = (
            "/dev/shm/k2-openhost-filament_box.json"
            if self.observation_mode
            else "/mnt/UDISK/printer_data/filament_box.json"
        )

        self.store = BoxStore(
            config.get("state_path", default_state_path)
        )
''',
        "observation-mode configuration",
    )

    text = replace_once(
        text,
        '''        pins = self.printer.lookup_object("pins")
        pins.allow_multi_use_pin("nozzle_mcu:PB9")
        buttons = self.printer.load_object(config, "buttons")
        self.cut_sensor_state = False
        buttons.register_buttons(["!nozzle_mcu:PB9"], self._cut_sensor_callback)

        self.address_manager = AutoAddressManager(self.box_count, self.store.known_addresses)
        self.change_engine = BoxChangeEngine(self, config)
''',
        '''        self.cut_sensor_state = False

        if not self.observation_mode:
            pins = self.printer.lookup_object("pins")
            pins.allow_multi_use_pin("nozzle_mcu:PB9")
            buttons = self.printer.load_object(config, "buttons")
            buttons.register_buttons(
                ["!nozzle_mcu:PB9"],
                self._cut_sensor_callback
            )

        self.address_manager = AutoAddressManager(
            self.box_count,
            self.store.known_addresses
        )

        self.change_engine = BoxChangeEngine(self, config)
''',
        "cut-sensor isolation",
    )

    text = replace_once(
        text,
        '''    def _register_commands(self):
        commands = (
''',
        '''    def _register_commands(self):
        # K2-OpenHost observation mode:
        # no user-facing operational commands are registered.
        if self.observation_mode:
            return

        commands = (
''',
        "operational G-code guard",
    )

    text = replace_once(
        text,
        '''        self._invalidate_tracking_session()
        self.serial = self.printer.lookup_object("serial_485 serial485")
        client = box_protocol.AutoAddressClient(self.serial)
''',
        '''        self._invalidate_tracking_session()
        base_serial = self.printer.lookup_object(
            "serial_485 serial485"
        )

        self.serial = (
            _ReadOnlyCFSProxy(base_serial)
            if self.observation_mode
            else base_serial
        )

        client = box_protocol.AutoAddressClient(self.serial)
''',
        "CFS transport proxy",
    )

    text = replace_once(
        text,
        '''    def _register_t_commands(self):
        if self.tx_registered:
''',
        '''    def _register_t_commands(self):
        if self.observation_mode:
            return

        if self.tx_registered:
''',
        "T-command guard",
    )

    text = replace_once(
        text,
        '''    def _klippy_ready(self, *args):
        self.klippy_ready = True
        self.reactor.register_callback(self._install_runout_source_observer)
        if self.drivers_ready:
''',
        '''    def _klippy_ready(self, *args):
        self.klippy_ready = True

        if not self.observation_mode:
            self.reactor.register_callback(
                self._install_runout_source_observer
            )

        if self.drivers_ready:
''',
        "runout-observer guard",
    )

    text = replace_once(
        text,
        '''    def _initialize_rfid(self):
        """Apply persisted reader policy and establish presence baselines."""
        for address, driver in sorted(self.drivers.items()):
''',
        '''    def _initialize_rfid(self):
        """Apply persisted reader policy and establish presence baselines."""

        if self.observation_mode:
            for address, driver in sorted(self.drivers.items()):
                try:
                    slots = self._require_reply(
                        driver.query_slot_mask(timeout=0.5),
                        "box %d RFID presence baseline"
                        % address
                    )

                    self.rfid_presence[address] = (
                        slots.value & 0x0F
                    )

                except Exception:
                    _klog(
                        "observation RFID baseline failed "
                        "for box %d",
                        address,
                        level=logging.exception
                    )

            return

        for address, driver in sorted(self.drivers.items()):
''',
        "RFID startup write guard",
    )

    BOX.write_text(text, encoding="utf-8")
    print(f"patched: {BOX.relative_to(ROOT)}")


def main() -> None:
    patch_box_protocol()
    patch_box()

    py_compile.compile(str(BOX_PROTOCOL), doraise=True)
    py_compile.compile(str(BOX), doraise=True)
    print("Python compile: OK")


if __name__ == "__main__":
    main()
