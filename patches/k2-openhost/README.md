# K2-OpenHost validated patchset

This directory preserves the exact K2-OpenHost changes that were hardware-validated against the Jacobean 6.18 CFS extras on a Creality K2 Pro.

## Base files

The patches are SHA-gated against these original Jacobean 6.18 files:

```text
extras/box_protocol.py
SHA-256 78eedb979c21a64e42e3ea31f0906c3e8a129ddff903a5484ed1adc8371930ac

extras/box.py
SHA-256 6377ad449f9ce10ed3577ba9ffe3909057b61fa0806f25f7ef483b55537dd7a1
```

The fork `main` branch should remain suitable for tracking Jacob upstream. K2-OpenHost compatibility work lives on the `k2-openhost` branch.

## Patch 0001: K2 Pro 4-byte BOX_STATE

`0001-k2-pro-box-state-4byte.patch` extends `BoxStateReply` and `decode_box_state()` so the K2 Pro steady `CMD_BOX_STATE (0x0A)` four-byte payload can be decoded without fabricating fields that are absent on this firmware.

Validated properties:

- upstream 6-byte decoding is retained;
- `STATUS=0x30` slot-event decoding is retained;
- four-byte steady payload exposes `firmware_base`, `substatus`, and `load_flag`;
- `temp_c`, `humidity_pct`, `box_state`, and `downstream_mask` remain `None` for the K2 Pro four-byte representation.

Hardware validation returned the native Jacob `BoxStateReply` successfully and preserved the previously captured slot event `slot_events=[2, 3, 0, 0]`.

## Patch 0002: protected CFS observation mode

`0002-cfs-observation-mode.patch` adds an `observation_mode` to `box.py` for safe integration testing.

When enabled it:

- wraps only the CFS path in a read-only transport proxy;
- leaves the shared `serial_485.py` transport untouched for other RS-485 devices such as closed-loop controllers;
- permits the read-only CFS functions used by discovery and polling;
- blocks mutating CFS functions before they reach the underlying serial transport;
- skips the automatic RFID policy write (`0x0D`) during startup;
- does not register operational `BOX_*` commands;
- does not register `Tn` material-change commands;
- does not register the nozzle cut sensor;
- does not install the automatic runout observer;
- defaults observation state storage to `/dev/shm/k2-openhost-filament_box.json`.

## Hardware validation result

The real Jacob `Box()` class was instantiated behind the observation guard and successfully completed enumeration, RFID presence baseline, `read_live_state()`, and an internal `_poll()` cycle through K2-OpenHost.

Observed state during the validation:

```text
CFS address: 0x01
slot_mask: 0x0E
hub_mask: 0x00
buffer_state: 2
loaded_slot: -1
loaded_mask: 0x0
tracking: false
BOX_STATE status: 0x00
substatus: 0
load_flag: 0
```

The explicit guard self-test attempted CFS function `0x0D` and confirmed that the underlying TX counter did not increase.

Final transport statistics from the native `Box()` observation test:

```text
allowed requests: 35
blocked requests: 1
tx_frames: 35
rx_frames: 35
crc_errors: 0
invalid_len: 0
unmatched: 0
stale_dropped: 0
timeouts: 0
send_errors: 0
reader_errors: 0
```

The `filament_sensor_error` seen in the standalone Python harness is expected because that harness intentionally did not instantiate the real Kalico `filament_switch_sensor`; it is not a CFS transport error.

## Apply the validated patchset

From the repository root:

```sh
sh patches/k2-openhost/apply.sh
```

The script:

1. checks the SHA-256 of each unmodified source file;
2. refuses to patch an unexpected upstream version;
3. stores a `.k2-openhost.orig` backup;
4. applies the two validated patches;
5. verifies patch markers;
6. runs `python3 -m py_compile` on both modified modules.

Do not bypass the SHA checks when moving to a newer Jacob release. Rebase/review the patchset against that release instead.

## Current safety boundary

This patchset is for observation and compatibility validation only. Automatic CFS load/unload remains intentionally disabled until K2 Pro loaded-path semantics are correlated reliably; the K2 Pro four-byte steady state does not provide Jacob's six-byte `downstream_mask` field.
