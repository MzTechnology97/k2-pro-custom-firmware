# K2-OpenHost integration branch

This branch contains the K2-OpenHost compatibility work for running the Jacobean/Kalico CFS stack from an external CM5 connected to a Creality K2 Pro through the K2 USB gadget bridge.

## Recommended CM5 layout

Keep Kalico and the K2-specific overlay as two separate Git clones:

```text
/home/alfio/kalico
    -> Jacob10383/kalico

/home/alfio/k2-pro-custom-firmware
    -> MzTechnology97/k2-pro-custom-firmware, branch k2-openhost
```

Kalico remains the upstream motion/control host. This repository supplies the Jacobean K2-specific extras and the K2-OpenHost hardware-validated modifications.

Install or refresh the K2 extras into an existing Kalico clone with:

```sh
cd /home/alfio/k2-pro-custom-firmware
git switch k2-openhost
sh tools/install-to-kalico.sh /home/alfio/kalico
```

Preview the operation without changing Kalico:

```sh
sh tools/install-to-kalico.sh /home/alfio/kalico --dry-run
```

The installer reads `extras/manifest.json`, copies the complete Jacobean 6.18 K2 extras set into `kalico/klippy/extras/`, backs up any differing pre-existing destination file, verifies that `box.py` and `box_protocol.py` contain the validated K2-OpenHost changes, compiles every installed Python extra, and writes an installation receipt at:

```text
/home/alfio/kalico/.k2-openhost-install.txt
```

Backups are stored under:

```text
/home/alfio/kalico/.k2-openhost-backups/<timestamp>/
```

This means there is no need to fork Kalico only to carry the K2 extras. Kalico can be updated independently; after an update, rerun the overlay installer and review any backed-up destination files if upstream introduced a conflicting extra.

## Validated patchset

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

The branch already contains these changes directly in `extras/box_protocol.py` and `extras/box.py`; the `.patch` files are retained as a reproducible archive against the clean Jacob base.

The upstream-style shared `serial_485.py` transport is intentionally not patched, because the same RS-485 bus is also used by other K2 devices such as closed-loop motor controllers.

Automatic CFS load/unload is intentionally not enabled yet. The current K2 Pro four-byte steady state lacks the Jacobean six-byte `downstream_mask`, so loaded-path detection must be validated before mutating CFS operations are enabled.

The fork `main` branch is intended to remain suitable for following Jacob upstream; K2-OpenHost-specific work should remain isolated on this branch until explicitly promoted.
