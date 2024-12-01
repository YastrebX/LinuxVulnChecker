import subprocess

def inspect_running_processes():
    """
    Inspects currently running processes to look for suspicious activity or misconfigurations.
    Returns a summary of findings.
    """
    try:
        # Use `ps aux` to list all running processes
        output = subprocess.check_output(["ps", "aux"], text=True)
        lines = output.strip().split("\n")

        if len(lines) <= 1:
            return "No running processes found."

        # Example: Filter for processes using 'high CPU' or suspicious commands
        suspicious_processes = []
        for line in lines[1:]:
            if "suspicious_keyword" in line.lower() or "malware_indicator" in line.lower():
                suspicious_processes.append(line)

        if suspicious_processes:
            return "Suspicious processes detected:\n" + "\n".join(suspicious_processes)
        else:
            return "No suspicious processes detected."

    except FileNotFoundError:
        return "The 'ps' command is not available. Unable to inspect running processes."
    except Exception as e:
        return f"Error while inspecting running processes: {str(e)}"
