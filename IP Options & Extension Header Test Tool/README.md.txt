# IP Options & Extension Header Test Tool

A GUI-based network conformance testing tool built with **Scapy** and **Tkinter** to verify how network devices handle IP packets with unnecessary IPv4 options or IPv6 extension headers, as per **3GPP TS 33.117 - Section 4.2.4.1.1.3**.

![screenshot](screenshots/tool_gui.png)

---

## ✨ Features

- **IPv4 Options Testing**
  - Send TCP SYN packets with custom IP options: Record Route (RR), Timestamp, LSRR, SSRR, Stream ID, etc.

- **IPv6 Extension Header Testing**
  - Inject headers such as Hop-by-Hop, Routing, Fragment, Destination Options

- **Live Response Status**
  - Uses `sr1()` to determine if packet was acknowledged
  - Statuses include: `Passed`, `Dropped or No ACK`, `Failed`

- **User-Friendly GUI**
  - Built in Tkinter for cross-platform use

- **Evidence Export**
  - Export structured test results to **HTML** report
  - Save all transmitted packets as **PCAP** file

- **Signed Output**
  - Test tool GUI and reports include `Made by sudoninja` signature

---



This tool is designed to support:

> **Test Case: TC_HANDLING-IP-OPTIONS-AND-EXTENSIONS**  
> "IP packets with unnecessary options or extension headers shall not be processed"

Used to:
- Verify that DUT drops or ignores IP packets containing IP Options or Extension Headers
- Collect evidence for compliance validation

---

## 📁 Folder Structure

```
/
├── ip_option_test_tool.py
├── README.md
├── /screenshots
├── /pcaps
├── /reports
```

---

## 🚀 How to Run

### Requirements
- Python 3.7+
- `scapy`
- `tkinter` (included by default)

### Install dependencies
```bash
pip install scapy
```

### Launch tool
```bash
python ip_option_test_tool.py
```

---

## 🔍 Example Evidence Export

- `test_report.html` - lists each packet sent with timestamp, test type, and result
- `test_capture.pcap` - can be loaded into Wireshark for packet-level inspection

---

## 📣 Contributions

Pull requests, feedback, and feature ideas are welcome!

---

## ⚖️ License

This project is licensed under the **MIT License**.

---

### 📄 Created by: **sudoninja**

