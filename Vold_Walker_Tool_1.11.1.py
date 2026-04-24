import time
import random
import os
import sys
import threading
from datetime import datetime
import getpass
import subprocess
import platform
import subprocess
import platform
import re

MENU7_ADMIN_PASSWORD = "admin1234"

# ===== SOCIAL LAB GLOBAL =====
SOCIAL_PLATFORMS = [
    "Facebook", "TikTok", "Instagram", "Zalo", "Telegram",
    "Discord", "Twitter(X)", "Snapchat", "WhatsApp", "Line",
    "WeChat", "YouTube", "Reddit", "LinkedIn", "Pinterest"
]

PERMISSIONS_7 = {
    "user": ["scan", "risk", "report", "help", "exit"],
    "admin": ["scan", "atk", "dep", "risk", "report", "help", "exit"]
}

SOCIAL_RULES = [
    {
        "name": "Weak password",
        "risk": "HIGH",
        "check": lambda d: d["password"] == "WEAK"
    },
    {
        "name": "2FA disabled",
        "risk": "MEDIUM",
        "check": lambda d: d["2fa"] is False
    },
    {
        "name": "Public profile",
        "risk": "LOW",
        "check": lambda d: d["public"] is True
    }
]
# ======================Rules server================
SERVER_STATE = {
    "target": None,
    "role": None,
    "steps": {
        "recon": False,
        "scan": False,
        "enum": False,
        "config": False,
        "escalate": False,
        "persist": False,
        "cleanup": False
    },
    "findings": [],
    "risk": "LOW",
    "timeline": []
}


MENU_PASSWORD = "admin123"   # đổi tùy bạn
MAX_ATTEMPTS = 3

# ================= GLOBAL =================
STATE = "INIT"
              #thêm
RISK_SCORE = {
    "LOW": 1,
    "INFO": 1,
    "MEDIUM": 2,
    "HIGH": 3
}

# =========== Risk score =====================
def role_level(r):
    return {"guest": 1, "analyst": 2, "admin": 3}.get(r, 1)

                   #rules
RULES = [
    {
        "name": "Open Network",
        "check": lambda n: n["security"] == "OPEN",
        "risk": "HIGH",
        "note": "Open network – traffic can be intercepted"
    },
    {
        "name": "Weak WPA",
        "check": lambda n: n["security"] == "WPA2",
        "risk": "MEDIUM",
        "note": "WPA2 detected – consider WPA3 upgrade"
    },
    {
        "name": "Strong Encryption",
        "check": lambda n: n["security"] == "WPA3",
        "risk": "LOW",
        "note": "Modern encryption standard"
    },
    {
        "name": "Strong Signal",
        "check": lambda n: n["signal"] > -50,
        "risk": "INFO",
        "note": "Strong signal – network is nearby"
    }
]

MINER = {
    "coin": "XMR-SIM",
    "hashrate": 0.0,
    "difficulty": 120000,
    "latency": 0,
    "accepted": 0,
    "rejected": 0,
    "total": 0.0,
    "usd_rate": 165.0,
    "uptime": 0
}

# ===== COMMAND MODE CONFIG =====
USER_ROLE = "analyst"   # guest / analyst / admin

ALIASES = {
    "s": "scan",
    "ls": "list",
    "q": "exit",
    "ra": "risk all",
}

PERMISSIONS = {
    "scan": "guest",
    "list": "guest",
    "select": "analyst",
    "risk all": "analyst",
    "config": "admin",
}
#========Banner Command mode=====
def command_banner():
    print(r"""
============================================_  ___  __  _  _ ___ ___ ====================
=                                          /_\ |  \/  || || |   |   |                   =
=                                         / _ \| |\/| || || | | | | |                   =
=  ██████╗ ███╗   ███╗██████╗ ███╗   ██╗ /_/ \_\_|  |_||_||_|___|___|                   =
=  ██╔══██╗████╗ ████║██╔══██╗████╗  ██║      ◢◤  W I F I   A U D I T   S Y S T E M  ◢◤
=  ██║  ██║██╔████╔██║██║  ██║██╔██╗ ██║      -------------------------------------------
=  ██║  ██║██║╚██╔╝██║██║  ██║██║╚██╗██║                                                =
=  ██████╔╝██║ ╚═╝ ██║██████╔╝██║ ╚████║                                                =
=  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═══╝                             by Dang Khoa       =
=========================================================================================
   WIFI AUDIT INTERACTIVE COMMAND SHELL                                                 =
=========================================================================================
Type 'help' to list commands
""")

