import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from scapy.all import *
import socket
import threading
import datetime
import json
import csv
import os

# ===== Default Test Config =====
DEFAULT_IPV4 = "192.0.2.1"
DEFAULT_IPV6 = "2001:db8::1"
DEFAULT_IFACE = "eth0"
DEFAULT_PORT = 80

sent_packets = []
test_results = []  # Store structured results: (timestamp, description, status)

# ===== IP Option and Extension Header Mappings =====
ipv4_options = {
    "End of Option List (EOL)": IPOption(b'\x00'),
    "No Operation (NOP)": IPOption(b'\x01'),
    "Record Route (RR)": IPOption(b'\x07\x07\x04'),
    "Timestamp": IPOption(b'\x44\x08\x04\x00\x00\x00\x00\x00'),
    "Loose Source Route (LSRR)": IPOption(b'\x83\x07\x04' + socket.inet_aton(DEFAULT_IPV4)),
    "Strict Source Route (SSRR)": IPOption(b'\x89\x07\x04' + socket.inet_aton(DEFAULT_IPV4)),
    "Security": IPOption(b'\x94\x04\x00\x00'),
    "Stream ID": IPOption(b'\x95\x06\x00\x00\x00\x00'),
}

ipv6_ext_headers = {
    "Hop-by-Hop Options": IPv6ExtHdrHopByHop(),
    "Routing Header": IPv6ExtHdrRouting(),
    "Fragment Header": IPv6ExtHdrFragment(),
    "Destination Options": IPv6ExtHdrDestOpt(),
}

