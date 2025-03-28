import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from fpdf import FPDF
import datetime

class HTTPMethodTester:
    def __init__(self, root):
        self.root = root
        self.root.title("HTTP Method Tester v1.0")

        # URL Input
        ttk.Label(root, text="Target URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # Test Button
        self.test_button = ttk.Button(root, text="Test Methods", command=self.test_methods)
        self.test_button.grid(row=0, column=2, padx=5, pady=5)

        # Output Box
        self.output = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled')
        self.output.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Export Buttons
        self.export_html_button = ttk.Button(root, text="Export as HTML", command=self.export_html)
        self.export_html_button.grid(row=2, column=0, padx=5, pady=5)

        self.export_pdf_button = ttk.Button(root, text="Export as PDF", command=self.export_pdf)
        self.export_pdf_button.grid(row=2, column=1, padx=5, pady=5)

        # Signature label in bottom-right corner
        self.signature = ttk.Label(root, text="Made by sudoninja", font=("Arial", 9, "italic"))
        self.signature.grid(row=2, column=2, padx=5, pady=5, sticky="e")

        self.results = []

    def test_methods(self):
        target_url = self.url_entry.get().strip()
        if not target_url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        self.results.clear()
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'CONNECT', 'PATCH']
        self.output.config(state='normal')
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"Testing HTTP methods for {target_url}\n\n")

        for method in methods:
            try:
                response = requests.request(method, target_url, timeout=5)
                result = f"{method}: {response.status_code} {response.reason}"
            except Exception as e:
                result = f"{method}: Error - {str(e)}"
            self.output.insert(tk.END, result + "\n")
            self.results.append(result)

        self.output.config(state='disabled')

    def export_html(self):
        if not self.results:
            messagebox.showinfo("No Data", "No results to export. Please run a test first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if not file_path:
            return

        with open(file_path, "w") as f:
            f.write("<html><head><title>HTTP Method Test Report</title></head><body>")
            f.write(f"<h2>HTTP Method Test Report</h2><p><b>Target:</b> {self.url_entry.get()}</p><ul>")
            for result in self.results:
                f.write(f"<li>{result}</li>")
            f.write("</ul><p>Generated on: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "</p>")
            f.write("<p style='text-align:right; font-style:italic;'>Made by sudoninja</p>")
            f.write("</body></html>")

        messagebox.showinfo("Success", f"HTML report saved to:\n{file_path}")

    def export_pdf(self):
        if not self.results:
            messagebox.showinfo("No Data", "No results to export. Please run a test first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="HTTP Method Test Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Target: {self.url_entry.get()}", ln=True)
        pdf.ln(5)

        for result in self.results:
            pdf.multi_cell(0, 10, txt=result)

        pdf.ln(10)
        pdf.cell(200, 10, txt="Generated on: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt="Made by sudoninja", ln=True, align='R')

        pdf.output(file_path)
        messagebox.showinfo("Success", f"PDF report saved to:\n{file_path}")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HTTPMethodTester(root)
    root.mainloop()
