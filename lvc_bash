#!/bin/bash

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root."
  exit
fi

echo "Starting Linux system security check..."

# 1. Check for users with empty passwords
echo "1. Checking for users with empty passwords..."
awk -F: '($2 == "") {print $1}' /etc/shadow
if [ $? -eq 0 ]; then
  echo "Empty password check completed."
else
  echo "No users with empty passwords found."
fi
echo

# 2. Check for world-writable files (except for /proc)
echo "2. Checking for world-writable files..."
find / -xdev -type f -perm -0002 2>/dev/null
echo "World-writable files check completed."
echo

# 3. Check for active listening services
echo "3. Checking active listening services..."
netstat -tuln
echo "Active listening services check completed."
echo

# 4. Check for installed and enabled firewall (UFW as example)
echo "4. Checking if firewall (UFW) is active..."
ufw status | grep -q "Status: active"
if [ $? -eq 0 ]; then
  echo "UFW is active."
else
  echo "UFW is not active! Consider enabling it."
fi
echo

# 5. Check for unnecessary SUID/SGID files
echo "5. Checking for unnecessary SUID/SGID files..."
find / -perm /6000 -type f 2>/dev/null
echo "SUID/SGID files check completed."
echo

# 6. Check for insecure SSH configuration
echo "6. Checking SSH configuration..."
grep -E "PermitRootLogin|PasswordAuthentication" /etc/ssh/sshd_config
echo "SSH configuration check completed."
echo

# 7. Check for outdated packages
echo "7. Checking for outdated packages..."
apt list --upgradable 2>/dev/null
echo "Outdated package check completed."
echo

# 8. Check for weak file permissions in home directories
echo "8. Checking for weak file permissions in home directories..."
for dir in /home/*; do
  if [ -d "$dir" ]; then
    perms=$(stat -c "%A" "$dir")
    if [[ "$perms" =~ "w" ]]; then
      echo "Warning: $dir has weak permissions: $perms"
    fi
  fi
done
echo "Weak permissions check completed."
echo

echo "Linux security check completed."

