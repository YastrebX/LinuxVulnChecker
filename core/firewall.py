import subprocess

def verify_firewall_rules():
    """
    Checks if a firewall is active and evaluates its rules.
    Returns a summary of findings.
    """
    findings = []

    try:
        # Check if a firewall is active (example: UFW for Ubuntu systems)
        status_output = subprocess.check_output(["ufw", "status"], text=True).strip()
        if "inactive" in status_output.lower():
            findings.append("Firewall is inactive.")
        else:
            findings.append("Firewall is active.")
            findings.append("Firewall rules:\n" + status_output)

    except FileNotFoundError:
        findings.append("The 'ufw' command is not available. Ensure a firewall is installed.")
    except Exception as e:
        findings.append(f"Error while verifying firewall rules: {str(e)}")

    return "\n".join(findings) if findings else "No firewall issues detected."
