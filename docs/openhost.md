# K2-OpenHost integration notes

## Lineage and attribution

The K2-specific extras in this branch originate from **Jacob10383/Jacobean** and the upstream `k2-plus-custom-firmware` project. K2-OpenHost adds only the K2 Pro compatibility and safety changes documented below.

## Validated changes

### K2 Pro CFS state

The tested K2 Pro returns a valid four-byte steady payload for CFS `BOX_STATE`. The patched decoder accepts that representation and exposes `firmware_base`, `substatus` and `load_flag` without inventing absent fields. The original six-byte and asynchronous slot-event paths remain intact.

### CFS observation mode

`box.py` can be run with `observation_mode: True`. In that mode the Box/CFS stack is wrapped by a read-only proxy, operational Box/T commands and runout hooks are not registered, and the normal startup RFID-policy write is skipped.

The protection is intentionally scoped to Box/CFS rather than global `serial_485.py`, because the same RS-485 bus also carries other K2 devices.

### Hardware result

The real Jacobean `Box()` completed enumeration, live-state reads and internal polling through the CM5 -> USB gadget -> T113 -> RS-485 path. Final transport counters were 35 TX / 35 RX with all error counters at zero. A deliberate mutation function `0x0D` was blocked before it reached the serial TX path.

## Current destination

The extras from this branch are synchronized into:

```text
MzTechnology97/kalico-k2pro:k2-pro-openhost
```

That repository is the current integrated Kalico target for full CM5 observation-mode testing.

The canonical architecture/status documentation is maintained in `MzTechnology97/K2-OpenHost`.