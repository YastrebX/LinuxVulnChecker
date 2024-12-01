import subprocess

def analyze_user_accounts():
    """
    Analyzes user accounts for potential security issues such as inactive accounts
    or accounts without passwords.
    Returns a summary of findings.
    """
    findings = []

    try:
        # Check for inactive accounts
        inactive_users = subprocess.check_output(
            ["lastlog", "--time", "90"], text=True
        ).strip().split("\n")
        
        if len(inactive_users) > 1:
            findings.append("Inactive users (no login in 90 days):\n" + "\n".join(inactive_users[1:]))
        else:
            findings.append("No inactive users found.")

        # Check for accounts with empty passwords
        passwd_file = "/etc/shadow"
        with open(passwd_file, "r") as f:
            for line in f:
                user, password, *_ = line.split(":")
                if password == "!" or password == "":
                    findings.append(f"User '{user}' has no password set.")
        
    except FileNotFoundError:
        findings.append("Required command or file not found for user account analysis.")
    except Exception as e:
        findings.append(f"Error while analyzing user accounts: {str(e)}")

    return "\n".join(findings) if findings else "No user account issues detected."
