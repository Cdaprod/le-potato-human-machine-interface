# My recommendation: Install a lightweight Linux desktop, then run LinuxCNC on top of it.

Looking at your photos, you've already built something that could make an excellent **dedicated CNC control console**.

You've got:
- A Le Potato single-board computer (exact model needs confirmation).
- A built-in display.
- A custom 3D-printed enclosure.
- Aluminum T-slot extrusion framing.
- USB 3.0 ports, Ethernet, and other front-panel connections.
- An enclosure that could accommodate additional electronics.

And you're already developing an ESP32-S3 wireless MPG pendant, an ESP32-C3 ESP-NOW bridge, and a GRBL-based Doesbot controller.

**I wouldn't immediately flash a dedicated LinuxCNC image.** Your existing GRBL hardware changes which software architecture makes sense.

## 1. Understand the difference

| Configuration | Purpose | My recommendation |
|---|---|---|
| Ubuntu Server (headless) | SSH, services, containers | Fine for a remote controller, but doesn't take advantage of your screen |
| Ubuntu Desktop | General-purpose graphical Linux | Good, provided there's a supported image |
| Debian + lightweight desktop | Efficient graphical Linux | **My preferred starting point** |
| LinuxCNC | Full CNC machine-control platform | Consider for a future controller upgrade |
| CNCjs | Browser-based GRBL control | **Best immediate match for your Doesbot** |
| bCNC | Python-based GRBL sender | Excellent alternative |

### Why not immediately install LinuxCNC?

Your Doesbot already has a GRBL firmware controller responsible for generating step pulses, handling motion, and controlling machine outputs.

LinuxCNC is designed to take over that motion-control responsibility.

Running LinuxCNC as the primary controller generally means replacing or bypassing the GRBL motion-control architecture.

You don't need to do that to get a sophisticated CNC control system.

Instead, your Le Potato can become the **host computer** responsible for:

1. Displaying your CNC interface.
2. Sending G-code to GRBL.
3. Monitoring machine position and status.
4. Managing jobs and files.
5. Providing network access.
6. Integrating your ESP32-based pendant ecosystem.

The Doesbot continues performing the actual motion control.

That also means Linux on the Le Potato doesn't need to satisfy LinuxCNC's stringent real-time motion-control requirements.

## 2. Which operating system should you install?

I checked the currently available images.

For the original **Libre Computer Le Potato (AML-S905X-CC)**, there are several options.

| Operating system | Desktop | Suitability |
|---|---|---|
| Armbian + XFCE | Yes | ⭐ My first choice |
| Debian 13 + XFCE | Install separately | Excellent |
| Ubuntu 24.04 | Optional | Good |
| Ubuntu Server | No | Useful for headless operation |
| LinuxCNC image | Specialized | Not recommended for this configuration |

Armbian currently lists a stable XFCE desktop image for Le Potato. That makes it particularly attractive because you won't have to manually configure a desktop environment.

**Download:** [oai_citation:0‡armbian.com](https://armbian.com/boards/lepotato?utm_source=chatgpt.com)

Alternatively, Libre Computer provides board-specific Debian images and installation instructions:

[oai_citation:1‡hub.libre.computer](https://hub.libre.computer/t/debian-12-bookworm-and-11-bullseye-for-libre-computer-boards/230?utm_source=chatgpt.com)

One important consideration: the board may have only 1–2 GB of RAM. XFCE is substantially more appropriate than a full GNOME desktop for that hardware.

## 3. What I'd build with your existing hardware

Your system could look like this:

```text
             CNC CONTROL CONSOLE
          Le Potato + Touch Display
         Debian/Armbian + XFCE
                     |
       ┌─────────────┴─────────────┐
       |                           |
    CNCjs UI                  Diagnostics UI
       |                           |
       |                    ESP32-S3 Pendant
       |                    ESP32-C3 Bridge
       |                    Serial Monitoring
       |
    USB Serial
       |
  Doesbot GRBL Controller
       |
   Stepper Drivers
       |
   X / Y / Z / A
```

The ESP32-C3 can remain connected to the Doesbot's UART header for your wireless pendant, provided we verify that concurrent serial communication is supported. We should not assume USB and accessory UART can safely accept commands simultaneously.

Your Le Potato would host the main control interface, and you could access that same interface from your iPhone, MacBook, or another computer.

**CNCjs:** [oai_citation:2‡github.com](https://github.com/cncjs/cncjs?utm_source=chatgpt.com)

One additional advantage is that your existing custom display enclosure can become a dedicated CNC operator station rather than a general-purpose desktop.

## 4. Before flashing anything, inspect the existing installation

Because you already have Ubuntu installed, we might not need to reflash at all.

SSH into the Le Potato and execute:

`/home/david/scripts/system-inventory.sh`

```bash
#!/usr/bin/env bash

echo "=== OPERATING SYSTEM ==="
cat /etc/os-release

echo "=== KERNEL ==="
uname -a

echo "=== BOARD ==="
cat /proc/device-tree/model 2>/dev/null
echo

echo "=== CPU ==="
lscpu

echo "=== MEMORY ==="
free -h

echo "=== STORAGE ==="
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS

echo "=== DISPLAY ==="
ls /sys/class/drm/

echo "=== DESKTOP ==="
systemctl get-default

echo "=== USB ==="
lsusb
```

You can run those commands individually; there's no need to create the script first.

If the installed Ubuntu release is still supported and its board-specific kernel works correctly, we could simply add XFCE:

```bash
sudo apt update
sudo apt install xfce4 xfce4-goodies lightdm
sudo systemctl set-default graphical.target
sudo reboot
```

That avoids unnecessarily disturbing your existing installation. Confirm sufficient free storage before installing the desktop.

If Ubuntu is outdated, I'd flash a new Armbian XFCE image to a **separate microSD card**, preserving the original installation as a fallback.

---

## 5. What about LinuxCNC?

I wouldn't abandon LinuxCNC as an option.

It's particularly interesting for your longer-term CNC plans because of its HAL architecture, programmable machine logic, and support for advanced motion control.

However, LinuxCNC requires a suitable real-time kernel when directly controlling machinery. Its official ARM64 packages do not automatically make every ARM board suitable for real-time CNC control. [oai_citation:3‡LinuxCNC](https://linuxcnc.org/downloads/?utm_source=chatgpt.com)

You could install LinuxCNC for simulation and experimentation without replacing GRBL.

For actual machine control, we'd need to validate the hardware, real-time performance, and motion-control interfaces first.

---

## 6. Two things I noticed in your photos

**First:** The aluminum extrusion housing is already well suited to a modular machine console. You have room to expand the electronics and improve cable management.

**Second:** Your display appears connected through HDMI, with a separate controller board underneath the Le Potato. Before selecting an operating system, we should identify that display controller and establish whether the screen supports touch input.

If it's an HDMI display with USB touch, getting it working under XFCE may be straightforward.

If it's an HDMI display with a separate I²C touch controller, we'll need to check driver compatibility.

### Here's what I want to establish next:

1. **Is your display a touchscreen?** Have you previously used touch input on it?
2. **Can you still SSH into the Le Potato?** If so, run the inventory commands above.

Once we establish those two things, we can choose the correct OS and configure this as a dedicated CNC console without unnecessarily reflashing hardware that may already work.