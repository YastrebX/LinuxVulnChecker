import os
import stat

def verify_file_permissions():
    """
    Identifies files and directories with overly permissive permissions
    (e.g., world-writable files). Excludes system directories and provides a manageable output.
    Returns a list of files or directories with issues.
    """
    # Directories to exclude from the scan
    exclude_dirs = {"/proc", "/dev", "/sys", "/run", "/tmp", "/var/tmp", "/mnt", "/media"}

    # Directories to prioritize in the scan
    include_dirs = ["/home", "/etc", "/var/log"]

    findings = []
    seen_inodes = set()  # Track processed inodes to avoid duplicate processing

    def scan_directory(directory):
        """
        Scans a single directory for overly permissive file permissions.
        """
        for dirpath, dirnames, filenames in os.walk(directory, followlinks=False):
            # Skip directories in the exclusion list
            if any(excluded in dirpath for excluded in exclude_dirs):
                continue

            for name in dirnames + filenames:
                try:
                    full_path = os.path.join(dirpath, name)
                    file_stat = os.lstat(full_path)  # Use lstat to avoid following symbolic links

                    # Skip if the inode has been processed (avoid loops)
                    if file_stat.st_ino in seen_inodes:
                        continue
                    seen_inodes.add(file_stat.st_ino)

                    # Check if the file or directory is world-writable
                    if file_stat.st_mode & stat.S_IWOTH:
                        findings.append(full_path)

                except (PermissionError, FileNotFoundError):
                    # Ignore files or directories that cannot be accessed
                    continue
                except OSError as e:
                    # Handle other OS-level errors
                    findings.append(f"Skipped {full_path} due to error: {str(e)}")
                    continue

    # Scan only the prioritized directories
    for directory in include_dirs:
        if os.path.exists(directory):
            scan_directory(directory)

    if not findings:
        return "No overly permissive file permissions found."

    return "Files or directories with overly permissive permissions:\n" + "\n".join(findings)


