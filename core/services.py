import subprocess

def check_unnecessary_services():
    """
    Lists enabled services and compares them with a list of commonly unnecessary services.
    Returns a summary of findings.
    """
    unnecessary_services = [
        "telnet",
        "rsh",
        "rlogin",
        "rexec",
        "ftp",
        "nfs",
        "rpcbind",
    ]
    findings = []

    try:
        # Use `systemctl list-unit-files` to get the status of all services
        output = subprocess.check_output(["systemctl", "list-unit-files"], text=True)
        lines = output.strip().split("\n")

        for line in lines:
            for service in unnecessary_services:
                if service in line and "enabled" in line:
                    findings.append(f"Unnecessary service '{service}' is enabled.")

    except FileNotFoundError:
        findings.append("The 'systemctl' command is not available. Unable to list services.")
    except Exception as e:
        findings.append(f"Error while checking unnecessary services: {str(e)}")

    return "\n".join(findings) if findings else "No unnecessary services detected."
