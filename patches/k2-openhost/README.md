# K2-OpenHost validated patchset

This directory preserves the exact K2-OpenHost changes hardware-validated against the **Jacobean 6.18 K2 extras** on a Creality K2 Pro.

The underlying K2 custom-firmware/extras work is authored by **Jacob10383/Jacobean** and originates from `Jacob10383/k2-plus-custom-firmware`. These patch files represent only the K2 Pro/OpenHost compatibility and safety deltas applied by this fork.

## Repository role

- `main` is the Jacob-derived reference branch plus fork documentation context.
- `k2-openhost` contains the compatibility changes directly in `extras/box_protocol.py` and `extras/box.py`.
- these `.patch` files provide reproducible snapshots of those same changes.
- the resulting extra sources were originally synchronized into `MzTechnology97/kalico-k2pro:k2-pro-openhost` for CM5 testing.

Since 2026-10-02 the CFS extras (persistent inventory, K2-RFID catalog, auto mapping, K2 Pro adapter and environment reporting) are developed and hardware-tested directly in `kalico-k2pro:k2-pro-openhost`. The `extras/box*.py` files on this branch mirror that tree, and the automatic Kalico-side sync workflow has been replaced by a read-only drift check. `extras/manifest.json` intentionally keeps the upstream Jacobean base hashes used by the guards below.

The patch base is the Jacob-derived commit:

```text
370957f83c640b595327cbf95650221aa8325d83
```

## Original file guards

```text
extras/box_protocol.py
SHA-256 78eedb979c21a64e42e3ea31f0906c3e8a129ddff903a5484ed1adc8371930ac

extras/box.py
SHA-256 6377ad449f9ce10ed3577ba9ffe3909057b61fa0806f25f7ef483b55537dd7a1
```

## Patch 0001 — K2 Pro four-byte BOX_STATE

`0001-k2-pro-box-state-4byte.patch` extends the Jacobean decoder so the tested K2 Pro steady four-byte `CMD_BOX_STATE (0x0A)` payload is accepted without fabricating fields that are not present.

Validated properties:

- existing six-byte decoding retained;
- `STATUS=0x30` slot-event decoding retained;
- four-byte steady representation exposes `firmware_base`, `substatus` and `load_flag`;
- legacy-only fields remain `None` for the K2 Pro representation.

## Patch 0002 — protected CFS observation mode

`0002-cfs-observation-mode.patch` adds `observation_mode` to `box.py`.

When enabled it:

- wraps only the CFS/Box path in a read-only transport proxy;
- leaves shared `serial_485.py` available to other RS-485 devices;
- blocks non-whitelisted CFS functions before TX;
- skips the automatic RFID policy write (`0x0D`);
- does not register operational `BOX_*` or `Tn` commands;
- does not install automatic runout behavior;
- defaults observation state to a volatile `/dev/shm` path.

## Hardware validation

The real Jacobean `Box()` class completed enumeration, RFID/slot baseline, ten `read_live_state()` cycles and an internal `_poll()` through K2-OpenHost.

The explicit guard test attempted function `0x0D` and confirmed the underlying TX counter did not increase.

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

The standalone harness intentionally lacked the real filament-switch object, so its filament-sensor warning is not a CFS transport failure.

## Reproducibility

For the exact supported Jacobean base:

```sh
sh patches/k2-openhost/apply.sh
```

The SHA-gated applicator refuses an unexpected upstream version, stores backups, applies the validated replacements and compiles the modified modules. GitHub Actions also verifies the unified diffs against a clean base.

Do not bypass the SHA guards on a newer Jacob release. Rebase/review the changes instead.

## Safety boundary

This patchset is still an observation/compatibility layer. Automatic CFS load/unload remains disabled until loaded-path semantics and the full CM5 Klippy integration are validated.