import os
import subprocess
from datetime import datetime

# Log file setup
LOG_FILE = f"sv_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log_message(message):
    # Append a message to the log file.
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def run_command(command):
    # Run a system command and return the output.
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        log_message(f"Error running command {command}: {e.output.decode().strip()}")
        return None

# 1. Check File Permissions
def check_file_permissions():
    log_message("\n----- File Permissions Check -----")
    
    # Checking for world-writable files
    log_message("\nWorld-writable files:")
    output = run_command("find / -perm -2 -type f 2>/dev/null")
    log_message(output if output else "No world-writable files found.")
    
    # Checking permissions on /etc/passwd and /etc/shadow
    log_message("\n/etc/passwd permissions:")
    output = run_command("ls -l /etc/passwd")
    log_message(output)
    
    log_message("\n/etc/shadow permissions:")
    output = run_command("ls -l /etc/shadow")
    log_message(output)

# 2. Check User & Group Configurations
def check_user_group_configurations():
    log_message("\n----- User & Group Configurations -----")
    
    # Check for users with UID 0 (root privileges)
    log_message("\nUsers with UID 0 (root privileges):")
    output = run_command("awk -F: '$3 == 0 { print $1 }' /etc/passwd")
    log_message(output if output else "No users with UID 0 found except root.")
    
    # Check for inactive users
    log_message("\nInactive users (no recent login):")
    output = run_command("lastlog | grep 'Never logged in'")
    log_message(output if output else "No inactive users found.")

# 3. Check Running Services & Network Configuration
def check_services_network():
    log_message("\n----- Running Services & Network Configuration -----")
    
    # List services running as root
    log_message("\nServices running as root:")
    output = run_command("ps -eo user,comm | grep '^root' | awk '{print $2}' | sort | uniq")
    log_message(output if output else "No services running as root.")

    # List listening ports
    log_message("\nListening network services:")
    output = run_command("ss -tuln")
    log_message(output)

# 4. Check Firewall Rules
def check_firewall():
    log_message("\n----- Firewall Rules -----")
    
    # Check if UFW (Uncomplicated Firewall) is active
    log_message("\nUFW status:")
    output = run_command("ufw status")
    log_message(output if output else "UFW not found or inactive.")

# 5. Check Outdated/Vulnerable Packages
def check_packages():
    log_message("\n----- Package Security Check -----")
    
    # Check for available updates
    log_message("\nAvailable package updates:")
    output = run_command("apt list --upgradable 2>/dev/null")
    log_message(output if output else "All packages are up to date.")

# 6. Check Logs for Suspicious Activity
def check_logs():
    log_message("\n--- Log Auditing ---")
    
    # Check for failed SSH login attempts
    log_message("\nFailed SSH login attempts:")
    output = run_command("grep 'Failed password' /var/log/auth.log")
    log_message(output if output else "No failed SSH login attempts found.")

# 7. Find SUID/SGID Files
def check_suid_sgid():
    log_message("\n----- SUID/SGID Files -----")
    
    # Find files with the SUID/SGID bit set
    log_message("\nFiles with SUID/SGID bit set:")
    output = run_command("find / -perm /6000 -type f 2>/dev/null")
    log_message(output if output else "No SUID/SGID files found.")

# 8. Check Kernel and System Security Settings
def check_kernel_security():
    log_message("\n----- Kernel & System Security -----")
    
    # Check sysctl settings for common hardening
    log_message("\nSysctl settings related to security:")
    output = run_command("sysctl -a | grep 'kernel\\|net.ipv4.conf.all.rp_filter\\|net.ipv4.conf.all.accept_source_route'")
    log_message(output)

def main():
    log_message("Linux Server Vulnerability Report")
    log_message(f"Report generated on {datetime.now()}\n")
    
    check_file_permissions()
    check_user_group_configurations()
    check_services_network()
    check_firewall()
    check_packages()
    check_logs()
    check_suid_sgid()
    check_kernel_security()
    
    log_message("\n Vulnerability checking is complete. Report saved to: " + LOG_FILE)

if __name__ == "__main__":
    main()
