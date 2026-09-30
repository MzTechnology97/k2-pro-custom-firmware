<!-- K2-OPENHOST-FORK-CONTEXT -->
> **Fork / upstream context:** this page is preserved from **Jacob10383/Jacobean's `k2-plus-custom-firmware`** documentation and remains credited to the original project. It may describe the original K2 Plus full-firmware/T113-local workflow. For the current **K2 Pro / K2-OpenHost** architecture, start from [`docs/index.md`](index.md), [`docs/openhost.md`](openhost.md), and [MzTechnology97/K2-OpenHost](https://github.com/MzTechnology97/K2-OpenHost). K2 Plus values or procedures are not assumed to apply unchanged to K2 Pro.

# Install

Unload any filament from the printhead before starting.

SSH into the printer and run:

```sh
python3 -c "import urllib.request; exec(urllib.request.urlopen('https://firmware.jacobean.xyz/install.py').read(), {'__name__':'__main__'})"
```

Power cycle the printer when instructed. If SSH drops during the final archive
step before the completion message appears, the install is complete; power
cycle the printer.

## First boot

After the printer starts again, connect it to the network:

- Ethernet: nothing else is required.
- Wi-Fi: use the printer screen only far enough to join the network.

Then SSH into the printer and run:

```sh
bootstrap
```

When bootstrap finishes, Fluidd is available on port `4408` and Mainsail on
port `4409` at the printer's IP address.

The default configuration expects the 5.8 mm Y-endstop spacer and the
Cartographer mount used by K2 Improvements.

## Before your first print

1. [Calibrate the printer](calibration.md). Follow the path that applies to
   your probe mode.
2. [Set up OrcaSlicer](setup.md) after calibration.
3. Read [CFS and RFID](cfs.md) to find the Fluidd CFS widget, its controls,
   and RFID setup.
