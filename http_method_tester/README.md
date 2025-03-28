```markdown
# HTTP Method Tester GUI Tool

A lightweight Python GUI tool to test supported HTTP methods (`GET`, `POST`, `PUT`, etc.) on any web server and generate reports in **HTML** and **PDF** formats.

---

## 📌 Features

- GUI-based tool using Tkinter
- Test all standard HTTP methods
- Displays status codes and reasons
- Export results to:
  - ✅ HTML report
  - ✅ PDF report
- Scrollable interface for easy result viewing

---

## 🚀 Use Case

Useful for:

- Web application and API testing
- Security testing and recon
- DevOps / QA validation
- Quick compatibility checks of allowed HTTP verbs

---

## 🔧 Installation

### 1. Clone the repo

```bash
git clone 
cd http-method-tester
```

### 2. Install dependencies

```bash
pip install requests fpdf
```

### 3. Run the tool

```bash
python http_method_tester_gui.py
```

---

## 📄 Sample HTML Report

```html
<ul>
  <li>GET: 200 OK</li>
  <li>POST: 405 Method Not Allowed</li>
  <li>PUT: 403 Forbidden</li>
  ...
</ul>
```

---

## 📘 How it Works

- Enter a target URL in the GUI.
- Click "Test Methods".
- The tool sends HTTP requests with various methods.
- Results are shown with status codes and reasons.
- Reports can be exported as HTML or PDF.

---

## 💡 Benefits

- No command line needed – beginner friendly
- Fast and simple for quick HTTP diagnostics
- Portable – runs on any system with Python
- Great for internal pen testing or bug bounty setups

---

## 📜 License

MIT License – feel free to use, modify, and contribute!

---

## 🤝 Contribute

Want to add new features (like CSV/Excel export, headers, proxy config)? PRs are welcome!

---

## 🧑‍💻 Author

**Sudoninja**  
