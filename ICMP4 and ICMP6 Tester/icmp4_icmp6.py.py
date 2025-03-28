import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import os
import subprocess
import json
import csv
from scapy.all import IP, ICMP, sr1
import openpyxl

ICMP_TYPES = [
    ("Echo Reply", 0),
    ("Destination Unreachable", 3),
    ("Echo Request", 8),
    ("Time Exceeded", 11),
    ("Parameter Problem", 12),
    ("Redirect", 5),
    ("Timestamp", 13),
    ("Timestamp Reply", 14),
    ("Router Solicitation (IPv6)", 133),
    ("Router Advertisement (IPv6)", 134),
    ("Neighbor Solicitation (IPv6)", 135),
    ("Neighbor Advertisement (IPv6)", 136),
    ("Packet Too Big (IPv6)", 2),
]

class ICMPTesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ICMP4 and ICMP6 Test Tool v1.0")
        self.root.geometry("800x550")
        self.root.configure(bg="lightgreen", highlightbackground="green", highlightthickness=5)

        self.results = []

        self.setup_widgets()

    def setup_widgets(self):
        frm_top = tk.Frame(self.root, bg="lightgreen")
        frm_top.pack(pady=10)

        tk.Label(frm_top, text="Target IP:", bg="lightgreen").grid(row=0, column=0, padx=5)
        self.entry_ip = tk.Entry(frm_top)
        self.entry_ip.grid(row=0, column=1, padx=5)

        tk.Label(frm_top, text="ICMP Type:", bg="lightgreen").grid(row=0, column=2, padx=5)
        self.icmp_type_var = tk.StringVar()
        self.icmp_type_menu = ttk.Combobox(frm_top, textvariable=self.icmp_type_var,
            values=[f"{desc} (Type {type_})" for desc, type_ in ICMP_TYPES])
        self.icmp_type_menu.grid(row=0, column=3, padx=5)
        self.icmp_type_menu.current(2)  # Default to Echo Request

        tk.Button(frm_top, text="Start Test", command=self.run_test).grid(row=0, column=4, padx=5)
        tk.Button(frm_top, text="Export HTML", command=self.export_html).grid(row=0, column=5, padx=5)
        tk.Button(frm_top, text="Export PDF", command=self.export_pdf).grid(row=0, column=6, padx=5)
        tk.Button(frm_top, text="Export Excel", command=self.export_excel).grid(row=0, column=7, padx=5)

        frm_save = tk.Frame(self.root, bg="lightgreen")
        frm_save.pack(pady=5)
        tk.Button(frm_save, text="Save Session (JSON)", command=self.save_json).pack(side=tk.LEFT, padx=10)
        tk.Button(frm_save, text="Load Session (JSON)", command=self.load_json).pack(side=tk.LEFT, padx=10)
        tk.Button(frm_save, text="Save Session (CSV)", command=self.save_csv).pack(side=tk.LEFT, padx=10)
        tk.Button(frm_save, text="Load Session (CSV)", command=self.load_csv).pack(side=tk.LEFT, padx=10)

        self.tree = ttk.Treeview(self.root, columns=("Type", "Response", "Status"), show='headings')
        self.tree.heading("Type", text="ICMP Type")
        self.tree.heading("Response", text="Response Summary")
        self.tree.heading("Status", text="Result")
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        footer = tk.Label(self.root, text="Made by sudoninja", anchor='se', bg="lightgreen", fg="darkgreen")
        footer.pack(side='bottom', anchor='e', padx=10, pady=5)

    def run_test(self):
        target_ip = self.entry_ip.get().strip()
        icmp_selection = self.icmp_type_menu.get()

        if not target_ip or not icmp_selection:
            messagebox.showerror("Input Error", "Please enter a target IP and select ICMP type.")
            return

        try:
            icmp_code = int(icmp_selection.split("Type")[-1].strip(" )"))
        except ValueError:
            messagebox.showerror("Type Error", "Unable to parse ICMP type.")
            return

        pkt = IP(dst=target_ip)/ICMP(type=icmp_code)
        response = sr1(pkt, timeout=2, verbose=0)

        if response:
            summary = response.summary()
            result = "Test Passed" if icmp_code in [0, 8, 3, 11, 12] else "Check Configuration"
        else:
            summary = "No response received."
            result = "Not Responding"

        self.results.append((icmp_selection, summary, result))
        self.tree.insert("", "end", values=(icmp_selection, summary, result))

    def export_html(self):
        filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write("""
            <html><head><title>ICMP Test Results</title></head><body>
            <h2>ICMP Packet Test Results</h2>
            <table border="1" cellpadding="5">
            <tr><th>ICMP Type</th><th>Response</th><th>Result</th></tr>
            """)
            for row in self.results:
                f.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n")
            f.write("""</table><br><i>Generated: """ + str(datetime.datetime.now()) + "</i></body></html>")

        messagebox.showinfo("Export", f"Results saved to {filename}")

    def export_pdf(self):
        try:
            import pdfkit
        except ImportError:
            messagebox.showerror("Missing Dependency", "pdfkit is not installed.")
            return

        html_path = "temp_icmp_report.html"
        self.export_html_temp(html_path)

        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not pdf_path:
            return

        try:
            pdfkit.from_file(html_path, pdf_path)
            messagebox.showinfo("Export", f"PDF saved to {pdf_path}")
        except Exception as e:
            messagebox.showerror("PDF Error", str(e))
        finally:
            if os.path.exists(html_path):
                os.remove(html_path)

    def export_html_temp(self, path):
        with open(path, 'w') as f:
            f.write("""
            <html><head><title>ICMP Test Results</title></head><body>
            <h2>ICMP Packet Test Results</h2>
            <table border="1" cellpadding="5">
            <tr><th>ICMP Type</th><th>Response</th><th>Result</th></tr>
            """)
            for row in self.results:
                f.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n")
            f.write("""</table><br><i>Generated: """ + str(datetime.datetime.now()) + "</i></body></html>")

    def export_excel(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not filename:
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "ICMP Results"
        ws.append(["ICMP Type", "Response Summary", "Result"])

        for row in self.results:
            ws.append(row)

        wb.save(filename)
        messagebox.showinfo("Export", f"Excel file saved to {filename}")

    def save_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not filename:
            return
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        messagebox.showinfo("Save", f"Session saved to {filename}")

    def load_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filename:
            return
        with open(filename, 'r') as f:
            self.results = json.load(f)
        self.refresh_tree()
        messagebox.showinfo("Load", f"Session loaded from {filename}")

    def save_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not filename:
            return
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ICMP Type", "Response Summary", "Result"])
            writer.writerows(self.results)
        messagebox.showinfo("Save", f"CSV saved to {filename}")

    def load_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filename:
            return
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            self.results = list(reader)
        self.refresh_tree()
        messagebox.showinfo("Load", f"CSV loaded from {filename}")

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.results:
            self.tree.insert("", "end", values=row)

if __name__ == '__main__':
    root = tk.Tk()
    app = ICMPTesterGUI(root)
    root.mainloop()
