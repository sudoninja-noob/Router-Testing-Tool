import tkinter as tk
from tkinter import filedialog, messagebox
import ssl, socket, paramiko
from pysnmp.hlapi import *

def test_https_mutual_auth(host, port, cert, key, ca_cert, output):
    try:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_cert)
        context.load_cert_chain(certfile=cert, keyfile=key)
        with socket.create_connection((host, int(port))) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                output.insert(tk.END, f"[+] HTTPS Mutual TLS successful. Cipher: {ssock.cipher()}\n")
                output.insert(tk.END, f"    Server cert: {ssock.getpeercert()}\n")
    except Exception as e:
        output.insert(tk.END, f"[-] HTTPS Mutual TLS failed: {e}\n")

def test_ssh_key_auth(host, port, username, key_file, output):
    try:
        key = paramiko.RSAKey.from_private_key_file(key_file)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=int(port), username=username, pkey=key)
        output.insert(tk.END, "[+] SSH Key-based Mutual Authentication successful.\n")
        client.close()
    except Exception as e:
        output.insert(tk.END, f"[-] SSH Key-based auth failed: {e}\n")

def test_snmpv3_auth(host, port, user, auth_key, priv_key, output):
    auth_proto = usmHMACSHAAuthProtocol
    priv_proto = usmAesCfb128Protocol if priv_key else None

    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(user, auth_key, priv_key, authProtocol=auth_proto, privProtocol=priv_proto),
        UdpTransportTarget((host, int(port))),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))  # sysDescr
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:
        output.insert(tk.END, f"[-] SNMPv3 Auth failed: {errorIndication}\n")
    elif errorStatus:
        output.insert(tk.END, f"[-] SNMPv3 Error: {errorStatus.prettyPrint()}\n")
    else:
        output.insert(tk.END, "[+] SNMPv3 Authentication successful.\n")
        for varBind in varBinds:
            output.insert(tk.END, f"    {varBind}\n")

def browse_file(entry):
    path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, path)

def run_test():
    output.delete(1.0, tk.END)
    protocol = protocol_var.get()
    host = host_entry.get()
    port = port_entry.get()

    if protocol == "HTTPS":
        test_https_mutual_auth(host, port, cert_entry.get(), key_entry.get(), ca_entry.get(), output)
    elif protocol == "SSH":
        test_ssh_key_auth(host, port, user_entry.get(), ssh_key_entry.get(), output)
    elif protocol == "SNMPv3":
        test_snmpv3_auth(host, port, snmp_user_entry.get(), snmp_auth_entry.get(), snmp_priv_entry.get(), output)

# --- GUI Layout ---
# (Keep all your imports and function definitions as-is)

# --- GUI Layout with Green Border and Signature ---
root = tk.Tk()
root.title("Mutual Authentication Tester V1.0")
root.configure(bg="green")  # Green border around the app

# White inner frame (main content area)
main_frame = tk.Frame(root, bg="white", padx=10, pady=10, relief="solid", borderwidth=2)
main_frame.pack(padx=10, pady=(10, 0))

# Footer for signature
footer = tk.Frame(root, bg="white")
footer.pack(fill=tk.X, side=tk.BOTTOM, anchor="e", padx=10, pady=(0, 5))
tk.Label(footer, text="Made by sudoninja", bg="white", fg="gray").pack(side=tk.RIGHT)

# All widgets below this point go into main_frame instead of root
protocol_var = tk.StringVar(value="HTTPS")
tk.Label(main_frame, text="Protocol:", bg="white").grid(row=0, column=0, sticky="e")
tk.OptionMenu(main_frame, protocol_var, "HTTPS", "SSH", "SNMPv3").grid(row=0, column=1)

tk.Label(main_frame, text="Host:", bg="white").grid(row=1, column=0, sticky="e")
host_entry = tk.Entry(main_frame)
host_entry.grid(row=1, column=1)

tk.Label(main_frame, text="Port:", bg="white").grid(row=2, column=0, sticky="e")
port_entry = tk.Entry(main_frame)
port_entry.grid(row=2, column=1)

# HTTPS
cert_entry = tk.Entry(main_frame, width=40)
key_entry = tk.Entry(main_frame, width=40)
ca_entry = tk.Entry(main_frame, width=40)

tk.Label(main_frame, text="Client Cert (HTTPS):", bg="white").grid(row=3, column=0, sticky="e")
cert_entry.grid(row=3, column=1)
tk.Button(main_frame, text="Browse", command=lambda: browse_file(cert_entry)).grid(row=3, column=2)

tk.Label(main_frame, text="Client Key (HTTPS):", bg="white").grid(row=4, column=0, sticky="e")
key_entry.grid(row=4, column=1)
tk.Button(main_frame, text="Browse", command=lambda: browse_file(key_entry)).grid(row=4, column=2)

tk.Label(main_frame, text="CA Cert (HTTPS):", bg="white").grid(row=5, column=0, sticky="e")
ca_entry.grid(row=5, column=1)
tk.Button(main_frame, text="Browse", command=lambda: browse_file(ca_entry)).grid(row=5, column=2)

# SSH
tk.Label(main_frame, text="SSH Username:", bg="white").grid(row=6, column=0, sticky="e")
ssh_user_entry = tk.Entry(main_frame)
ssh_user_entry.grid(row=6, column=1)

tk.Label(main_frame, text="SSH Password:", bg="white").grid(row=7, column=0, sticky="e")
ssh_pass_entry = tk.Entry(main_frame, show="*")
ssh_pass_entry.grid(row=7, column=1)

ssh_key_entry = tk.Entry(main_frame, width=40)
tk.Label(main_frame, text="SSH Key File:", bg="white").grid(row=8, column=0, sticky="e")
ssh_key_entry.grid(row=8, column=1)
tk.Button(main_frame, text="Browse", command=lambda: browse_file(ssh_key_entry)).grid(row=8, column=2)

# SNMPv3
tk.Label(main_frame, text="SNMPv3 User:", bg="white").grid(row=9, column=0, sticky="e")
snmp_user_entry = tk.Entry(main_frame)
snmp_user_entry.grid(row=9, column=1)

tk.Label(main_frame, text="SNMPv3 Auth Key:", bg="white").grid(row=10, column=0, sticky="e")
snmp_auth_entry = tk.Entry(main_frame)
snmp_auth_entry.grid(row=10, column=1)

tk.Label(main_frame, text="SNMPv3 Priv Key (optional):", bg="white").grid(row=11, column=0, sticky="e")
snmp_priv_entry = tk.Entry(main_frame)
snmp_priv_entry.grid(row=11, column=1)

# Run button
tk.Button(main_frame, text="Run Test", command=run_test).grid(row=12, column=1, pady=5)

# Output box
output = tk.Text(main_frame, height=12, width=70)
output.grid(row=13, column=0, columnspan=3, pady=10)

root.mainloop()
