# ENER019 Control Panel

<div align="right">
<a href="https://buymeacoffee.com/incubusvictim" target="_blank"><img align="top" src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a> <img align="top" src="https://github.com/IncubusVictim/ener019-web-switches/blob/main/bmc_qr.png" width="100" />
</div>

<img align="middle" src="https://github.com/IncubusVictim/ener019-web-switches/blob/main/static/ener019.png" width="400" />

## Description
A clean, dark-themed web interface to control an **Energenie ENER019** 4-socket power strip over the local network.

The frontend is a simple responsive HTML page.

The backend is a small Python Flask application that talks to the device using its built-in web interface.

<b><I>NOTE: I've designed this to run on my Windows 11 server, but it should work out of the box on another platform. When I have time I will try it out on Linux.</i></b>

---

## Features

- Dark theme, mobile-friendly interface
- Four animated red/green toggles
- Live status loaded on page open
- Instant visual feedback when switching
- Automatic revert of the switch if the command fails
- Designed to run 24/7 on a server

---

## Requirements

- Windows
- Python 3.9 or newer
- Network access to the ENER019 device
- The ENER019 must be on the same local network

---

## Project Structure

```
ener019-control/
├── app.py                          # Flask backend
├── static/
│   └── ener019.png                 # Sample ENER019 image
│   └── socketdark-192.png          # Smaller icon
│   └── socketdark-512.png          # Larger icon
├── templates/
│   └── index.html                  # Dark-theme frontend
└── README.md                       # This file
```
---


## Installation

### 1. Install Python

---

- Download and install Python from https://www.python.org/  
**Important:** tick “Add Python to PATH” during installation.

---

### 2. Create project folder

```
mkdir C:\ener019-control
cd C:\ener019-control
```

Place app.py and the templates folder here.

### 3. Install dependencies
---

```
pip install flask requests
```

---

### 4. Running as a Windows Service
---

To make the site start automatically when the server boots (even if no one is logged in), install it as a Windows service using NSSM.

#### 1. Download NSSM
---

- Go to https://nssm.cc/download
- Download the latest release
- Extract it to a permanent location, e.g. C:\Tools\nssm\
---

#### 2. Install the service
---

Open an Administrator Command Prompt or PowerShell:

```
cd C:\Tools\nssm\win64
.\nssm.exe install ENER019
```

A configuration window will appear. Fill in the fields as follows:

| Tab | Field | Value |
|-----|-------|-------|
| Application | Path | Full path to ```python.exe``` |
| | Startup directory | ```C:\ener019-control``` |
| | Arguments | ```app.py``` |
| Details | Display name | ```ENER019 Control``` |
| | Description | Web interface for Energenie ENER019 |
| Log on | | Local System account (default is fine) |

Click Install service.

---

#### 3. Start the service
---

```
.\nssm.exe start ENER019
```

The service will now start automatically every time Windows boots.
Useful NSSM commands

```
nssm start ENER019          # Start
nssm stop ENER019           # Stop
nssm restart ENER019        # Restart
nssm status ENER019         # Check status
nssm edit ENER019           # Re-open the configuration GUI
nssm remove ENER019 confirm # Completely remove the service
```
---
