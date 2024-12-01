import re
import subprocess

def audit_system_logs():
    """
    Scans system logs for suspicious entries such as repeated login failures
    or unexpected system reboots.
    Returns a summary of findings.
    """
    findings = []

    try:
        # Read authentication logs for login failures
        auth_log_path = "/var/log/auth.log"  # Adjust for system (e.g., "/var/log/secure" for CentOS)
        with open(auth_log_path, "r") as log_file:
            logins = []
            for line in log_file:
                if "Failed password" in line:
                    logins.append(line.strip())
        
        if logins:
            findings.append(f"Failed login attempts:\n{len(logins)} attempts detected.")
        else:
            findings.append("No failed login attempts detected.")

        # Read kernel logs for unexpected reboots
        kernel_log_path = "/var/log/kern.log"  # Adjust for system if needed
        with open(kernel_log_path, "r") as log_file:
            reboots = []
            for line in log_file:
                if "Kernel panic" in line or "unexpected reboot" in line.lower():
                    reboots.append(line.strip())
        
        if reboots:
            findings.append(f"Unexpected reboots detected:\n{len(reboots)} events found.")
        else:
            findings.append("No unexpected reboots detected.")
    except FileNotFoundError:
        findings.append("Required log file not found for log analysis.")
    except Exception as e:
        findings.append(f"Error while auditing system logs: {str(e)}")

    return "\n".join(findings) if findings else "No issues detected in system logs."