# ===== GUI App Class =====
class IPTestTool:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Option & Extension Header Test Tool")
        self.notebook = ttk.Notebook(self.root)
        self.ipv4_tab = tk.Frame(self.notebook)
        self.ipv6_tab = tk.Frame(self.notebook)
        self.notebook.add(self.ipv4_tab, text="IPv4 Options")
        self.notebook.add(self.ipv6_tab, text="IPv6 Extensions")
        self.notebook.pack(fill='both', expand=True)

        self.build_ipv4_tab()
        self.build_ipv6_tab()
        self.build_logger()
        self.build_export_buttons()
        self.build_footer()

    def build_ipv4_tab(self):
        tk.Label(self.ipv4_tab, text="IPv4 Address:").grid(row=0, column=0, sticky='e')
        self.ipv4_var = tk.StringVar(value=DEFAULT_IPV4)
        tk.Entry(self.ipv4_tab, textvariable=self.ipv4_var, width=30).grid(row=0, column=1)

        tk.Label(self.ipv4_tab, text="Interface:").grid(row=1, column=0, sticky='e')
        self.iface_var = tk.StringVar(value=DEFAULT_IFACE)
        tk.Entry(self.ipv4_tab, textvariable=self.iface_var, width=30).grid(row=1, column=1)

        tk.Label(self.ipv4_tab, text="Port:").grid(row=2, column=0, sticky='e')
        self.port_var = tk.StringVar(value=str(DEFAULT_PORT))
        tk.Entry(self.ipv4_tab, textvariable=self.port_var, width=30).grid(row=2, column=1)

        tk.Label(self.ipv4_tab, text="IPv4 Option:").grid(row=3, column=0, sticky='e')
        self.ipv4_option_var = tk.StringVar()
        ipv4_option_menu = ttk.Combobox(self.ipv4_tab, textvariable=self.ipv4_option_var, values=list(ipv4_options.keys()), width=28)
        ipv4_option_menu.grid(row=3, column=1)
        ipv4_option_menu.current(2)

        send_btn = tk.Button(self.ipv4_tab, text="Send IPv4 Packet", command=lambda: threading.Thread(target=self.send_ipv4_packet).start())
        send_btn.grid(row=4, column=0, columnspan=2, pady=5)

    def build_ipv6_tab(self):
        tk.Label(self.ipv6_tab, text="IPv6 Address:").grid(row=0, column=0, sticky='e')
        self.ipv6_var = tk.StringVar(value=DEFAULT_IPV6)
        tk.Entry(self.ipv6_tab, textvariable=self.ipv6_var, width=30).grid(row=0, column=1)

        tk.Label(self.ipv6_tab, text="Interface:").grid(row=1, column=0, sticky='e')
        self.iface6_var = tk.StringVar(value=DEFAULT_IFACE)
        tk.Entry(self.ipv6_tab, textvariable=self.iface6_var, width=30).grid(row=1, column=1)

        tk.Label(self.ipv6_tab, text="Port:").grid(row=2, column=0, sticky='e')
        self.port6_var = tk.StringVar(value=str(DEFAULT_PORT))
        tk.Entry(self.ipv6_tab, textvariable=self.port6_var, width=30).grid(row=2, column=1)

        tk.Label(self.ipv6_tab, text="IPv6 Extension:").grid(row=3, column=0, sticky='e')
        self.ipv6_ext_var = tk.StringVar()
        ipv6_ext_menu = ttk.Combobox(self.ipv6_tab, textvariable=self.ipv6_ext_var, values=list(ipv6_ext_headers.keys()), width=28)
        ipv6_ext_menu.grid(row=3, column=1)
        ipv6_ext_menu.current(1)

        send_btn = tk.Button(self.ipv6_tab, text="Send IPv6 Packet", command=lambda: threading.Thread(target=self.send_ipv6_packet).start())
        send_btn.grid(row=4, column=0, columnspan=2, pady=5)

    def build_logger(self):
        tk.Label(self.root, text="Log Output:").pack()
        self.output_text = scrolledtext.ScrolledText(self.root, height=10)
        self.output_text.pack(fill='both', expand=True)

    def build_export_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Button(frame, text="Export Log to HTML", command=self.export_html).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Export Packets to PCAP", command=self.export_pcap).pack(side=tk.LEFT, padx=5)

    def build_footer(self):
        footer = tk.Label(self.root, text="Made by sudoninja", anchor='e', fg="gray")
        footer.pack(fill='x', side='bottom', padx=10, pady=3)

    def log(self, msg, status="Sent"):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        line = f"{timestamp} {msg}"
        self.output_text.insert(tk.END, line + f" | Status: {status}\n")
        self.output_text.see(tk.END)
        test_results.append((timestamp, msg, status))

    def send_ipv4_packet(self):
        try:
            option = ipv4_options[self.ipv4_option_var.get()]
            pkt = IP(dst=self.ipv4_var.get(), options=[option]) / TCP(dport=int(self.port_var.get()), flags="S")
            response = sr1(pkt, iface=self.iface_var.get(), timeout=2, verbose=False)
            sent_packets.append(pkt)
            status = "Passed" if response and response.haslayer(TCP) and response.getlayer(TCP).flags == "SA" else "Dropped or No ACK"
            self.log(f"Sent IPv4 packet with option: {self.ipv4_option_var.get()}", status=status)
        except Exception as e:
            self.log(f"Error sending IPv4: {str(e)}", status="Failed")

    def send_ipv6_packet(self):
        try:
            ext = ipv6_ext_headers[self.ipv6_ext_var.get()]
            pkt = IPv6(dst=self.ipv6_var.get()) / ext / TCP(dport=int(self.port6_var.get()), flags="S")
            response = sr1(pkt, iface=self.iface6_var.get(), timeout=2, verbose=False)
            sent_packets.append(pkt)
            status = "Passed" if response and response.haslayer(TCP) and response.getlayer(TCP).flags == "SA" else "Dropped or No ACK"
            self.log(f"Sent IPv6 packet with extension: {self.ipv6_ext_var.get()}", status=status)
        except Exception as e:
            self.log(f"Error sending IPv6: {str(e)}", status="Failed")

    def export_html(self):
        path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if not path:
            return
        with open(path, "w") as f:
            f.write("<html><body><h2>IP Option & Extension Header Test Report</h2>")
            f.write("<table border='1' cellpadding='5'><tr><th>Timestamp</th><th>Description</th><th>Status</th></tr>")
            for timestamp, desc, status in test_results:
                f.write(f"<tr><td>{timestamp}</td><td>{desc}</td><td>{status}</td></tr>")
            f.write("</table><br><div style='text-align:right;color:gray;'>Made by sudoninja</div></body></html>")
        self.log(f"Exported test report to HTML: {path}", status="Report Saved")

    def export_pcap(self):
        path = filedialog.asksaveasfilename(defaultextension=".pcap", filetypes=[("PCAP files", "*.pcap")])
        if not path:
            return
        wrpcap(path, sent_packets)
        self.log(f"Exported packets to PCAP: {path}", status="PCAP Saved")

if __name__ == '__main__':
    root = tk.Tk()
    app = IPTestTool(root)
    root.mainloop()
