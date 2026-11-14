# Hardware / platform verification

Target development board: Libre Computer AML-S905X-CC (Le Potato), reportedly the 4 GiB variant. Confirm the exact board version, operating system, device tree, memory, power supply and available interfaces on the unit.

* A very small GPIO-attached LCD is present, but **controller, GPIO wiring, bus, logic voltage and resolution are unverified**.
* No real LCD driver is installed by default. Browser eyes are a software simulator.
* The original enclosure photo assets are retained in `images/`.
* A previous CNC console concept appears in the repository history.

Suggested inventory:

```bash
cat /etc/os-release
cat /proc/device-tree/model
free -h
lsusb
ls -l /dev/serial/by-id/ 2>/dev/null || true
```

Never feed unknown external voltages directly into SBC GPIO; validate voltage levels, bus termination, wiring and protective circuits. Keep CNC and 3D-printer critical control with their respective specialized controllers.
