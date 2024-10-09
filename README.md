# Linux Security Check Script

This bash script performs basic security checks on a Linux system to identify common vulnerabilities and misconfigurations. It is intended to help improve the security posture of a home Linux PC by checking for weak passwords, unnecessary services, file permissions, and other potential security issues.

## Features

The script performs the following checks:

1. **Empty Passwords:** Identifies any users that have no password set, which can be a serious security risk.
2. **World-Writable Files:** Lists files that are world-writable (i.e., writable by anyone), which could allow malicious modifications.
3. **Listening Services:** Displays all active listening services to help you identify any unnecessary or vulnerable services running on your system.
4. **Firewall (UFW) Status:** Checks if the Uncomplicated Firewall (UFW) is active. If it's not, you will be prompted to enable it for better security.
5. **SUID/SGID Files:** Searches for files with SUID or SGID bits set, which can allow privilege escalation if not properly managed.
6. **SSH Configuration:** Checks for insecure SSH settings, such as `PermitRootLogin` and `PasswordAuthentication`, that could weaken remote access security.
7. **Outdated Packages:** Lists any packages that have updates available, ensuring your system is up to date with security patches.
8. **Weak Home Directory Permissions:** Verifies that home directories do not have weak permissions that could expose sensitive data.

## Requirements

- **Linux OS:** The script is designed for use on Linux-based operating systems.
- **Root/Sudo Privileges:** The script must be run as root or with sudo privileges to perform system-wide checks.

## Usage

1. Clone this repository or download the script directly.
2. Make the script executable:
   
   chmod +x security_check.sh
   
3. Run the script with root privileges:
   
   sudo ./security_check.sh
   

The script will then proceed to perform the checks and display the results on your terminal. No changes are made to the system automatically, allowing you to review the findings and take appropriate actions manually.

## Example Output


Starting Linux system security check...

1. Checking for users with empty passwords...
No users with empty passwords found.

2. Checking for world-writable files...
/tmp/testfile.txt
World-writable files check completed.

3. Checking active listening services...
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN
Active listening services check completed.

4. Checking if firewall (UFW) is active...
UFW is not active! Consider enabling it.

5. Checking for unnecessary SUID/SGID files...
/usr/bin/passwd
SUID/SGID files check completed.

...

Linux security check completed.


## Customization

You can modify or extend the script to suit your specific needs. For example, you may want to check for additional configurations (e.g., specific CVEs, specific services), add automatic fixes, or integrate more advanced security checks (like using tools such as `Lynis`, `Chkrootkit`, etc.).

## License

This project is licensed under the GPL-3.0 License

## Contributing

Feel free to submit issues, pull requests, or suggestions to improve the script.
