import subprocess

def check_open_ports():
    """
    Uses the 'ss' command to list open ports and their associated services.
    Returns a formatted string or list of findings.
    """
    try:
        # Check for open ports using `ss`
        output = subprocess.check_output(["ss", "-tuln"], text=True)
        lines = output.strip().split("\n")
        
        if len(lines) <= 1:
            return "No open ports detected."

        return "\n".join(lines)
    except FileNotFoundError:
        return "The 'ss' command is not available. Please install 'iproute2'."
    except Exception as e:
        return f"Error while checking open ports: {str(e)}"
