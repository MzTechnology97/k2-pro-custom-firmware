# K2-OpenHost integration notes

Updated: **2026-10-01**.

## Lineage and attribution

The K2-specific extras in this branch originate from **Jacob10383/Jacobean** and the upstream `k2-plus-custom-firmware` project. K2-OpenHost adds only the K2 Pro compatibility, safety and external-host integration changes documented here.

## Validated changes

### K2 Pro CFS state

The tested K2 Pro returns a valid four-byte steady payload for CFS `BOX_STATE`. The patched decoder accepts that representation and exposes the fields actually present without inventing absent data. The original six-byte and asynchronous slot-event paths remain intact.

### CFS observation mode

`box.py` can run with `observation_mode: True`. In that mode the Box/CFS stack is wrapped by a read-only proxy, operational Box/T commands and runout hooks are not registered, and the normal startup RFID-policy write is skipped.

The protection is intentionally scoped to Box/CFS rather than global `serial_485.py`, because the same RS-485 bus also carries the K2 closed-loop motor controllers and other devices.

### CFS hardware result

The real Jacobean `Box()` completed enumeration, live-state reads and internal polling through the CM5 -> USB gadget -> T113 -> RS-485 path. A reference run ended at 35 TX / 35 RX with all transport error counters at zero. A deliberate mutation function `0x0D` was blocked before it reached serial TX.

### External-host motor-control result

The integrated Kalico branch now uses the K2 Pro closed-loop motor topology on the same RS-485 path. Hardware validation includes:

- X/Y controller discovery and communication;
- startup retry recovery when the CM5 becomes ready before the motor controllers;
- normal CoreXY motion;
- X/Y sensorless/stall homing;
- correct Z direction.

A duplicate GS2 bridge discovered during an experimental Cartographer multiplexing test caused RS-485 failures. Returning the transport to a single `ttyGS2 <-> ttyS5` owner restored normal motor-control operation. This is now a documented transport requirement.

### Full machine-control baseline

The real K2 Pro has also completed from the external CM5/Kalico host:

- full homing with the stock PRTouch stack;
- bed, nozzle and chamber heater tests;
- PID tuning;
- emergency shutdown with active heater loads removed;
- a Klippain-ShakeTune resonance measurement.

This establishes a known-good non-Cartographer machine-control baseline.

## Cartographer direction

Cartographer is no longer targeted as a fourth multiplexed T113 gadget channel. The experimental MUX/DEMUX path successfully carried live Cartographer data but reset/re-enumeration and PTY lifecycle added unnecessary complexity.

The preferred final path is direct USB from Cartographer to the CM5, maintained in:

```text
MzTechnology97/cartographer3d-plugin-k2openhost
```

That plugin also carries `register_as_probe` support for standalone Cartographer mode and optional future mixed PRTouch + Cartographer operation.

## Current destination

The K2 extras from this branch are synchronized into:

```text
MzTechnology97/kalico-k2pro:k2-pro-openhost
```

That repository is the current integrated Kalico runtime target. The canonical architecture/status documentation is maintained in `MzTechnology97/K2-OpenHost`.