def lab_banner():
    clear()
    print(r"""
==================================================================================
██╗   ██╗ ██████╗ ██╗██████╗     ██╗    ██╗ █████╗ ██╗     ██╗  ██╗███████╗██████╗ 
██║   ██║██╔═══██╗██║██╔══██╗    ██║    ██║██╔══██╗██║     ██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██║   ██║██║██║  ██║    ██║ █╗ ██║███████║██║     █████╔╝ █████╗  ██████╔╝
╚██╗ ██╔╝██║   ██║██║██║  ██║    ██║███╗██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
 ╚████╔╝ ╚██████╔╝██║██████╔╝    ╚███╔███╔╝██║  ██║███████╗██║  ██╗███████╗██║  ██║
  ╚═══╝   ╚═════╝ ╚═╝╚═════╝      ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
══════════════════════════════════════════════════════════════════════════════════
        ⚡ VOID WALKER FRAMEWORK ⚡
        ▸ Scan • Exploit • Automate • Dominate
        ▸ Author : Cru21n
        ▸ Mode   : Interactive Terminal
══════════════════════════════════════════════════════════════════════════════════
                                                                                  by Dang Khoa
""")


def server_lab_banner():
    clear()
    print(r"""
███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

        S E R V E R   S E C U R I T Y   L A B
              ( DEMO / SIMULATION )
""")
#==========Prompt Server============
def server_prompt(target=None, role=None):
    base = "SERVER-LAB"
    if target:
        base += f"({target})"
    if role:
        base += f"[{role}]"
    return base + "> "

#=========Processs============
def progress_1_to_100(title="Processing"):
    print(f"\n{title}")
    for i in range(1, 101):
        print(f"\rProgress: {i}%", end="")
        time.sleep(0.03)
    print("\nDone.\n")

def lab_prompt(section, target=None, role=None):
    base = f"LAB:{section}"
    if target:
        base += f"({target})"
    if role:
        base += f"[{role}]"
    return base + "> "

#============Prompt==================
def build_prompt(state, target=None):
    if target:
        return f"wifi@audit:{state}({target})> "
    return f"wifi@audit:{state}> "

#===========Help Command Mode===========
def help_command(cmd=None):
    helps = {
        "scan": "Scan real Wi-Fi networks",
        "list": "List parsed networks",
        "select": "Select SSID and run rule engine",
        "risk all": "Show overall risk summary",
        "exit": "Exit command mode"
    }

    if cmd:
        print(f"{cmd}: {helps.get(cmd, 'No help available')}")
    else:
        print("\nAvailable commands:")
        for k in helps:
            print(f" - {k}")

def simple_prompt(module, info=None):
    if info:
        return f"{module}({info})> "
    return f"{module}> "

# ================= UI =================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(r"""
======================================================================================    
=██╗   ██╗ ██████╗ ██╗██████╗     ██╗    ██╗ █████╗ ██╗     ██╗  ██╗███████╗██████╗  =
=██║   ██║██╔═══██╗██║██╔══██╗    ██║    ██║██╔══██╗██║     ██║ ██╔╝██╔════╝██╔══██╗ =
=██║   ██║██║   ██║██║██║  ██║    ██║ █╗ ██║███████║██║     █████╔╝ █████╗  ██████╔╝ =
=╚██╗ ██╔╝██║   ██║██║██║  ██║    ██║███╗██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗ =
= ╚████╔╝ ╚██████╔╝██║██████╔╝    ╚███╔███╔╝██║  ██║███████╗██║  ██╗███████╗██║  ██║ ==============
=  ╚═══╝   ╚═════╝ ╚═╝╚═════╝      ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ by Dang Khoa =
 Ultimate Audit & Simulation Framework ============================================================
""")
def password_gate():
    attempts = 0
    delay = 1
    while attempts < MAX_ATTEMPTS:
        banner()
        print("=== SECURED ACCESS ===")
        pwd = getpass.getpass("Enter menu password: ")
        if pwd == MENU_PASSWORD:
            print("[✓] Access granted")
            time.sleep(1)
            return True
        else:
            attempts += 1
            print(f"[!] Invalid ({attempts}/{MAX_ATTEMPTS})")
            time.sleep(delay)
            delay += 2
    sys.exit()

# ================= PROGRESS =================
def advanced_progress(title, min_delay=0.01, max_delay=0.06):
    start = time.time()
    for i in range(1, 101):
        elapsed = time.time() - start
        eta = int((elapsed / i) * (100 - i))
        bar = "█" * (i // 4) + "-" * (25 - i // 4)
        print(f"\r[{title}] [{bar}] {i:3d}% | ETA ~{eta}s", end="")
        time.sleep(random.uniform(min_delay, max_delay))
    print()

def staged_progress():
    stages = [
        (1, 15,  "Initializing buffers"),
        (16, 30, "Allocating worker threads"),
        (31, 50, "Binding system resources"),
        (51, 70, "Stabilizing pipeline"),
        (71, 85, "Optimizing execution"),
        (86, 100,"Final integrity checks")
    ]
    start = time.time()
    for a, b, label in stages:
        for i in range(a, b + 1):
            elapsed = time.time() - start
            eta = int((elapsed / i) * (100 - i)) if i > 0 else 0
            print(f"\r[{label}] {i:3d}% | ETA ~{eta}s", end="")
            time.sleep(random.uniform(0.03, 0.06))
    print()

#============Server lab=================
SERVER_RULES = [
    {"name": "Outdated services", "risk": "MEDIUM"},
    {"name": "Weak SSH policy", "risk": "HIGH"},
    {"name": "Directory listing enabled", "risk": "LOW"},
    {"name": "Weak sudoers config", "risk": "HIGH"},
]

def server_risk_engine(findings):
    score = 0
    hits = 0
    for f in findings:
        for r in SERVER_RULES:
            if r["name"] in f:
                hits += 1
                score += {"LOW":1,"MEDIUM":2,"HIGH":3}[r["risk"]]
    if hits == 0:
        return "LOW"
    avg = round(score / hits)
    return {1:"LOW",2:"MEDIUM",3:"HIGH"}.get(avg,"LOW")

def log_step(step, note):
    SERVER_STATE["timeline"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "step": step,
        "note": note
    })

def server_prompt(target=None, role=None, risk=None):
    base = "SERVER-LAB"
    if target:
        base += f"({target})"
    if role:
        base += f"[{role}]"
    if risk:
        base += f"<{risk}>"
    return base + "> "

def server_lab():
    server_lab_banner()

    role = input("Enter role (admin/user) > ").lower()
    if role != "admin":
        print("Access denied. Admin permission required.")
        time.sleep(2)
        return

    target = input("Target server (IP / hostname - demo) > ").strip()
    if not target:
        target = "demo-server"

    print(f"\nAdmin access granted for {target}\n")

    while True:
        cmd = input(server_prompt(target, role)).lower().strip()

        if cmd in ("exit", "back"):
            return

        elif cmd == "help":
            print("""
