# K2 Pro Custom Firmware / K2-OpenHost compatibility fork

This repository is a fork of **[Jacob10383/k2-plus-custom-firmware](https://github.com/Jacob10383/k2-plus-custom-firmware)**.

The original K2 custom-firmware stack, its architecture and the K2-specific extras were created by **Jacob10383/Jacobean**. Those upstream authorship references are intentionally preserved throughout this fork.

## Why this fork exists

`MzTechnology97/k2-pro-custom-firmware` is used by the **[K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost)** project to keep an auditable K2 Pro compatibility layer on top of Jacob's public K2 work.

The active development branch is:

```text
k2-openhost
```

That branch contains the Jacobean K2 extras plus the K2 Pro/OpenHost deltas validated on real hardware. It is **not** intended to erase or replace the original K2 Plus project history.

## Current role in K2-OpenHost

This repository is the versioned source/history for:

- Jacobean K2-specific Kalico extras;
- the K2 Pro four-byte CFS `BOX_STATE` compatibility change;
- protected CFS `observation_mode`;
- K2 Pro/OpenHost motor-control compatibility history;
- reproducible patch material synchronized into the active external-host Kalico tree.

The integrated runtime target is:

- **[MzTechnology97/kalico-k2pro](https://github.com/MzTechnology97/kalico-k2pro)**, branch `k2-pro-openhost`.

Cartographer runtime integration is maintained separately in:

- **[MzTechnology97/cartographer3d-plugin-k2openhost](https://github.com/MzTechnology97/cartographer3d-plugin-k2openhost)**.

The canonical architecture and hardware-validation record remains:

- **[MzTechnology97/K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost)**.

## Current hardware milestone — 2026-10-01

The project has progressed beyond transport and CFS observation testing. On the real K2 Pro, the external CM5/Kalico stack has now validated:

- Main MCU + Nozzle MCU simultaneous operation;
- RS-485 closed-loop motor communication;
- normal CoreXY motion;
- X/Y sensorless/stall homing;
- correct Z direction;
- complete homing with the stock PRTouch stack;
- bed/nozzle/chamber heater operation and PID tuning;
- emergency shutdown of active heater loads;
- successful Klippain-ShakeTune resonance measurement;
- protected CFS observation mode and K2 Pro four-byte steady-state support.

Stable transport mapping:

```text
/dev/ttyUSB0 -> Main MCU
/dev/ttyUSB1 -> Nozzle MCU
/dev/ttyUSB2 -> RS-485 / CFS / closed-loop
Cartographer -> direct USB on CM5 (target topology)
```

The earlier Cartographer T113 MUX/DEMUX experiment carried live Cartographer MCU data but is not retained as the production design. Direct USB to the CM5 is preferred for native reset/re-enumeration handling.

## Upstream K2 Plus documentation

The inherited `docs/` material originates from Jacob's K2 Plus custom-firmware project. It is preserved as upstream reference material and attribution. Some pages therefore describe a full K2 Plus firmware replacement and T113-local installation flow that is **not** the current K2 Pro/OpenHost deployment path.

For current K2 Pro/OpenHost procedures, use the `k2-openhost` branch documentation and the canonical K2-OpenHost repository.

## Branch policy

- `main` stays close to the Jacob-derived release base and carries fork/documentation context.
- `k2-openhost` contains the K2 Pro/OpenHost compatibility work and validated extra sources.

## Credits

Primary upstream projects/authors:

- **Jacob10383 / Jacobean** — original `k2-plus-custom-firmware`, K2 extras and related Kalico work.
- **KalicoCrew/kalico** — Kalico project and contributors.
- **Klipper3d/klipper** — Klipper project and contributors.
- **CrealityOfficial** — public K2 Klipper sources used by the wider community.

Additional reverse-engineering and K2 project references are listed in the K2-OpenHost documentation.

This fork is an independent community project and is not affiliated with Creality.