# 🛰️ ICMPv4 & ICMPv6 Test Tool v1.0

A **GUI-based testing utility** for sending and analyzing ICMP packets (Echo, Timestamp, Parameter Problem, etc.) for both **IPv4 and IPv6**.  
Built with **Python**, **Scapy**, and **Tkinter** — perfect for network engineers and testers.

---

## 📦 Features

- ✅ Send ICMP packets (IPv4/IPv6)
- ✅ Display packet summary and response status in real time
- ✅ Export results to:
  - 📄 HTML  
  - 📊 PDF (via pdfkit)  
  - 📑 Excel (.xlsx)
- ✅ Save/load sessions in:
  - 🔐 JSON  
  - 📋 CSV
- ✅ Clean green-themed GUI
- ✅ Built-in footer branding: **Made by sudoninja**

---

## 🚀 Installation

### Requirements

- Python 3.7+
- Dependencies:

```bash
pip install scapy openpyxl
pip install pdfkit  # For PDF export (optional)
🧪 Note: PDF generation requires wkhtmltopdf installed and accessible in your system PATH.
________________________________________
🖥️ Usage
python icmp_gui_tool.py
•	Enter a target IP address
•	Select the desired ICMP type
•	Click Start Test to send and view response
•	Use the buttons to export results or save/load sessions
________________________________________
🌐 Supported ICMP Types
Description	IPv4 Type	IPv6 Type
Echo Request	8	129
Echo Reply	0	128
Destination Unreachable	3	1
Time Exceeded	11	3
Parameter Problem	12	4
Packet Too Big	-	2
Neighbor Solicitation	-	135
Neighbor Advertisement	-	136
Router Solicitation	-	133
Router Advertisement	-	134
Timestamp / Reply	13 / 14	-
________________________________________
📂 File Structure
icmp_test_tool/
├── icmp_gui_tool.py          # Main GUI script
├── requirements.txt          # Dependency list
└── README.md                 # This file
________________________________________
📸 Screenshots
Add screenshots of the GUI here after uploading them to your repo or an image hosting service.
________________________________________
✨ Credits
Made with 💚 by sudoninja
Tool powered by:
•	Python 🐍
•	Scapy 📡
•	Tkinter 🎨
________________________________________
📄 License
This project is licensed under the MIT License.
________________________________________
🤝 Contributions
Feel free to fork, open issues, and submit pull requests!
Suggestions and feedback are welcome. 🚀

---

And your `requirements.txt` file:

scapy>=2.5.0 openpyxl>=3.1.2 pdfkit>=1.0.0
