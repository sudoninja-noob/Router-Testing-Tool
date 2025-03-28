# Security Testing Tools Mapping


## Chapter 1: Common Security Requirements

### Section 1.1: Access and Authorization

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.1.1** | Wireshark, tcpdump, custom mutual authentication testers (TLS, SSH, SNMPv3) |
| **1.1.2** | Burp Suite, Ettercap, OpenSSL, tshark for management traffic inspection |
| **1.1.3** | Cisco ISE, FreeIPA, Keycloak for RBAC testing |
| **1.1.4** | RADIUS/TACACS+ testing tools, Nmap scripts for login brute-force |
| **1.1.5** | SSH hardening checks, Fail2ban, manual testing of restricted logins |
| **1.1.6** | Policy review scripts, access control simulation tools |
| **1.1.7** | User account audit tools, custom Python/Ansible scripts to check accounts and groups |

---

### Section 1.2: Authentication Attribute Management

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.2.1** | Authconfig, Password Policy Enforcement Tools |
| **1.2.2** | LDAP, RADIUS, Kerberos testing tools |
| **1.2.3** | Hydra, Medusa, Fail2Ban, SSHGuard |
| **1.2.4** | CrackLib, PAM modules, John the Ripper for strength validation |
| **1.2.5** | Session timeout testing via browser automation (Selenium) |
| **1.2.6** | Password change automation scripts, audit logs |
| **1.2.7** | Custom test scripts, error message capture via Burp Suite |
| **1.2.8** | Account audit scripts, CIS-CAT Pro, Lynis |

---

### Section 1.3: Software Security

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.3.1–1.3.2** | GPG, APT/YUM security checks, SBOM (Software Bill of Materials) |
| **1.3.3** | SAST tools: SonarQube, Checkmarx |
| **1.3.4** | ClamAV, YARA, VirusTotal API |
| **1.3.5–1.3.6** | Bloaty, Lynis, Ansible playbooks to remove unused services |
| **1.3.7** | BIOS/UEFI config, AuditD, bootloader lockdown checks |
| **1.3.8** | Chrony/NTP audit scripts, tlsdate |
| **1.3.9** | Self-test simulation via custom startup scripts, Tripwire |
| **1.3.10** | Nmap, Netstat, iptables audit |
| **1.3.11** | Wireless scanning tools: Kismet, Aircrack-ng |

---

### Section 1.4: System Secure Execution Environment

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.4.1–1.4.2** | LSOF, ps, rpm -q, dpkg --list, Lynis, Audit scripts |

---

### Section 1.5: User Audit

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.5.1** | AuditD, Syslog, SIEM tools |
| **1.5.2** | Syslog monitoring, custom script triggers, Wazuh |
| **1.5.3** | Syslog-ng, Rsyslog, Secure SCP export, GPG encryption |

---

### Section 1.6: Data Protection

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.6.1** | OpenSSL, Wireshark, test TLS/IPsec tunnels |
| **1.6.2–1.6.3** | FIPS validation tools, Crypto libraries audit (OpenSSL, Libgcrypt) |
| **1.6.4–1.6.6** | Data Loss Prevention (DLP) tools, Tripwire, AIDE, SELinux |
| **1.6.7** | Exfiltration detection tools: Zeek, Snort, Suricata |

---

### Section 1.7: Network Services

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.7.1** | iptables, pfSense, Cisco ACL simulation |
| **1.7.2** | VLAN analysis using Wireshark, tcpdump, virtual lab simulation |
| **1.7.3** | hping3, Scapy, custom anti-spoofing test scripts |

---

### Section 1.8: Attack Prevention Mechanisms

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.8.1** | LOIC/HOIC (simulated in lab), Slowloris, mitigation via WAF/FW |
| **1.8.2** | Stress-ng, iperf3, custom resource saturation tests |
| **1.8.3** | Scapy, IP options injection, verify drops/logs |

---

### Section 1.9: Vulnerability Testing Requirements

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.9.1** | Peach Fuzzer, Boofuzz, Sulley |
| **1.9.2** | Nmap, Masscan, Netcat |
| **1.9.3** | OpenVAS, Nessus, Qualys, Nikto (web) |

---

### Section 1.10: Operating System

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.10.1** | Filesystem monitoring, Sysdig, Inotify |
| **1.10.2** | Scapy, ping/ICMP testers, firewall rules verification |
| **1.10.3** | Sudoers audit, PrivEsc tools: LinPEAS, GTFOBins |
| **1.10.4** | User audit, whoami, getent passwd |
| **1.10.5** | GRSecurity, AppArmor, SELinux, Sysctl checks |
| **1.10.6** | USBGuard, udevadm rules, BIOS config |
| **1.10.7** | mount, fstab audits, AppArmor, SELinux policies |

---

### Section 1.11: Web Servers

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.11.1** | SSL Labs, testssl.sh, Burp Suite |
| **1.11.2** | Logrotate, Syslog, Apache/nginx log review |
| **1.11.3** | Burp Suite, cookie attribute analysis, JWT analyzers |
| **1.11.4** | OWASP ZAP, Burp, custom fuzzers |
| **1.11.5–1.11.18** | Nikto, Dirb, custom CGI/SSI/HTTP method checkers, mod_security, WAF |

---

### Section 1.12: Other Security Requirements

| Subsection | Tools / Techniques |
|------------|---------------------|
| **1.12.1** | Remote debug audit, CLI/API analysis |
| **1.12.2** | Policy verification (manual), login scripts audit |
| **1.12.3–1.12.5** | Trusted Boot/UEFI Secure Boot, Integrity checks, Tripwire |
| **1.12.6** | lshw, lspci, ifconfig/ip link, udev rules |
| **1.12.7** | Baseline hardening scripts, CIS benchmarks |
| **1.12.8** | Crypto module control tools, config file review |
| **1.12.9** | QoS/firewall policy validation, routing table inspection |



