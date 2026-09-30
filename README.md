# K2 Pro Custom Firmware — K2-OpenHost branch

This branch is part of the **[K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost)** project and is derived from **[Jacob10383/k2-plus-custom-firmware](https://github.com/Jacob10383/k2-plus-custom-firmware)**.

The original K2 custom-firmware stack and K2-specific extras were created by **Jacob10383/Jacobean**. This fork keeps that attribution visible and carries only the K2 Pro/OpenHost deltas validated during our hardware work.

## Branch purpose

`k2-openhost` is the **source-of-truth for the Jacobean K2 extras plus our compatibility/safety patches**. It is not the final standalone CM5 repository anymore: the integrated test target is now:

```text
MzTechnology97/kalico-k2pro
branch: k2-pro-openhost
```

The Kalico fork contains the K2 Pro baseline configuration and synchronizes the validated extras from this branch into `klippy/extras/`.

## Hardware-validated K2 Pro deltas

Current validated changes include:

- K2 Pro four-byte CFS `BOX_STATE` support in `extras/box_protocol.py`, while retaining the original Jacobean six-byte/event paths;
- protected CFS `observation_mode` in `extras/box.py`;
- a CFS-only read guard that leaves the shared `serial_485.py` transport available to other K2 RS-485 devices;
- reproducible unified patches and SHA-gated application tooling.

The real Jacobean `Box()` class completed observation polling through the full OpenHost path with **35 TX / 35 RX and zero transport errors**. A deliberate `0x0D` mutation was blocked before TX.

## Repository map

- **K2-OpenHost** — architecture, test evidence and roadmap.
- **kalico-k2pro:k2-pro-openhost** — integrated CM5 Kalico test tree.
- **this branch** — versioned Jacobean extras and K2 Pro/OpenHost patch history.

## Documentation

- [K2-OpenHost branch notes](K2-OPENHOST.md)
- [Documentation context](docs/index.md)
- [OpenHost integration notes](docs/openhost.md)
- [Validated patchset](patches/k2-openhost/README.md)

The remaining `docs/` pages originate from Jacob's K2 Plus full-firmware project and are retained as attributed upstream reference material. They should not be treated as the current CM5/OpenHost installation procedure unless explicitly updated for this branch.

## Credits

- **Jacob10383 / Jacobean** — original `k2-plus-custom-firmware`, K2 extras and related Kalico work.
- **KalicoCrew/kalico** and contributors.
- **Klipper3d/klipper** and contributors.
- **CrealityOfficial** public K2 Klipper sources.
- Additional K2/CFS references are documented in `MzTechnology97/K2-OpenHost`.

This is an independent community project and is not affiliated with Creality.