SERVER LAB COMMANDS
-------------------
recon        - basic reconnaissance
scan         - service scan simulation
config       - weak config check
escalate     - privilege escalation (demo)
risk         - overall risk assessment
exit         - return to lab
""")

        elif cmd == "recon":
            progress_1_to_100("Reconnaissance Phase")
            print("Open ports discovered: 22, 80, 443")
            print("OS fingerprint: Linux (simulated)")

        elif cmd == "scan":
            progress_1_to_100("Service Scanning")
            print("SSH: outdated version (demo)")
            print("HTTP: directory listing enabled (demo)")

        elif cmd == "config":
            progress_1_to_100("Configuration Audit")
            print("Weak sudo policy detected")
            print("Default credentials risk (demo)")

        elif cmd == "escalate":
            progress_1_to_100("Privilege Escalation Simulation")
            print("Privilege escalation path identified (simulation only)")

        elif cmd == "risk":
            print("OVERALL SERVER RISK: HIGH")
            print("Reason: weak config + outdated services")

        else:
            print("Unknown command. Type 'help'")
            
# =================Server lab pro===============
def server_lab():
    server_lab_banner()

    role = input("Enter role (admin/user) > ").lower()
    if role != "admin":
        print("Access denied. Admin permission required.")
        time.sleep(2)
        return

    target = input("Target server (demo) > ").strip() or "demo-server"

    # reset state
    SERVER_STATE["target"] = target
    SERVER_STATE["role"] = role
    for k in SERVER_STATE["steps"]:
        SERVER_STATE["steps"][k] = False
    SERVER_STATE["findings"].clear()
    SERVER_STATE["timeline"].clear()
    SERVER_STATE["risk"] = "LOW"

    print(f"\nAdmin access granted for {target}\n")

    while True:
        cmd = input(server_prompt(target, role, SERVER_STATE["risk"])).lower().strip()

        if cmd in ("exit", "back"):
            return

        elif cmd == "help":
            print("""
