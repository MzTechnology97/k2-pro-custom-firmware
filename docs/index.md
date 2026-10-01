# Documentation — K2 Pro / K2-OpenHost branch

This branch is derived from **Jacob10383/k2-plus-custom-firmware**. The original K2 Plus custom-firmware architecture, documentation and K2-specific extras remain attributed to **Jacob10383/Jacobean**.

## Start here for this fork

- [K2-OpenHost branch overview](../K2-OPENHOST.md)
- [OpenHost integration notes](openhost.md)
- [Validated patchset](../patches/k2-openhost/README.md)
- [Canonical K2-OpenHost project](https://github.com/MzTechnology97/K2-OpenHost)
- [Integrated Kalico fork](https://github.com/MzTechnology97/kalico-k2pro/tree/k2-pro-openhost)
- [Cartographer K2-OpenHost plugin](https://github.com/MzTechnology97/cartographer3d-plugin-k2openhost)

## Current project status

As of 2026-10-01, the integrated CM5/Kalico stack has progressed beyond observation-only tests and has validated real machine control on the K2 Pro, including full PRTouch homing, heater/PID tests, emergency heater shutdown, closed-loop/stall homing and a Klippain-ShakeTune resonance test.

The next major hardware milestone is Cartographer connected directly to the CM5 USB host, followed by a complete supervised print workflow.

## Upstream documentation retained here

The other pages in this directory come from the original K2 Plus full-firmware project. They remain useful technical references for Jacobean K2 behavior, but installation/setup/recovery pages describe the upstream full-firmware/T113-local workflow rather than the current CM5/OpenHost architecture.

Do not translate a K2 Plus geometry, pin, service-zone or protocol assumption directly to K2 Pro unless it has been validated or replaced by the real K2 Pro configuration.

For the current OpenHost machine paths, runtime configuration and test state, prefer the canonical `K2-OpenHost` repository and the active `kalico-k2pro:k2-pro-openhost` branch.