# K2-OpenHost integration branch

This branch carries the K2 Pro/OpenHost compatibility layer on top of the public **Jacob10383/Jacobean K2 custom-firmware extras**.

## Upstream base

Original upstream project:

- `Jacob10383/k2-plus-custom-firmware`

Original K2 extras and full-firmware design remain attributed to Jacob10383/Jacobean.

## Current architecture

The project no longer relies on manually overlaying these files onto an unrelated Kalico clone. The integrated CM5 target is now:

```text
MzTechnology97/kalico-k2pro
branch: k2-pro-openhost
```

That fork is based on `Jacob10383/kalico` and currently contains:

- the Kalico core;
- a K2 Pro `.cfg` baseline;
- the K2-specific extras synchronized from this branch;
- the hardware-validated OpenHost CFS patches.

This repository remains the clean source/history for those extras and patches.

## Validated patchset

Stored under:

```text
patches/k2-openhost/
```

Current patches:

1. K2 Pro four-byte CFS `BOX_STATE` compatibility for `extras/box_protocol.py`;
2. protected CFS `observation_mode` for `extras/box.py`.

The branch contains the patched source directly, while the unified diffs and SHA-gated applicator provide a reproducible archive against the clean Jacob-derived base.

## Why serial_485.py is not globally restricted

The K2 RS-485 path is shared by the CFS and other K2 hardware such as closed-loop/belt devices. The read-only protection is therefore applied only to the Box/CFS stack, not to the common serial transport.

## Hardware milestone

The real Jacobean `Box()` class has been exercised through the full K2-OpenHost path on a K2 Pro:

- enumeration completed;
- read-only RFID/slot baseline completed;
- ten live-state polls completed;
- internal `_poll()` completed;
- function `0x0D` was deliberately attempted and blocked before TX;
- final transport statistics: 35 TX / 35 RX, all error counters zero.

Automatic CFS load/unload remains intentionally disabled pending loaded-path correlation and full real-Klippy observation testing on the CM5.

## Documentation ownership

- this repo/branch: source patches and Jacobean extra integration;
- `MzTechnology97/kalico-k2pro:k2-pro-openhost`: integrated Kalico test tree;
- `MzTechnology97/K2-OpenHost`: canonical architecture, test status, roadmap and cross-project credits.