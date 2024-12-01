from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from collections import defaultdict
import logging
import concurrent.futures
import os
from core import (
    ports,
    permissions,
    packages,
    users,
    processes,
    services,
    firewall,
    logs,
    kernel,
    security_config
)
from core.report import generate_report

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # Replace with a secure key for production

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from collections import defaultdict
import concurrent.futures
import os
import logging
from core import (
    ports,
    permissions,
    packages,
    users,
    processes,
    services,
    firewall,
    logs,
    kernel,
    security_config
)

logger = logging.getLogger(__name__)

class SecurityAudit:
    def __init__(self):
        """
        Initialize the SecurityAudit class with a dictionary of security checks 
        and a results dictionary to store the outputs.
        """
        self.results = defaultdict(lambda: "No result available")
        self.checks = {
            "open_ports": ports.check_open_ports,
            "file_permissions": permissions.verify_file_permissions,
            "installed_packages": packages.audit_installed_packages,
            "user_accounts": users.analyze_user_accounts,
            "running_processes": processes.inspect_running_processes,
            "unnecessary_services": services.check_unnecessary_services,
            "firewall_rules": firewall.verify_firewall_rules,
            "system_logs": logs.audit_system_logs,
            "kernel_vulnerabilities": kernel.check_kernel_vulnerabilities,
            "security_config": security_config.inspect_security_configurations,
        }

    def validate_check_name(self, check_name):
        """
        Validates if the given check name exists in the checks dictionary.

        :param check_name: Name of the check to validate.
        :return: True if the check name is valid, False otherwise.
        """
        return check_name in self.checks

    def run_check(self, check_name):
        """
        Run a specific security check by its name.

        :param check_name: The name of the security check to run.
        :return: The result of the security check or an error message if invalid.
        """
        if not self.validate_check_name(check_name):
            return f"Invalid check name: {check_name}"

        try:
            result = self.checks[check_name]()
            self.results[check_name] = result
            return result
        except Exception as e:
            error_message = f"Error while running {check_name}: {str(e)}"
            logger.error(error_message, exc_info=True)
            self.results[check_name] = error_message
            return error_message

    def run_all_checks(self):
        """
        Run all security checks concurrently and store their results.

        :return: None
        """
        max_workers = int(os.getenv("THREAD_POOL_SIZE", 5))  # Configurable thread pool size
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_check = {executor.submit(self.checks[check_name]): check_name for check_name in self.checks}
            for future in concurrent.futures.as_completed(future_to_check):
                check_name = future_to_check[future]
                try:
                    self.results[check_name] = future.result()
                except Exception as e:
                    error_message = f"Error while running {check_name}: {str(e)}"
                    logger.error(error_message, exc_info=True)
                    self.results[check_name] = error_message



security_audit = SecurityAudit()

# Sample user credentials (replace with database in production)
USER_CREDENTIALS = {
    "admin": "password123"
}

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Login required decorator
def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

# Protected routes
@app.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    per_page = int(os.getenv("PER_PAGE", 5))
    total_results = len(security_audit.results)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = list(security_audit.results.items())[start:end]
    total_pages = (total_results + per_page - 1) // per_page

    return render_template(
        "index.html",
        checks=security_audit.checks.keys(),
        results=dict(paginated_results),
        page=page,
        total_pages=total_pages
    )

@app.route("/run_all_checks", methods=["POST"])
@login_required
def run_all_checks():
    try:
        security_audit.run_all_checks()  # Correct method call
        results = {check: result for check, result in security_audit.results.items()}
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        logger.error("Error in /run_all_checks", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/run_selected_checks", methods=["POST"])
@login_required
def run_selected_checks():
    try:
        data = request.get_json()
        if not data or "checks" not in data:
            return jsonify({"status": "error", "message": "No checks provided."}), 400

        selected_checks = data["checks"]
        if not selected_checks:
            return jsonify({"status": "error", "message": "No checks selected."}), 400

        results = {}
        for check_name in selected_checks:
            if security_audit.validate_check_name(check_name):
                results[check_name] = security_audit.run_check(check_name)
            else:
                results[check_name] = f"Invalid check name: {check_name}"

        return jsonify({"status": "success", "results": results})

    except Exception as e:
        logger.error("Error in /run_selected_checks", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/clear_results", methods=["POST"])
@login_required
def clear_results():
    security_audit.results.clear()
    return jsonify({"status": "success", "message": "Results cleared successfully."})

@app.route("/report")
@login_required
def report():
    report_data = generate_report(security_audit.results)
    return render_template("report.html", report=report_data)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 36261))
    app.run(debug=True, host="0.0.0.0", port=port)


