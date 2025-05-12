#!/usr/bin/env python3

import subprocess

# Define Windows-style VM paths (Updated paths based on your input)
vm_paths = {
    "Ubuntu Server": r'"C:\\Users\\timot\\OneDrive\\Documents\\Virtual Machines\\Ubuntu Server\\Ubuntu Server.vmx"',
    "Ubuntu Desktop": r'"C:\\Users\\timot\\OneDrive\\Documents\\Virtual Machines\\Ubuntu Desktop\\Ubuntu Desktop.vmx"',
    "Windows 11": r'"C:\\Users\\timot\\OneDrive\\Documents\\Virtual Machines\\Windows 11\\Windows 11.vmx"',
    "Windows 10": r'"C:\\Users\\timot\\OneDrive\\Documents\\Virtual Machines\\Windows 11\\Windows 10.vmx"'
}

# Path to vmrun.exe (in Windows format)
vmrun_path = "C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe"

# Full path to PowerShell from WSL
powershell_path = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"

def run_powershell_command(args):
    """Runs a vmrun.exe command via PowerShell from WSL."""
    full_command = f'"{vmrun_path}" {args}'
    try:
        result = subprocess.run(
            [powershell_path, "-Command", f'& {full_command}'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr.strip())
    except Exception as e:
        print(f"Failed to run command: {e}")

def execute_vmrun(command, vm_name):
    """Executes vmrun start/stop for a VM."""
    if vm_name in vm_paths:
        run_powershell_command(f"{command} {vm_paths[vm_name]}")
    else:
        print(f"VM '{vm_name}' not found!")

def list_running_vms():
    """Lists running VMs."""
    print("\nRunning Virtual Machines:")
    run_powershell_command("list")

def get_vm_ips():
    """Retrieves IPs of running VMs."""
    print("\nFetching IP addresses of running VMs...")
    try:
        result = subprocess.run(
            [powershell_path, f'"{vmrun_path}" list'],
            capture_output=True, text=True
        )
        lines = result.stdout.splitlines()[1:]  # Skip first line
        if not lines:
            print("No VMs running.")
            return
        for vmx in lines:
            ip_result = subprocess.run(
                [powershell_path, f'"{vmrun_path}" getGuestIPAddress "{vmx.strip()}"'],
                capture_output=True, text=True
            )
            ip = ip_result.stdout.strip() or "Not Available"
            print(f"{vmx} - IP Address: {ip}")
    except Exception as e:
        print(f"Failed to get IPs: {e}")

def main():
    while True:
        print("\nVM Management Menu:")
        print("1. Start Ubuntu Server VM")
        print("2. Start Ubuntu Desktop VM")
        print("3. Start Windows 11 VM")
        print("4. Stop Ubuntu Server VM")
        print("5. Stop Ubuntu Desktop VM")
        print("6. Stop Windows 11 VM")
        print("7. List Running VMs")
        print("8. Get IP Addresses of Running VMs")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        actions = {
            "1": lambda: execute_vmrun("start", "Ubuntu Server"),
            "2": lambda: execute_vmrun("start", "Ubuntu Desktop"),
            "3": lambda: execute_vmrun("start", "Windows 11"),
            "4": lambda: execute_vmrun("stop", "Ubuntu Server"),
            "5": lambda: execute_vmrun("stop", "Ubuntu Desktop"),
            "6": lambda: execute_vmrun("stop", "Windows 11"),
            "7": list_running_vms,
            "8": get_vm_ips,
            "9": exit
        }

        actions.get(choice, lambda: print("Invalid selection!"))()

if __name__ == "__main__":
    main()