COMMANDS
--------
recon       - reconnaissance
scan        - service scan
enum        - enumerate services
config      - config audit
escalate    - privilege escalation (demo)
persist     - persistence check
cleanup     - cleanup traces (demo)
risk        - overall risk
report txt  - export report txt
report json - export report json
status      - show progress
exit        - return
""")

        elif cmd == "recon":
            progress_1_to_100("Reconnaissance")
            SERVER_STATE["steps"]["recon"] = True
            SERVER_STATE["findings"].append("Directory listing enabled")
            log_step("recon", "Basic host & surface info collected")
            print("Recon completed")

        elif cmd == "scan":
            if not SERVER_STATE["steps"]["recon"]:
                print("Run recon first")
                continue
            progress_1_to_100("Service Scan")
            SERVER_STATE["steps"]["scan"] = True
            SERVER_STATE["findings"].append("Outdated services")
            log_step("scan", "Open ports and versions identified")
            print("Scan completed")

        elif cmd == "enum":
            if not SERVER_STATE["steps"]["scan"]:
                print("Run scan first")
                continue
            progress_1_to_100("Enumeration")
            SERVER_STATE["steps"]["enum"] = True
            log_step("enum", "Service enumeration done")
            print("Enumeration completed")

        elif cmd == "config":
            if not SERVER_STATE["steps"]["enum"]:
                print("Run enum first")
                continue
            progress_1_to_100("Config Audit")
            SERVER_STATE["steps"]["config"] = True
            SERVER_STATE["findings"].append("Weak sudoers config")
            log_step("config", "Config weaknesses found")
            print("Config audit completed")

        elif cmd == "escalate":
            if not SERVER_STATE["steps"]["config"]:
                print("Run config first")
                continue
            progress_1_to_100("Privilege Escalation (Demo)")
            SERVER_STATE["steps"]["escalate"] = True
            SERVER_STATE["findings"].append("Weak SSH policy")
            log_step("escalate", "Escalation path simulated")
            print("Escalation simulation completed")

        elif cmd == "persist":
            if not SERVER_STATE["steps"]["escalate"]:
                print("Run escalate first")
                continue
            progress_1_to_100("Persistence Check")
            SERVER_STATE["steps"]["persist"] = True
            log_step("persist", "Persistence vectors reviewed")
            print("Persistence check completed")

        elif cmd == "cleanup":
            progress_1_to_100("Cleanup")
            SERVER_STATE["steps"]["cleanup"] = True
            log_step("cleanup", "Artifacts cleaned (demo)")
            print("Cleanup completed")

        elif cmd == "risk":
            SERVER_STATE["risk"] = server_risk_engine(SERVER_STATE["findings"])
            print(f"OVERALL RISK: {SERVER_STATE['risk']}")

        elif cmd.startswith("report"):
            SERVER_STATE["risk"] = server_risk_engine(SERVER_STATE["findings"])
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            if "json" in cmd:
                fn = f"server_report_{ts}.json"
                with open(fn, "w", encoding="utf-8") as f:
                    import json
                    json.dump(SERVER_STATE, f, indent=2)
                print(f"Saved {fn}")
            else:
                fn = f"server_report_{ts}.txt"
                with open(fn, "w", encoding="utf-8") as f:
                    f.write(f"Target: {target}\nRole: {role}\nRisk: {SERVER_STATE['risk']}\n\nFindings:\n")
                    for x in SERVER_STATE["findings"]:
                        f.write(f"- {x}\n")
                    f.write("\nTimeline:\n")
                    for t in SERVER_STATE["timeline"]:
                        f.write(f"{t['time']} | {t['step']} | {t['note']}\n")
                print(f"Saved {fn}")

        elif cmd == "status":
            print("Steps:")
            for k,v in SERVER_STATE["steps"].items():
                print(f" - {k}: {'OK' if v else 'PENDING'}")

        else:
            print("Unknown command. Type 'help'")

# ================= Hidden lab =================
def hidden_lab():
    lab_banner()
    print("Type 'help' to see lab commands\n")

    selected_wifi = None
    selected_social = None
    social_role = None

    while True:
        cmd = input(lab_prompt("MAIN")).lower().strip()
        # ==== Server lab =======
        if cmd == "server enter":
            server_lab()
            continue

        # ===== EXIT =====
        if cmd in ("exit", "quit", "back"):
            return

        # ===== HELP =====
        if cmd == "help":
            print("""
LAB COMMANDS
------------
wifi scan        - scan real wifi
wifi select      - choose wifi target
wifi analyze     - analyze selected wifi

social enter     - enter social lab (ask role)
social scan      - scan account (demo)
social atk       - attack simulation (admin)
social dep       - defense simulation (admin)

server enter    - enter server security lab (admin only)

