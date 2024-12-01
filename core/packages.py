import subprocess

def audit_installed_packages():
    """
    Checks for outdated packages or packages with known vulnerabilities.
    Returns a summary of findings.
    """
    try:
        # Use `apt list --upgradable` for Debian/Ubuntu-based systems
        output = subprocess.check_output(["apt", "list", "--upgradable"], text=True)
        lines = output.strip().split("\n")
        
        if len(lines) <= 1:
            return "All installed packages are up-to-date."
        
        upgradable_packages = lines[1:]
        return "Outdated packages:\n" + "\n".join(upgradable_packages)

    except FileNotFoundError:
        return "The 'apt' command is not available. This check supports Debian/Ubuntu-based systems only."
    except Exception as e:
        return f"Error while auditing installed packages: {str(e)}"
