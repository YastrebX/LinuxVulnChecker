def generate_report(findings):
    """
    Generates a structured security audit report.
    Accepts a dictionary of findings from various system checks.
    Returns a formatted report as a single string.
    """
    report_lines = []
    severity_map = {
        "open_ports": "High",
        "file_permissions": "Medium",
        "installed_packages": "High",
        "user_accounts": "Medium",
        "running_processes": "High",
        "unnecessary_services": "Low",
        "firewall_rules": "High",
        "system_logs": "Medium",
        "kernel_vulnerabilities": "High",
        "security_config": "High",
    }

    if not findings:
        return "No results available. Please run checks before generating a report."

    for check, result in findings.items():
        severity = severity_map.get(check, "Unknown")
        report_lines.append(f"Check: {check.replace('_', ' ').title()}")
        report_lines.append(f"Severity: {severity}")
        if isinstance(result, str):
            report_lines.append(f"Result:\n{result}")
        else:
            report_lines.append(f"Result:\n{str(result)}")
        report_lines.append("-" * 40)  # Separator for readability

    return "\n".join(report_lines)