status           - show current target
exit             - return main menu
""")
            continue

        # ===== WIFI =====
        if cmd == "wifi scan":
            wifi_scan()
            continue

        if cmd == "wifi select":
            nets = parse_real_wifi()
            if not nets:
                print("No networks found")
                continue
            target = select_ssid(nets)
            selected_wifi = target
            print(f"Selected WiFi: {target['ssid']}")
            continue

        if cmd == "wifi analyze":
            if not selected_wifi:
                print("No WiFi selected")
                continue
            progress_1_to_100("Analyzing WiFi Security")
            overall = rule_engine(selected_wifi)
            fake_ai_insight(selected_wifi["ssid"])
            print(f"Overall Risk: {overall}")
            continue

        # ===== SOCIAL =====
        if cmd == "social enter":
            selected_social = input("Platform (Facebook/TikTok/Instagram...) > ")
            social_role = input("Role (user/admin) > ").lower()
            if social_role not in ("user", "admin"):
                social_role = "user"
            print(f"Entered Social Lab: {selected_social} ({social_role})")
            continue

        if cmd == "social scan":
            if not selected_social:
                print("Enter social lab first")
                continue
            progress_1_to_100("Scanning Account Metadata")
            fake_account = {
                "password_strength": random.choice(["WEAK", "STRONG"]),
                "2fa": random.choice([True, False]),
                "public_profile": random.choice([True, False])
            }
            rule_engine(fake_account, RULES_ACCOUNT)
            continue

        if cmd == "social atk":
            if social_role != "admin":
                print("Permission denied (admin only)")
                continue
            progress_1_to_100("Attack Chain Simulation")
            print("Attack simulation completed")
            continue

        if cmd == "social dep":
            if social_role != "admin":
                print("Permission denied (admin only)")
                continue
            progress_1_to_100("Defense Hardening")
            print("Defense simulation completed")
            continue

        if cmd == "status":
            print("STATUS")
            print(" WiFi :", selected_wifi["ssid"] if selected_wifi else "None")
            print(" Social :", selected_social if selected_social else "None")
            print(" Role :", social_role if social_role else "None")
            continue

        print("Unknown command. Type 'help'")

# ================= WIFI =================
import subprocess
import platform

def wifi_scan():
    os_name = platform.system()

    print(f"\n[+] Scanning Wi-Fi on {os_name}...\n")

    try:
        if os_name == "Windows":
            cmd = ["netsh", "wlan", "show", "networks", "mode=Bssid"]
            result = subprocess.check_output(cmd, encoding="utf-8", errors="ignore")
            print(result)

        elif os_name == "Linux":
            cmd = ["nmcli", "-f", "IN-USE,SSID,SIGNAL,SECURITY", "dev", "wifi", "list"]
            result = subprocess.check_output(cmd, encoding="utf-8", errors="ignore")
            print(result)

        elif os_name == "Darwin":  # macOS
            cmd = [
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
                "-s"
            ]
            result = subprocess.check_output(cmd, encoding="utf-8", errors="ignore")
            print(result)

        else:
            print("❌ OS not supported")

    except Exception as e:
        print(f"❌ Scan failed: {e}")
        

                   #thêm
def parse_real_wifi():
    os_name = platform.system()
    networks = []

    try:
        if os_name == "Windows":
            out = subprocess.check_output(
                ["netsh", "wlan", "show", "networks", "mode=Bssid"],
                encoding="utf-8", errors="ignore"
            )

            ssid = None
            sec = "UNKNOWN"
            signal = -80

            for line in out.splitlines():
                line = line.strip()

                if line.startswith("SSID "):
                    if ssid:
                        networks.append({"ssid": ssid, "security": sec, "signal": signal})
                    ssid = line.split(":", 1)[1].strip()
                    sec = "UNKNOWN"
                    signal = -80

                elif line.startswith("Authentication"):
                    auth = line.split(":", 1)[1].strip().upper()
                    if "OPEN" in auth:
                        sec = "OPEN"
                    elif "WPA3" in auth:
                        sec = "WPA3"
                    elif "WPA2" in auth:
                        sec = "WPA2"

                elif line.startswith("Signal"):
                    pct = int(line.split(":", 1)[1].replace("%", "").strip())
                    # quy đổi % → dBm (ước lượng)
                    signal = int(pct / 2 - 100)

            if ssid:
                networks.append({"ssid": ssid, "security": sec, "signal": signal})

        elif os_name == "Linux":
            out = subprocess.check_output(
                ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi", "list"],
                encoding="utf-8", errors="ignore"
            )
            for row in out.splitlines():
                parts = row.split(":")
                if len(parts) >= 3:
                    ssid = parts[0] or "<hidden>"
                    signal = int(parts[1]) / 2 - 100
                    sec = "OPEN" if parts[2] == "" else ("WPA3" if "WPA3" in parts[2] else "WPA2")
                    networks.append({"ssid": ssid, "security": sec, "signal": int(signal)})

    except Exception as e:
        print(f"[!] Parse scan failed: {e}")

    return networks

    #==========Select SSID==================
def select_ssid(networks):
    print("\nAvailable Networks:")
    for i, n in enumerate(networks, 1):
        print(f"{i}) {n['ssid']} | {n['security']} | {n['signal']} dBm")

    while True:
        try:
            idx = int(input("\nSelect SSID number > "))
            if 1 <= idx <= len(networks):
                return networks[idx - 1]
        except:
            pass
        print("Invalid selection.")


    #=========Rules============
def rule_engine(network):
    print(f"\n[RULE ENGINE] Evaluating: {network['ssid']}")
    total = 0
    hits = 0

    for rule in RULES:
        try:
            if rule["check"](network):
                hits += 1
                score = RISK_SCORE.get(rule["risk"], 1)
                total += score
                print(f"[{rule['risk']}] {rule['name']}")
                print(f" └─ {rule['note']}")
        except Exception:
            pass

    if hits == 0:
        print("[INFO] No specific risk rules triggered")
        return "LOW"

    avg = round(total / hits)
    overall = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}.get(avg, "LOW")
    print(f"[OVERALL RISK] {overall}")
    return overall

# ================= ANALYSIS =================
def security_analysis():
    rules = [
        ("Home_Wifi", "WPA2", "MEDIUM", "Upgrade to WPA3 recommended"),
        ("Cafe_Free", "OPEN", "HIGH", "Avoid sensitive traffic"),
        ("Office_AP", "WPA3", "LOW", "Configuration is secure")
    ]
    for ssid, enc, risk, note in rules:
        print(f"[ANALYZE] {ssid} | ENC={enc} | RISK={risk}")
        print(f"[ADVICE] {note}")
        time.sleep(0.6)

# ================= FAKE AI =================
def fake_ai_insight(target):
    logs = [
        f"Collecting metadata from {target}",
        "Evaluating encryption parameters",
        "Cross-checking configuration patterns",
        "Estimating exposure surface",
        "Generating mitigation strategies"
    ]
    for l in logs:
        print(f"[AI] {l}")
        time.sleep(0.7)
    print("[AI] Insight generation completed\n")
    #----------Analysics-------------
def security_analysis():
    print("[+] Handshake integrity: OK")
    print("[+] Encryption strength: STRONG")
    print("[+] Known vulnerability: NONE")

def fake_ai_insight(ssid):
    print(f"\n[AI] Analyzing network '{ssid}'")
    advanced_progress("AI Model Inference", 0.02, 0.05)
    print("[AI] Password entropy: HIGH")
    print("[AI] Estimated crack time: > 10 years")

# ================= FAKE MINER =================
def miner_simulation(duration=18):
    start = time.time()
    cycle = 0
    print("\n[MINER] Connecting to simulation pool...")
    staged_progress()

    while time.time() - start < duration:
        cycle += 1
        MINER["uptime"] = int(time.time() - start)
        MINER["hashrate"] = round(random.uniform(180, 360), 2)
        MINER["latency"] = random.randint(40, 120)

        if random.random() < 0.86:
            MINER["accepted"] += 1
        else:
            MINER["rejected"] += 1

        MINER["total"] += MINER["hashrate"] * 0.00000002
        usd = MINER["total"] * MINER["usd_rate"]

        percent = int((MINER["uptime"] / duration) * 100)
        percent = min(percent, 100)

        print(
            f"[MINER] Cycle {cycle:02d} | {percent:3d}% | "
            f"{MINER['hashrate']} H/s | Diff {MINER['difficulty']} | "
            f"Latency {MINER['latency']}ms | "
            f"Shares {MINER['accepted']}/{MINER['rejected']} | "
            f"Total {MINER['total']:.6f} XMR | ${usd:.2f}"
        )
        time.sleep(random.uniform(0.8, 1.4))

    print("[MINER] Simulation workload completed\n")
    #------------Miner--------------
def miner_simulation(duration=10):
    start = time.time()
    total = 0.0
    while time.time() - start < duration:
        hashrate = random.uniform(180, 360)
        total += hashrate * 0.00000002
        print(f"[MINER] {hashrate:.2f} H/s | Total {total:.6f} BTC")
        time.sleep(random.uniform(0.8, 1.3))

#============Social lab==============
def banner_7():
    os.system("cls" if os.name == "nt" else "clear")
    print("""                                                          
