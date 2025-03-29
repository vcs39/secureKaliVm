#!/usr/bin/env python3
import subprocess
import os
import getpass

def print_banner():
    ascii_banner = r"""
 __     ___      _                    ____      _               
 \ \   / (_) ___(_) ___  _   _ ___   / ___|   _| |__   ___ _ __ 
  \ \ / /| |/ __| |/ _ \| | | / __| | |  | | | | '_ \ / _ \ '__|
   \ V / | | (__| | (_) | |_| \__ \ | |__| |_| | |_) |  __/ |   
    \_/  |_|\___|_|\___/ \__,_|___/  \____\__, |_.__/ \___|_|   
                                          |___/                 

 ____        _       _   _                 
/ ___|  ___ | |_   _| |_(_) ___  _ __  ___ 
\___ \ / _ \| | | | | __| |/ _ \| '_ \/ __|
 ___) | (_) | | |_| | |_| | (_) | | | \__ \\
|____/ \___/|_|\__,_|\__|_|\___/|_| |_|___/
    """
    print(ascii_banner)
    print("🔒 Vicious Cyber Solutions - secureKaliVM 🔒")

# Function: VMware Tools Installation
def install_vmware_tools():
    print("\n📦 [*] Installing VMware Tools...")
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "open-vm-tools", "open-vm-tools-desktop"], check=True)
        print("✅ VMware Tools installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing VMware Tools: {e}")

# Function: Setup Firewall
def setup_firewall():
    print("\n🔐 [*] Setting up UFW Firewall...")
    try:
        subprocess.run(["sudo", "apt", "install", "-y", "ufw"], check=True)
        subprocess.run(["sudo", "ufw", "default", "deny", "incoming"], check=True)
        subprocess.run(["sudo", "ufw", "default", "allow", "outgoing"], check=True)

        ssh = input("Do you want to allow SSH access? (y/n): ").strip().lower()
        if ssh == 'y':
            port = input("Enter the SSH port (default is 22): ").strip()
            port = port if port else "22"
            subprocess.run(["sudo", "ufw", "allow", f"{port}/tcp"], check=True)

        web = input("Are you running a web server (HTTP/HTTPS)? (y/n): ").strip().lower()
        if web == 'y':
            subprocess.run(["sudo", "ufw", "allow", "80/tcp"], check=True)
            subprocess.run(["sudo", "ufw", "allow", "443/tcp"], check=True)

        custom = input("Do you want to allow any custom ports? (e.g., 1337/tcp) (y/n): ").strip().lower()
        while custom == 'y':
            port_proto = input("Enter the port and protocol (e.g., 8080/udp): ").strip()
            if port_proto:
                subprocess.run(["sudo", "ufw", "allow", port_proto], check=True)
            custom = input("Add another custom port? (y/n): ").strip().lower()

        subprocess.run(["sudo", "ufw", "--force", "enable"], check=True)
        subprocess.run(["sudo", "ufw", "status", "verbose"])
        subprocess.run(["sudo", "ufw", "status", "verbose"], check=True)
        print("\n✅ Firewall is active and configured!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up firewall: {e}")

# Function: Set Up 2FA
def setup_2fa():
    print("\n🔑 [*] Setting up Two-Factor Authentication (2FA)...")
    print("ℹ️ This will guide the user to install Google Authenticator.")
    try:
        subprocess.run(["sudo", "apt", "install", "-y", "libpam-google-authenticator"], check=True)
        subprocess.run(["google-authenticator"], check=True)
        print("✅ 2FA setup initiated. Follow the prompts in terminal.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during 2FA setup: {e}")

# Function: Create Backup
def create_backup():
    default_backup_path = "/home/vcs39/secureKaliVM_backup"
    backup_path = input(f"Enter backup path (default: {default_backup_path}): ").strip() or default_backup_path

    try:
        if not os.path.exists(backup_path):
            subprocess.run(["sudo", "mkdir", "-p", backup_path], check=True)

        ssh_path = "/home/vcs39/.ssh"
        if not os.path.exists(ssh_path):
            print(f"⚠️ Warning: Source directory '{ssh_path}' does not exist. Creating it now...")
            os.makedirs(ssh_path, exist_ok=True)

        subprocess.run(["sudo", "cp", "-r", ssh_path, backup_path], check=True)
        print(f"[+] Backup completed successfully at {backup_path}.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating backup: {e}")

# Main Execution
if __name__ == "__main__":
    print_banner()  # Call the function to display the banner
    install_vmware_tools()
    setup_firewall()
    setup_2fa()
    create_backup()
