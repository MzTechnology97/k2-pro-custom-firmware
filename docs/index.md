# Documentation context — K2 Pro / K2-OpenHost fork

This repository is derived from **Jacob10383/k2-plus-custom-firmware**. The original firmware stack and documentation were authored by **Jacob10383/Jacobean** for the K2 Plus and remain credited as such.

## Current purpose of this fork

For K2-OpenHost, this repository is primarily the **source and history of K2-specific extras and compatibility patches**, not the final CM5 installation target.

Use:

- [K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost) for architecture, hardware validation and roadmap;
- [kalico-k2pro](https://github.com/MzTechnology97/kalico-k2pro), branch `k2-pro-openhost`, for the integrated Kalico tree used by the CM5 tests;
- this repository's `k2-openhost` branch for the validated Jacobean extra sources and patch history.

See [OpenHost integration notes](openhost.md).

## About the original documentation below

The following pages are preserved from the upstream K2 Plus full-firmware project. They are useful reference material, but pages such as installation/setup/recovery may describe the **original K2 Plus T113-local firmware replacement workflow**, not the current K2 Pro external-host/OpenHost procedure.

- [Installation](install.md)
- [Setup](setup.md)
- [Calibration](calibration.md)
- [CFS](cfs.md)
- [Configuration reference](config-reference.md)
- [Command reference](command-reference.md)
- [Error explanations](error-explanation.md)
- [RFID](rfid.md)
- [Updates and recovery](updates-recovery.md)

Do not silently assume that a K2 Plus mechanical/configuration value applies to K2 Pro. K2-OpenHost marks hardware-tested K2 Pro results separately from upstream-derived information.