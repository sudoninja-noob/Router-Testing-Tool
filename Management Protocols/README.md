# 🔐 Mutual Authentication GUI Tool

This is a lightweight Python-based GUI application designed to test **mutual authentication** for common management protocols used in network products.

### ✅ Supported Protocols

- **HTTPS with TLS (Mutual TLS):**
  - Validates client certificate support
  - Uses CA cert to verify server identity

- **SSH:**
  - Supports both **username/password** and **key-based** authentication

- **SNMPv3:**
  - Supports authentication (authKey) and optional encryption (privKey)
  - Tests access to `sysDescr` OID for validation

### 🖥 Built With

- **Python 3**
- **Tkinter** (standard GUI)
- **Paramiko** (for SSH)
- **PySNMP** (for SNMPv3)
- **Socket & SSL** (for HTTPS mutual TLS)

---

### 🚀 How to Run

1. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the GUI:
   ```bash
   python mutual_auth.py
   ```


### 💡 Features

- Clean GUI with input validation
- Browse file dialogs for certificate/key selection
- Green border & signature branding (`Made by sudoninja`)
- Outputs real-time test results in the window

---

### ✍️ Author

**Made by sudoninja
