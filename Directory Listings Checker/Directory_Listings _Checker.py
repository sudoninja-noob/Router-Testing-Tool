import requests
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import tempfile
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import threading

results_data = []
cancel_scan = False


def fetch_wayback_urls(domain):
    wayback_url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        response = requests.get(wayback_url, stream=True)
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if line:
                temp_file.write(line + "\n")
        temp_file.close()
        return temp_file.name
    except requests.exceptions.RequestException:
        return None


def extract_unique_paths(temp_file_path):
    unique_paths = set()
    with open(temp_file_path, "r", encoding="utf-8") as temp_file:
        for line in temp_file:
            url = line.strip()
            parsed_url = urlparse(url)
            path = parsed_url.path
            if path and path != "/":
                unique_paths.add(path)
    return sorted(unique_paths)


def check_directory_listing(domain, path):
    url = f"http://{domain}{path}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and "Index of /" in response.text:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


def process_domain(domain, threads):
    global cancel_scan
    results = []
    temp_file_path = fetch_wayback_urls(domain)
    if not temp_file_path:
        return results

    unique_paths = extract_unique_paths(temp_file_path)
    total_tasks = len(unique_paths)
    completed = 0
    start_time = time.time()

    progress_bar["maximum"] = total_tasks

    def update_progress():
        nonlocal completed
        elapsed = time.time() - start_time
        progress_bar["value"] = completed
        if completed > 0:
            time_per_task = elapsed / completed
            remaining = total_tasks - completed
            eta = time_per_task * remaining
            timer_label.config(text=f"Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s")
        else:
            timer_label.config(text="Running...")
        root.update_idletasks()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_directory_listing, domain, path): path for path in unique_paths}
        for future in as_completed(futures):
            if cancel_scan:
                break
            result = future.result()
            if result:
                results.append({"Domain": domain, "URL": result})
            completed += 1
            update_progress()

    os.unlink(temp_file_path)
    return results


def export_results():
    if not results_data:
        messagebox.showwarning("Warning", "No results to export.")
        return
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return
    df = pd.DataFrame(results_data)
    excel_path = os.path.join(output_dir, "directory_listings.xlsx")
    html_path = os.path.join(output_dir, "directory_listings.html")
    df.to_excel(excel_path, index=False)
    df.to_html(html_path, index=False)
    messagebox.showinfo("Exported", f"Results exported to:\n{excel_path}\n{html_path}")


def cancel_running_scan():
    global cancel_scan
    cancel_scan = True
    cancel_button.config(state=tk.DISABLED)
    timer_label.config(text="Scan cancelled.")


def run_scan_thread():
    global results_data, cancel_scan
    cancel_scan = False
    domain = domain_entry.get().strip()
    threads = int(threads_spinbox.get())
    if not re.match(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", domain):
        messagebox.showerror("Error", "Invalid domain format.")
        return

    scan_button.config(state=tk.DISABLED)
    cancel_button.config(state=tk.NORMAL)
    export_button.config(state=tk.DISABLED)
    results_text.delete(*results_text.get_children())
    progress_bar["value"] = 0
    timer_label.config(text="Starting...")

    results_data = process_domain(domain, threads)
    if results_data and not cancel_scan:
        for row in results_data:
            results_text.insert("", tk.END, values=(row['Domain'], row['URL']))
        messagebox.showinfo("Scan Complete", f"Found {len(results_data)} directory listings.")
    elif not cancel_scan:
        messagebox.showinfo("Scan Complete", "No directory listings found.")

    scan_button.config(state=tk.NORMAL)
    cancel_button.config(state=tk.DISABLED)
    export_button.config(state=tk.NORMAL)


def run_scan():
    threading.Thread(target=run_scan_thread).start()


# GUI setup
root = tk.Tk()
root.title("WaybackLister - GUI Edition")
root.geometry("700x650")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=False)

# Domain input
ttk.Label(frame, text="Target Domain:").grid(row=0, column=0, sticky=tk.W)
domain_entry = ttk.Entry(frame, width=40)
domain_entry.grid(row=0, column=1, padx=5, pady=5)

# Thread input
ttk.Label(frame, text="Threads:").grid(row=1, column=0, sticky=tk.W)
threads_spinbox = ttk.Spinbox(frame, from_=1, to=50, width=5)
threads_spinbox.set(10)
threads_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

# Buttons
buttons_frame = ttk.Frame(root, padding=10)
buttons_frame.pack()
scan_button = ttk.Button(buttons_frame, text="Start Scan", command=run_scan)
scan_button.grid(row=0, column=0, padx=10)
export_button = ttk.Button(buttons_frame, text="Export Results", command=export_results)
export_button.grid(row=0, column=1, padx=10)
cancel_button = ttk.Button(buttons_frame, text="Cancel Scan", command=cancel_running_scan)
cancel_button.grid(row=0, column=2, padx=10)
cancel_button.config(state=tk.DISABLED)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

# Timer label
timer_label = ttk.Label(root, text="", font=("Arial", 9))
timer_label.pack()

# Results display
columns = ("Domain", "URL")
results_text = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    results_text.heading(col, text=col)
    results_text.column(col, anchor="w", width=300)
results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Signature
signature = ttk.Label(root, text="Made by SUDONINJA", anchor="e", font=("Arial", 8))
signature.pack(side=tk.BOTTOM, anchor="e", padx=10, pady=5)

root.mainloop()
