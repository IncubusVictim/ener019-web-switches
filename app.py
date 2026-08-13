from flask import Flask, render_template, jsonify, request, send_from_directory
import requests
import re
import threading
import time

__author__ = "Incubus Victim"
__credits__ = ["Incubus Victim"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Incubus Victim"

app = Flask(__name__)

# ============ CONFIGURE THESE ============
DEVICE_IP   = "192.168.1.92"    # ← IP of your ENER019
PASSWORD    = "1"               # ← web password (default is usually 1)
icons = {
    "socket1": {
        "name": "Socket 1",
    },
    "socket2": {
        "name": "Socket 2",
    },
    "socket3": {
        "name": "Socket 3",
    },
    "socket4": {
        "name": "Socket 4",
    }
}
# ========================================

BASE_URL = f"http://{DEVICE_IP}"
lock = threading.Lock()

def login():
    """Login and return True if successful"""
    try:
        r = requests.post(f"{BASE_URL}/login.html",
                          data={"pw": PASSWORD},
                          timeout=5)
        return "Status" in r.text or "Log Out" in r.text
    except Exception as e:
        print("Login error:", e)
        return False

def logout():
    try:
        requests.get(f"{BASE_URL}/login.html", timeout=3)
    except:
        pass

def get_states():
    """Return list of 4 booleans [socket1, socket2, socket3, socket4]"""
    with lock:
        if not login():
            return None
        try:
            r = requests.get(f"{BASE_URL}/energenie.html", timeout=5)
            # look for: var sockstates = [1,0,1,1];
            m = re.search(r"var\s+sockstates\s*=\s*\[([01]),\s*([01]),\s*([01]),\s*([01])\]", r.text)
            if m:
                states = [bool(int(m.group(i))) for i in range(1, 5)]
            else:
                # fallback – some firmware variants
                states = [False, False, False, False]
            return states
        except Exception as e:
            print("Status error:", e)
            return None
        finally:
            logout()

def set_socket(socket_id: int, on: bool):
    """socket_id = 1..4, on = True/False"""
    with lock:
        if not login():
            return False
        try:
            data = {f"cte{socket_id}": 1 if on else 0}
            r = requests.post(BASE_URL + "/", data=data, timeout=5)
            return r.status_code == 200
        except Exception as e:
            print("Switch error:", e)
            return False
        finally:
            logout()

# ---------- Routes ----------

@app.route("/")
def index():
    return render_template("index.html", icons=icons)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route("/api/status")
def api_status():
    states = get_states()
    if states is None:
        return jsonify({"ok": False, "error": "Could not reach device"}), 500
    return jsonify({
        "ok": True,
        "switches": {
            "1": states[0],
            "2": states[1],
            "3": states[2],
            "4": states[3]
        }
    })

@app.route("/api/switch", methods=["POST"])
def api_switch():
    data = request.get_json(force=True)
    try:
        sid = int(data["id"])
        on  = bool(data["state"])
        if not 1 <= sid <= 4:
            raise ValueError
    except:
        return jsonify({"ok": False, "error": "Invalid parameters"}), 400

    success = set_socket(sid, on)
    if success:
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Failed to switch"}), 500

if __name__ == "__main__":
    print(f"ENER019 control → http://0.0.0.0:5000  (device {DEVICE_IP})")
    app.run(host="0.0.0.0", port=5000, debug=False)