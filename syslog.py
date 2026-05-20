#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import textwrap
import argparse
import plistlib
import requests

# --- CONFIGURATION ---
SCRIPT_PATH = os.path.abspath(sys.argv[0])
LOG_PATH = os.path.expanduser("~/logger.log")

SERVICE_NAME = "com.user.loggerpy"

LAUNCH_AGENTS_DIR = os.path.expanduser("~/Library/LaunchAgents")
PLIST_PATH = os.path.join(LAUNCH_AGENTS_DIR, f"{SERVICE_NAME}.plist")


def setup_launchd_service(server_url=None):
    """Create and load a macOS LaunchAgent."""

    os.makedirs(LAUNCH_AGENTS_DIR, exist_ok=True)

    program_args = [sys.executable, SCRIPT_PATH]

    if server_url:
        program_args += ["--server", server_url]

    plist_data = {
        "Label": SERVICE_NAME,
        "ProgramArguments": program_args,
        "RunAtLoad": True,
        "KeepAlive": True,
        "StandardOutPath": LOG_PATH,
        "StandardErrorPath": LOG_PATH,
    }

    with open(PLIST_PATH, "wb") as f:
        plistlib.dump(plist_data, f)

    print(f"LaunchAgent written to: {PLIST_PATH}")

    # Unload old version if already loaded
    subprocess.run(
        ["launchctl", "unload", PLIST_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Load the service
    result = subprocess.run(
        ["launchctl", "load", PLIST_PATH],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error loading LaunchAgent:")
        print(result.stderr)
    else:
        print(f"{SERVICE_NAME} loaded and started!")


def get_cpu_usage():
    """Get CPU usage on macOS."""
    try:
        output = subprocess.getoutput(
            "top -l 1 | grep 'CPU usage'"
        )
        return output.strip()
    except Exception as e:
        return f"CPU usage unavailable: {e}"


def get_memory_usage():
    """Get memory info on macOS."""
    try:
        output = subprocess.getoutput("vm_stat")
        return output.replace("\n", " | ")
    except Exception as e:
        return f"Memory usage unavailable: {e}"


def log_metrics(server_url=None):
    """Capture system metrics and optionally send them to a server."""

    uptime = subprocess.getoutput("uptime")
    cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()

    log_line = (
        f"[{time.ctime()}] "
        f"{uptime} | "
        f"{cpu_usage} | "
        f"{mem_usage}\n"
    )

    # Write to local log file
    with open(LOG_PATH, "a") as f:
        f.write(log_line)

    print(log_line, end="")

    # Send to server if URL provided
    if server_url:
        try:
            response = requests.post(server_url, data={"log": log_line})

            if response.status_code != 200:
                print(
                    f"Warning: Failed to send log "
                    f"to server ({response.status_code})"
                )

        except requests.RequestException as e:
            print(f"Error sending log to server: {e}")


def main():
    parser = argparse.ArgumentParser(description="macOS System Logger")

    parser.add_argument(
        "--server",
        type=str,
        help="Send logs to this server URL",
    )

    parser.add_argument(
        "--setup-service",
        action="store_true",
        help="Setup LaunchAgent for automatic logging",
    )

    args = parser.parse_args()

    if args.setup_service:
        setup_launchd_service(server_url=args.server)

    while True:
        log_metrics(server_url=args.server)
        time.sleep(60)


if __name__ == "__main__":
    main()
