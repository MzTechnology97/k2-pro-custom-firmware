# K2-OpenHost integration notes

## Upstream lineage

This fork originates from **Jacob10383/k2-plus-custom-firmware**. Jacob/Jacobean remains the original author of the custom-firmware stack and K2-specific extras carried here.

## K2 Pro validated deltas

The `k2-openhost` branch records the compatibility/safety differences validated on a real K2 Pro:

1. support for the K2 Pro steady CFS `BOX_STATE` representation with a four-byte payload while keeping the existing Jacobean six-byte/event decoders;
2. an `observation_mode` in `box.py` that wraps only the CFS Box stack with a read-only guard;
3. no automatic RFID-policy write, operational `BOX_*` commands, material `Tn` commands or runout observer while observation mode is active.

The shared `serial_485.py` transport is intentionally not globally restricted because the same K2 RS-485 path is also used by closed-loop/belt devices.

## Hardware milestone

The real Jacobean `Box()` class has completed K2-OpenHost observation polling through the full CM5 -> USB gadget -> T113 -> RS-485 path with 35 transmitted and 35 received frames and zero transport errors. A deliberate CFS mutation request (`0x0D`) was blocked before transmission.

## Current integration target

The validated extras from this repository are synchronized into:

```text
MzTechnology97/kalico-k2pro
branch: k2-pro-openhost
```

That Kalico fork is the current CM5 integration target. This repository remains the clean source/history for the Jacobean K2 extras and K2-OpenHost patchset.

For current status and safety boundaries, see the canonical **MzTechnology97/K2-OpenHost** repository.