# K2 Pro Custom Firmware — K2-OpenHost branch

This branch is part of the **[K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost)** project and is derived from **[Jacob10383/k2-plus-custom-firmware](https://github.com/Jacob10383/k2-plus-custom-firmware)**.

> [!WARNING]
> **Experienced users only — use at your own risk.** K2-OpenHost voids the manufacturer's warranty and can damage the printer beyond repair, brick its firmware or, in case of malfunction, cause a fire. The authors accept no liability for damage to property or persons.
> In OpenHost mode the **nozzle and chamber cameras** cannot be managed by the T113 and must be rewired directly to the external Linux host, and the printer's **external USB port** cannot be used to print and stops working completely in gadget mode.
> Read the [disclaimer and hardware limitations](https://github.com/MzTechnology97/K2-OpenHost/blob/main/docs/en/DISCLAIMER.md) ([italiano](https://github.com/MzTechnology97/K2-OpenHost/blob/main/docs/it/DISCLAIMER.md)) before using this repository.

The original K2 custom-firmware stack and K2-specific extras were created by **Jacob10383/Jacobean**. This fork keeps that attribution visible and carries only the K2 Pro/OpenHost deltas validated during our hardware work.

## Branch purpose

`k2-openhost` remains the **versioned source/history for Jacobean K2 extras plus K2 Pro/OpenHost compatibility and safety patches**. The integrated runtime target is:

```text
MzTechnology97/kalico-k2pro
branch: k2-pro-openhost
```

The Kalico fork contains the real external-host configuration and synchronized K2 extras used during current CM5 testing.

## Hardware-validated K2 Pro deltas

Validated work originating or archived here includes:

- K2 Pro four-byte CFS `BOX_STATE` support in `extras/box_protocol.py`, while preserving the original Jacobean six-byte/event paths;
- protected CFS `observation_mode` in `extras/box.py`;
- CFS-only read guard that leaves shared `serial_485.py` available to motor-control and other K2 RS-485 devices;
- K2 Pro motor-control topology/integration used by the external Kalico branch;
- reproducible patch/history material for OpenHost-specific K2 extras.

The real Jacobean `Box()` class completed observation polling through the OpenHost path with **35 TX / 35 RX and zero transport errors**. A deliberate `0x0D` mutation was blocked before TX.

## Current OpenHost milestone — 2026-10-01

The project has progressed well beyond the original observation-only stage. On the real K2 Pro, the external CM5/Kalico stack has now validated:

- Main MCU + Nozzle MCU simultaneous operation;
- RS-485 closed-loop motor communication;
- normal CoreXY motion;
- X/Y sensorless/stall homing;
- correct Z direction;
- full homing with the stock PRTouch stack;
- bed/nozzle/chamber heater operation and PID tuning;
- emergency shutdown with active heater loads removed correctly;
- Klippain-ShakeTune resonance testing.

The stable transport remains three dedicated T113 gadget serial channels:

```text
/dev/ttyUSB0 -> Main MCU
/dev/ttyUSB1 -> Nozzle MCU
/dev/ttyUSB2 -> RS-485 / CFS / closed-loop
```

Cartographer is no longer targeted as a fourth multiplexed T113 channel. The preferred final path is **direct USB to the CM5**, with the official [Cartographer3D plugin](https://github.com/Cartographer3D/cartographer3d-plugin) ([K2-OpenHost guide](https://github.com/MzTechnology97/K2-OpenHost/blob/main/docs/en/CARTOGRAPHER.md)).

## Repository map

- **K2-OpenHost** — canonical architecture, test evidence and roadmap.
- **kalico-k2pro:k2-pro-openhost** — integrated CM5 Kalico runtime tree.
- **[Cartographer3D plugin](https://github.com/Cartographer3D/cartographer3d-plugin)** (official) — Cartographer on Kalico/K2, used unchanged; the former K2-OpenHost fork was retired.
- **this branch** — versioned Jacobean K2 extra/patch history and K2 Pro/OpenHost compatibility source.

## Documentation

- [K2-OpenHost branch notes](K2-OPENHOST.md)
- [Documentation context](docs/index.md)
- [OpenHost integration notes](docs/openhost.md)
- [Validated patchset](patches/k2-openhost/README.md)

The remaining inherited `docs/` pages originate from Jacob's K2 Plus full-firmware project and are retained as attributed upstream reference material. They should not be treated as the current CM5/OpenHost installation procedure unless explicitly updated for this branch.

## Credits

- **Jacob10383 / Jacobean** — original `k2-plus-custom-firmware`, K2 extras and related Kalico work.
- **KalicoCrew/kalico** and contributors.
- **Klipper3d/klipper** and contributors.
- **CrealityOfficial** public K2 Klipper sources.
- Additional K2/CFS references are documented in `MzTechnology97/K2-OpenHost`.

This is an independent community project and is not affiliated with Creality.