# K2-OpenHost integration branch

This branch carries the K2 Pro/OpenHost compatibility layer on top of the public **Jacob10383/Jacobean K2 custom-firmware extras**.

Updated: **2026-10-01**.

## Upstream base

Original upstream project:

- `Jacob10383/k2-plus-custom-firmware`

Original K2 extras and full-firmware design remain attributed to Jacob10383/Jacobean.

## Current architecture

The integrated CM5 target is:

```text
MzTechnology97/kalico-k2pro
branch: k2-pro-openhost
```

The stable hardware transport uses three independent T113 gadget serial channels:

```text
Main MCU   -> /dev/ttyUSB0 -> ttyGS0 -> ttyS2
Nozzle MCU -> /dev/ttyUSB1 -> ttyGS1 -> ttyS3
RS-485/CFS -> /dev/ttyUSB2 -> ttyGS2 -> ttyS5
```

Cartographer is handled by the separate `MzTechnology97/cartographer3d-plugin-k2openhost` project and is now intended to connect **directly to the CM5 USB host**. A T113 MUX/DEMUX bridge was prototyped and transported live Cartographer data, but reset/re-enumeration complexity made direct USB the preferred final path.

This repository remains the clean source/history for K2/Jacobean extras and OpenHost/K2 Pro compatibility patches; it is not the runtime CM5 checkout.

## Validated patchset

Stored under:

```text
patches/k2-openhost/
```

The branch history includes:

1. K2 Pro four-byte CFS `BOX_STATE` compatibility for `extras/box_protocol.py`;
2. protected CFS `observation_mode` for `extras/box.py`;
3. K2 Pro/OpenHost motor-control compatibility used by the integrated Kalico tree.

The patched source and reproducible diffs preserve an auditable history against the Jacob-derived base.

## Why serial_485.py is not globally restricted

The K2 RS-485 path is shared by CFS and other hardware, including the closed-loop motor controllers. The read-only protection is therefore applied only to the Box/CFS stack, not to the common serial transport.

This separation became especially important during OpenHost motion testing: the same `/dev/ttyUSB2` transport now carries validated closed-loop X/Y communication and sensorless/stall homing while the CFS layer remains protected.

## Hardware milestones

### CFS observation milestone

The real Jacobean `Box()` class was exercised through the OpenHost path on a K2 Pro:

- enumeration completed;
- read-only RFID/slot baseline completed;
- ten live-state polls completed;
- internal `_poll()` completed;
- function `0x0D` was deliberately attempted and blocked before TX;
- final transport statistics: 35 TX / 35 RX, all error counters zero.

Automatic CFS load/unload remains intentionally disabled pending loaded-path correlation and controlled mutation tests.

### Full external-host machine-control milestone

Using `kalico-k2pro:k2-pro-openhost` on the CM5, the real K2 Pro has now also validated:

- Main and Nozzle MCU simultaneous control;
- closed-loop X/Y motor startup and communication;
- normal CoreXY movement;
- X/Y sensorless/stall homing;
- correct Z direction;
- complete homing using stock PRTouch;
- bed/nozzle/chamber heaters and PID tuning;
- emergency shutdown with active heater load removed;
- Klippain-ShakeTune resonance testing.

A duplicate GS2 bridge discovered during the experimental Cartographer multiplexing work caused RS-485 instability. Returning to exactly one `ttyGS2 <-> ttyS5` bridge restored normal motor-control behaviour. The final architecture therefore keeps GS2 dedicated to the original RS-485 bus.

## Documentation ownership

- this repo/branch: source patches and Jacobean extra integration/history;
- `MzTechnology97/kalico-k2pro:k2-pro-openhost`: integrated Kalico runtime tree;
- `MzTechnology97/cartographer3d-plugin-k2openhost`: Cartographer K2/OpenHost integration;
- `MzTechnology97/K2-OpenHost`: canonical architecture, test status, roadmap and cross-project credits.