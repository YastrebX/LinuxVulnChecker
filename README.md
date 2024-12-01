# **Linux Vuln Checker**

A Python-based web application for auditing the security of Linux systems. This tool helps system administrators identify vulnerabilities, analyze configurations, and generate comprehensive reports for system hardening.

---

## **Features**

- **Authentication**: Secure login system to restrict access.
- **Modular Security Checks**:
  - Open ports and unnecessary services.
  - File permissions audit.
  - Installed packages analysis for outdated or vulnerable packages.
  - User accounts inspection for inactive or unprotected accounts.
  - Running processes inspection for malware or suspicious activity.
  - Unnecessary services audit.
  - Firewall rules verification.
  - System logs analysis for suspicious entries.
  - Kernel vulnerabilities detection.
  - Security configurations audit, including SSH settings and SELinux/AppArmor status.
- **Dynamic Report Generation**: Comprehensive reports with recommendations for remediation.
- **Clear Results**: Reset the results to run fresh audits.
- **Web Interface**: Easy-to-use interface for managing audits and viewing reports.

---

## **Getting Started**

### **Prerequisites**
- Linux operating system for security auditing.
- Python 3.8 or higher.
- A virtual environment (optional but recommended).

---

### **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YastrebX/LinuxVulnChecker.git
   cd LinuxVulnChecker
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following content:
   ```
   SECRET_KEY=your_secret_key
   THREAD_POOL_SIZE=5
   ```

5. **Run the Application**:
   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:36261`.

---

## **Usage**

#### **Authentication**
1. Navigate to the login page: `http://127.0.0.1:36261/login`.
2. Log in using default credentials(you should change them):
   - Username: `admin`
   - Password: `password123`.

#### **Dashboard**
- **Run All Checks**: Perform all security audits in one click.
- **Run Selected Checks**: Choose specific checks to run.
- **View Full Report**: Access detailed security findings and recommendations.

#### **Clear Results**
- Use the "Clear Results" button to reset the audit results and start fresh.

---

## **File Structure**

```plaintext
.
├── app.py                # Main Flask application
├── core/                 # Core security check modules
│   ├── ports.py          # Open ports check
│   ├── permissions.py    # File permissions check
│   ├── packages.py       # Installed packages audit
│   ├── users.py          # User accounts analysis
│   ├── processes.py      # Running processes inspection
│   ├── services.py       # Unnecessary services check
│   ├── firewall.py       # Firewall rules verification
│   ├── logs.py           # System logs audit
│   ├── kernel.py         # Kernel vulnerabilities check
│   ├── security_config.py # Security configurations inspection
│   └── report.py         # Report generation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Dashboard template
│   ├── report.html       # Report page template
│   ├── login.html        # Login page template
├── static/               # Static files
│   ├── js/
│   │   ├── index.js      # Frontend JavaScript logic
│   │   └── script.js     # Additional JavaScript logic
│   └── css/
│       └── style.css     # Custom styles for the web interface
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .env                  # Environment variables
```

---

## **Testing**

1. **Run All Security Checks**:
   ```bash
   curl -X POST http://127.0.0.1:5000/run_all_checks
   ```

2. **Run Specific Security Checks**:
   ```bash
   curl -X POST http://127.0.0.1:5000/run_selected_checks \
        -H "Content-Type: application/json" \
        -d '{"checks": ["open_ports", "file_permissions"]}'
   ```

3. **Clear Results**:
   ```bash
   curl -X POST http://127.0.0.1:5000/clear_results
   ```

4. **Access Full Report**:
   Navigate to `http://127.0.0.1:5000/report`.

---

## **Customization**

### **Adding New Checks**
1. Create a new file in the `core/` directory (e.g., `my_check.py`).
2. Implement your custom check as a function.
3. Register the new check in the `SecurityAudit` class:
   ```python
   self.checks["my_custom_check"] = my_check_function
   ```

---

## **Deployment**

1. **Production Server**:
   Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn -w 4 app:app
   ```

2. **Reverse Proxy**:
   Set up Nginx or Apache as a reverse proxy for secure access.

3. **HTTPS**:
   Use a TLS certificate (e.g., via Let's Encrypt) to secure your application.

---

## **Security Recommendations**

- Replace the default `SECRET_KEY` with a strong, unique value.
- Use HTTPS for secure communication in production.
- Regularly update the dependencies in `requirements.txt` to avoid vulnerabilities.

---

## **Contributing**

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.