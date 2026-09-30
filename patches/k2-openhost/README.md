# K2-OpenHost validated patchset

This directory preserves the exact K2-OpenHost changes that were hardware-validated against the Jacobean 6.18 CFS extras on a Creality K2 Pro.

## Branch layout

- `main` remains the clean Jacob-derived branch and is the reference for future upstream syncs.
- `k2-openhost` contains the K2 Pro compatibility changes directly in `extras/box_protocol.py` and `extras/box.py`.
- this directory also keeps standalone unified-diff snapshots plus a SHA-gated deterministic applicator, so the changes remain reproducible even outside the branch history.

The current fork base is Jacob-derived commit:

```text
370957f83c640b595327cbf95650221aa8325d83
```

## Base files

The applicator is SHA-gated against these original Jacobean 6.18 files:

```text
extras/box_protocol.py
SHA-256 78eedb979c21a64e42e3ea31f0906c3e8a129ddff903a5484ed1adc8371930ac

extras/box.py
SHA-256 6377ad449f9ce10ed3577ba9ffe3909057b61fa0806f25f7ef483b55537dd7a1
```

## Patch 0001: K2 Pro 4-byte BOX_STATE

`0001-k2-pro-box-state-4byte.patch` extends `BoxStateReply` and `decode_box_state()` so the K2 Pro steady `CMD_BOX_STATE (0x0A)` four-byte payload can be decoded without fabricating fields that are absent on this firmware.

Validated properties:

- upstream 6-byte decoding is retained;
- `STATUS=0x30` slot-event decoding is retained;
- four-byte steady payload exposes `firmware_base`, `substatus`, and `load_flag`;
- `temp_c`, `humidity_pct`, `box_state`, and `downstream_mask` remain `None` for the K2 Pro four-byte representation.

Hardware validation returned the native Jacob `BoxStateReply` successfully and preserved the captured slot event `slot_events=[2, 3, 0, 0]`.

The direct source implementation was committed as:

```text
58438be54af474138c4f85eb6084edd8c0bc1096
k2-openhost: support K2 Pro 4-byte CFS BOX_STATE
```

## Patch 0002: protected CFS observation mode

`0002-cfs-observation-mode.patch` adds an `observation_mode` to `box.py` for safe integration testing.

When enabled it:

- wraps only the CFS path in a read-only transport proxy;
- leaves the shared `serial_485.py` transport untouched for other RS-485 devices such as closed-loop controllers;
- permits only the read-only CFS functions needed by discovery and polling;
- blocks mutating CFS functions before they reach the underlying serial transport;
- skips the automatic RFID policy write (`0x0D`) during startup;
- does not register operational `BOX_*` commands;
- does not register `Tn` material-change commands;
- does not register the nozzle cut sensor;
- does not install the automatic runout observer;
- defaults observation state storage to `/dev/shm/k2-openhost-filament_box.json`.

The direct source implementation was committed by CI as:

```text
7132f263c1706ad6810d8ec22c7a848e909b438a
k2-openhost: apply validated K2 Pro compatibility patches
```

## Hardware validation result

The real Jacob `Box()` class was instantiated behind the observation guard and successfully completed enumeration, RFID presence baseline, ten `read_live_state()` cycles, and an internal `_poll()` cycle through K2-OpenHost.

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

## Reproducibility paths

For a clean Jacobean 6.18 tree, the deterministic path is:

```sh
sh patches/k2-openhost/apply.sh
```

`apply.sh` invokes `apply.py`, which:

1. checks the exact SHA-256 of each unmodified source file;
2. refuses to touch an unexpected upstream version;
3. stores a `.k2-openhost.orig` backup;
4. applies the exact hardware-validated source replacements;
5. runs `python3 -m py_compile` on both modified modules.

The standalone files:

```text
0001-k2-pro-box-state-4byte.patch
0002-cfs-observation-mode.patch
```

are also real unified diffs against `main`. GitHub Actions validates them by applying both to a clean `origin/main` worktree and compiling the resulting modules. This guards the archive against drifting away from the directly committed source changes.

Do not bypass the SHA checks when moving to a newer Jacob release. Rebase/review the patchset against that release instead.

## Current safety boundary

This patchset is for observation and compatibility validation only. Automatic CFS load/unload remains intentionally disabled until K2 Pro loaded-path semantics are correlated reliably; the K2 Pro four-byte steady state does not provide Jacob's six-byte `downstream_mask` field.
