import os
import psutil
import win32api
import win32gui
import win32process
import pythoncom
import pyHook

# Set the name of the program to monitor
program_name = "PROGRAM.exe"

# Set the list of monitored keys
monitored_keys = ["Oem_Period", "Oem_Comma", "Space", "Return"]

# Initialise the dictionary of pressed keys
pressed_keys = {}

# Set up the hook manager
hook_manager = pyHook.HookManager()
hook_manager.KeyDown = lambda event: on_key_press(event)
hook_manager.HookKeyboard()

# Set up the process handle
pid = None
hwnd = win32gui.GetForegroundWindow()
if win32gui.IsWindowVisible(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
process_handle = psutil.Process(pid) if pid else None

# Log the network connections made by the process
def log_network_connections():
    if process_handle:
        with open(f"{program_name}_network_connections.txt", "w") as f:
            f.write(f"Network connections for process {process_handle.name()} (pid {process_handle.pid}):\n\n")
            connections = process_handle.connections()
            for conn in connections:
                f.write(f"Family: {conn.family}, Type: {conn.type}, Local Address: {conn.laddr}, Remote Address: {conn.raddr}, Status: {conn.status}\n")
            f.write("\n")

# Start the message loop to capture keystrokes
while True:
    pythoncom.PumpWaitingMessages()

    # Check if the current process has changed
    new_hwnd = win32gui.GetForegroundWindow()
    if hwnd != new_hwnd:
        hwnd = new_hwnd
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_handle = psutil.Process(pid) if pid else None
        log_network_connections()

# Handler for key presses
def on_key_press(event):
    key = event.Key
    if key in monitored_keys:
        if key not in pressed_keys:
            pressed_keys[key] = True
            log_key_press(key)
    return True

# Log the pressed key
def log_key_press(key):
    if process_handle:
        with open(f"{program_name}_keylog.txt", "a") as f:
            f.write(f"[{process_handle.name()} (pid {process_handle.pid})]: {key}\n")
