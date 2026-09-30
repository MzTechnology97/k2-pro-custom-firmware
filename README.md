# K2 Pro Custom Firmware / K2-OpenHost compatibility fork

This repository is a fork of **[Jacob10383/k2-plus-custom-firmware](https://github.com/Jacob10383/k2-plus-custom-firmware)**.

The original K2 custom-firmware stack, its architecture and the K2-specific extras were created by **Jacob10383/Jacobean**. Those upstream authorship references are intentionally preserved throughout this fork.

## Why this fork exists

`MzTechnology97/k2-pro-custom-firmware` is used by the **[K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost)** project to keep an auditable K2 Pro compatibility layer on top of Jacob's public K2 work.

The active development branch is:

```text
k2-openhost
```

That branch contains the Jacobean K2 extras plus the small K2 Pro/OpenHost deltas that have been validated on real hardware. It is **not** intended to erase or replace the original K2 Plus project history.

## Current role in K2-OpenHost

This repository is the versioned source for:

- Jacobean K2-specific Kalico extras;
- the K2 Pro four-byte CFS `BOX_STATE` compatibility change;
- the protected CFS `observation_mode` used during OpenHost validation;
- reproducible patch files and SHA-gated patch tooling;
- the source synchronized into `MzTechnology97/kalico-k2pro:k2-pro-openhost`.

The final CM5 test target is now the integrated fork:

- **[MzTechnology97/kalico-k2pro](https://github.com/MzTechnology97/kalico-k2pro)**, branch `k2-pro-openhost`.

The canonical architecture and hardware-validation record remains:

- **[MzTechnology97/K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost)**.

## Upstream K2 Plus documentation

The `docs/` directory on `main` originates from Jacob's K2 Plus custom-firmware project. It is preserved as upstream reference material and attribution. Some pages therefore describe a full K2 Plus firmware replacement and T113-local installation flow that is **not** the current K2 Pro/OpenHost deployment path.

Start with [docs/index.md](docs/index.md) for the fork context before using those guides.

## Branch policy

- `main` stays close to the Jacob-derived release base and carries only fork/documentation context.
- `k2-openhost` contains the K2 Pro/OpenHost compatibility work and validated extra sources.

## Credits

Primary upstream projects/authors:

- **Jacob10383 / Jacobean** — original `k2-plus-custom-firmware`, K2 extras and related Kalico work.
- **KalicoCrew/kalico** — Kalico project and contributors.
- **Klipper3d/klipper** — Klipper project and contributors.
- **CrealityOfficial** — public K2 Klipper sources used by the wider community.

Additional reverse-engineering and K2 project references are listed in the K2-OpenHost documentation.

This fork is an independent community project and is not affiliated with Creality.