=== ___  ___   ___ ___   _   _ =========================================================  
=  / __|/ _ \ / __|_ _| /_\ | |            ◢◤  W I F I   A U D I T   S Y S T E M  ◢◤  =                                             -------------------------------------------
=  \__ \ (_) | (__ | | / _ \| |__          -------------------------------------------  =
=  |___/\___/ \___|___/_/ \_\____|                                                      =
=  | \| | __|_   _| / / _ \/ __| |/ |                                                   =
=  | .` | _|  | |  / / (_) \__ \ ' <                                                    =
=  |_|\_|___| |_| /_/ \___/|___/_|\_|    by Dang Khoa                                   =
========================================-==============================================
                         SOCIAL ACCOUNT LAB - MODULE 7
                          (EDUCATION / SIMULATION)
                   ========================================
""")


def gate_admin_7():
    pwd = input("Admin password > ")
    return pwd == MENU7_ADMIN_PASSWORD

def social_rule_engine(data):
    score = 0
    hits = 0

    for r in SOCIAL_RULES:
        if r["check"](data):
            hits += 1
            if r["risk"] == "HIGH":
                score += 3
            elif r["risk"] == "MEDIUM":
                score += 2
            else:
                score += 1

    if hits == 0:
        return "LOW"

    avg = round(score / hits)
    return "HIGH" if avg >= 3 else "MEDIUM" if avg == 2 else "LOW"

def fake_scan(platform):
    print(f"[SCAN] Collecting public data from {platform} ...")
    time.sleep(1)
    print("[OK] Username, followers, privacy flags collected")


def fake_info(platform):
    print(f"[INFO] Platform: {platform}")
    print("[INFO] Risk model: DEMO")
    print("[INFO] No real data accessed")


def fake_attack(platform):
    print(f"[SIM] Running simulated attack chain on {platform}")
    time.sleep(1)
    print("[SIM] Phishing vector: TEST")
    print("[SIM] Credential reuse: TEST")
    print("[DONE] Simulation finished")


def fake_defense(platform):
    print(f"[SIM] Applying defense checklist for {platform}")
    time.sleep(1)
    print("[OK] Enable 2FA")
    print("[OK] Strong password")
    print("[OK] Privacy hardened")


def fake_osint(platform):
    print(f"[OSINT] Mapping public footprint on {platform}")
    time.sleep(1)
    print("[OK] Public posts indexed (fake)")


def fake_bruteforce(platform):
    print(f"[SIM] Brute force simulation on {platform}")
    time.sleep(1)
    print("[BLOCKED] Rate-limit triggered (demo)")


def fake_report(platform, role):
    fname = f"report_{platform}_{role}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"PLATFORM: {platform}\n")
        f.write(f"ROLE: {role}\n")
        f.write("MODE: SIMULATION ONLY\n")
        f.write("STATUS: OK\n")
    print(f"[OK] Report exported: {fname}")


def command_mode_7(platform):
    banner_7()
    role = input("Permission (user/admin) > ").lower()

    if role == "admin":
        if not gate_admin_7():
            print("[DENIED] Wrong admin password")
            input("Press ENTER...")
            return
    elif role != "user":
        role = "user"

    while True:
        cmd = input(f"[M7:{platform}:{role}]> ").lower().strip()

        if cmd == "exit":
            return

        if cmd not in PERMISSIONS_7[role]:
            print("[DENIED] Command not allowed")
            continue

        if cmd == "help":
            print("Available commands:")
            for c in PERMISSIONS_7[role]:
                print("-", c)

        elif cmd == "scan":
            fake_scan(platform)

        elif cmd == "info":
            fake_info(platform)

        elif cmd == "atk":
            fake_attack(platform)

        elif cmd == "dep":
            fake_defense(platform)

        elif cmd == "osint":
            fake_osint(platform)

        elif cmd == "brute":
            fake_bruteforce(platform)

        elif cmd == "report":
            fake_report(platform, role)

def prompt_7(platform, role, risk=None):
    base = f"SOCIAL-LAB {platform} [{role}]"
    if risk:
        base += f" <{risk}>"
    return base + " > "

def menu_7_social_lab():
    while True:
        banner()
        print("=== MODULE 7: SOCIAL ACCOUNT LAB ===\n")

        for i, p in enumerate(SOCIAL_PLATFORMS, 1):
            print(f"{i}) {p}")
        print("0) Back")

        c = input("Select platform > ").strip()

        if c == "0":
            return

        if c.isdigit():
            idx = int(c)
            if 1 <= idx <= len(SOCIAL_PLATFORMS):
                command_mode_7(SOCIAL_PLATFORMS[idx - 1])

def menu_7_social_lab():
    while True:
        banner_7()
        for i, p in enumerate(SOCIAL_PLATFORMS, 1):
            print(f"{i}) {p}")
        print("B) Back")

        c = input("Select platform > ").lower()

        if c == "b":
            return

        if c.isdigit():
            idx = int(c)
            if 1 <= idx <= len(SOCIAL_PLATFORMS):
                command_mode_7(SOCIAL_PLATFORMS[idx - 1])

def command_mode_7(platform):
    role = input("Select role (user/admin) > ").lower()
    if role == "admin":
        if not password_gate():
            return
    if role not in PERMISSIONS_7:
        role = "user"

    last_data = None
    last_risk = None

    while True:
        cmd = input(prompt_7(platform, role, last_risk)).strip().lower()

        if cmd == "exit":
            return

        if cmd not in PERMISSIONS_7[role]:
            print("[DENIED] Permission required")
            continue

        if cmd == "help":
            print("Commands:", ", ".join(PERMISSIONS_7[role]))
            continue

        if cmd == "scan":
            print("[1/3] Collecting public data...")
            time.sleep(1)
            print("[2/3] Analyzing security settings...")
            time.sleep(1)
            print("[3/3] Building profile...")
            time.sleep(1)

            last_data = {
                "password": random.choice(["WEAK", "STRONG"]),
                "2fa": random.choice([True, False]),
                "public": random.choice([True, False])
            }

            last_risk = social_rule_engine(last_data)
            print("Scan complete. Risk:", last_risk)

        elif cmd == "atk":
            print("[SIM] Running attack simulation...")
            time.sleep(2)
            print("[SIM] Attack paths evaluated")

        elif cmd == "dep":
            print("[SIM] Applying defense hardening...")
            time.sleep(2)
            print("[SIM] Security posture improved")

        elif cmd == "risk":
            if not last_data:
                print("No data. Run scan first.")
            else:
                print("Current risk:", last_risk)

        elif cmd == "report":
            if not last_data:
                print("Nothing to report.")
                continue
            fname = f"social_{platform.lower()}_report.txt"
            with open(fname, "w") as f:
                f.write(f"Platform: {platform}\n")
                f.write(f"Role: {role}\n")
                f.write(f"Risk: {last_risk}\n")
                f.write(str(last_data))
            print("Report exported:", fname)

#============Command mode=========
def command_mode():
    command_banner()
    networks = []
    state = "IDLE"
    target_ssid = None

    COMMANDS = {}

    def require(cmd):
        need = PERMISSIONS.get(cmd, "guest")
        if role_level(USER_ROLE) < role_level(need):
            print(f"[DENIED] '{cmd}' requires role: {need}")
            return False
        return True

    def cmd_scan(args):
        nonlocal networks, state
        networks = parse_real_wifi()
        state = "SCANNED"
        print(f"[✓] Found {len(networks)} networks")

    def cmd_list(args):
        if not networks:
            print("[!] Run scan first")
            return
        for i, n in enumerate(networks, 1):
            print(f"{i}) {n['ssid']} | {n['security']} | {n['signal']} dBm")

    def cmd_select(args):
        nonlocal state, target_ssid
        if not networks:
            print("[!] Run scan first")
            return
        target = select_ssid(networks)
        target_ssid = target["ssid"]
        state = "TARGET"
        rule_engine(target)

    def cmd_risk_all(args):
        if not networks:
            print("[!] Run scan first")
            return
        summary = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for n in networks:
            r = rule_engine(n)
            summary[r] += 1
        print("\n=== RISK SUMMARY ===")
        for k, v in summary.items():
            print(f"{k}: {v}")

    # registry
    COMMANDS["scan"] = cmd_scan
    COMMANDS["list"] = cmd_list
    COMMANDS["select"] = cmd_select
    COMMANDS["risk all"] = cmd_risk_all

    while True:
        prompt = build_prompt(state, target_ssid)
        raw = input(prompt).strip()

        if not raw:
            continue

        # alias
        raw = ALIASES.get(raw, raw)

        if raw in ("exit", "quit"):
            print("[*] Exit command mode")
            break

        if raw.startswith("help"):
            parts = raw.split()
            help_command(parts[1] if len(parts) > 1 else None)
            continue

        if raw not in COMMANDS:
            print("Unknown command. Type 'help'")
            continue

        if not require(raw):
            continue

        COMMANDS[raw]([])

# ================= ENGINE =================
def engine():
    global STATE

    STATE = "INIT"
    banner()
    print("[*] Initializing framework")
    staged_progress()

    STATE = "SCAN"
    print("\n[*] Scanning wireless environment")
    advanced_progress("WiFi Scan Engine")
    wifi_scan()

    STATE = "ANALYZE"
    print("[*] Running security analysis")
    advanced_progress("Security Analyzer")
    security_analysis()
    fake_ai_insight("Home_Wifi")

    STATE = "MINER"
    miner_simulation()

    STATE = "REPORT"
    generate_report()

    STATE = "WAIT"
    print("\n[✓] Demo completed. System idle.")
    while True:
        time.sleep(3)

# ================= MAIN =================
def advanced_menu():
    while True:
        banner()
        print("========= MAIN MENU =========")
        print("1) Full Audit (Scan + Analyze + AI + Miner + Report)")
        print("2) WiFi Scan Only")
        print("3) Security Analyze + AI Insight")
        print("4) Miner Simulation Only")
        print("5) System Monitor (idle view)")
        print("6) Command Mode (manual)")
        print("7) Secure Command Mode (Role Based)")
        print("0) Exit")
        print("=============================")

        choice = input("Select option > ").strip()

        # -------- FULL MODE --------
        if choice == "1":
            confirm = input("Run FULL audit simulation? (y/n) > ").lower()
            if confirm == "y":
                engine()
            else:
                print("Cancelled.")
                time.sleep(1)

        # -------- WIFI SCAN ONLY --------
        elif choice == "2":
            STATE = "SCAN"
            banner()
            advanced_progress("WiFi Scan Engine")
            wifi_scan()
            input("Press ENTER to return to menu...")

        # -------- ANALYZE + AI --------   
        elif choice == "3":
            STATE = "ANALYZE"
            banner()

            networks = parse_real_wifi()
            if not networks:
                print("No networks found.")
                input("Press ENTER...")
                continue

            target = select_ssid(networks)
            ssid = target["ssid"]

            while True:
                cmd = input(simple_prompt("ANALYZE", ssid)).lower().strip()

                if cmd == "run":
                    overall = rule_engine(target)
                    fake_ai_insight(ssid)
                    print(f"\nOverall risk: {overall}")

                elif cmd == "info":
                    print(target)

                elif cmd == "back":
                    break

                else:
                    print("Commands: run | info | back")

        # -------- MINER ONLY --------
        elif choice == "4":
            STATE = "MINER"
            banner()
            print("[MODE] Miner Simulation Only\n")
            miner_simulation()
            input("\nPress ENTER to return to menu...")

        # -------- MONITOR IDLE --------
        elif choice == "5":
            STATE = "IDLE"
            banner()
            print("[MODE] System Monitor (Idle)")
            print("Press Ctrl+C to stop and return to menu\n")
            try:
                while True:
                    time.sleep(2)
            except KeyboardInterrupt:
                pass
        
        #----------Social lab-----------
        elif choice == "7":
            menu_7_social_lab()

        #----------Command mode-------
        elif choice == "6":
            command_mode()
        
        #----------Hidden lab---------
        elif choice == "8":
            hidden_lab()
        
        #----------Server lab--------
        elif choice == "9":
            server_lab()

        # -------- EXIT --------
        elif choice == "0":
            print("Exiting framework...")
            time.sleep(1)
            sys.exit()

        else:
            print("Invalid option.")
            time.sleep(1)
  

if __name__ == "__main__":

    if password_gate():
        advanced_menu()

if __name__ == "__main__":
    if password_gate():
        advanced_menu()

