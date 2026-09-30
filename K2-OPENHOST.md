# K2-OpenHost integration branch

This branch contains the K2-OpenHost compatibility work for running the Jacobean/Kalico CFS stack from an external CM5 connected to a Creality K2 Pro through the K2 USB gadget bridge.

The validated patchset is stored under:

```text
patches/k2-openhost/
```

Start with:

```text
patches/k2-openhost/README.md
```

and apply the hardware-validated changes with:

```sh
sh patches/k2-openhost/apply.sh
```

The current patchset contains:

1. K2 Pro four-byte CFS `BOX_STATE` compatibility for `extras/box_protocol.py`;
2. a protected CFS `observation_mode` for `extras/box.py`.

The upstream-style shared `serial_485.py` transport is intentionally not patched, because the same RS-485 bus is also used by other K2 devices such as closed-loop motor controllers.

Automatic CFS load/unload is intentionally not enabled yet. The current K2 Pro four-byte steady state lacks the Jacobean six-byte `downstream_mask`, so loaded-path detection must be validated before mutating CFS operations are enabled.

The fork `main` branch is intended to remain suitable for following Jacob upstream; K2-OpenHost-specific work should remain isolated on this branch until explicitly promoted.
