import os
import subprocess

def inspect_security_configurations():
    """
    Inspects critical security settings such as SSH configurations,
    SELinux/AppArmor status, and other system security tools.
    Returns a summary of findings.
    """
    findings = []

    # Check SSH configuration
    ssh_config_path = "/etc/ssh/sshd_config"
    try:
        with open(ssh_config_path, "r") as ssh_config:
            config = ssh_config.read()
            if "PermitRootLogin yes" in config:
                findings.append("SSH: Root login is permitted. Disable 'PermitRootLogin' for better security.")
            else:
                findings.append("SSH: Root login is disabled.")

            if "PasswordAuthentication yes" in config:
                findings.append("SSH: Password authentication is enabled. Consider using key-based authentication.")
            else:
                findings.append("SSH: Password authentication is disabled.")
    except FileNotFoundError:
        findings.append("SSH configuration file not found. Unable to inspect SSH settings.")
    except Exception as e:
        findings.append(f"Error while inspecting SSH configuration: {str(e)}")

    # Check SELinux or AppArmor status
    try:
        selinux_status = subprocess.check_output(["getenforce"], text=True).strip()
        findings.append(f"SELinux status: {selinux_status}")
    except FileNotFoundError:
        findings.append("SELinux tools are not installed.")
    except Exception as e:
        findings.append(f"Error while checking SELinux status: {str(e)}")

    try:
        apparmor_status = subprocess.check_output(["aa-status"], text=True).strip()
        findings.append(f"AppArmor status:\n{apparmor_status}")
    except FileNotFoundError:
        findings.append("AppArmor tools are not installed.")
    except Exception as e:
        findings.append(f"Error while checking AppArmor status: {str(e)}")

    return "\n".join(findings) if findings else "No issues detected in security configurations."
