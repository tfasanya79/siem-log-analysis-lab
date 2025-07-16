# SIEM Log Analysis Lab

[![CI](https://github.com/tfasanya79/siem-log-analysis-lab/actions/workflows/main.yml/badge.svg)](https://github.com/tfasanya79/siem-log-analysis-lab/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/tfasanya79/siem-log-analysis-lab/branch/main/graph/badge.svg)](https://codecov.io/gh/tfasanya79/siem-log-analysis-lab)
![Python Version](https://img.shields.io/badge/python-3.12.3-blue.svg)
![License](https://img.shields.io/github/license/tfasanya79/siem-log-analysis-lab)
![Last Commit](https://img.shields.io/github/last-commit/tfasanya79/siem-log-analysis-lab)

This project is a lab for setting up a Security Information and Event Management (SIEM) system. The goal is to learn how to ingest logs from various sources, analyze them, and respond to security incidents.

...
# 🛡️ SIEM Log Analysis Lab (Wazuh + Automation + Threat Detection)

Welcome to your Blue Team Security Lab! This project is designed to help you learn, build, and showcase real-world skills in:

- SIEM deployment and log collection
- Threat detection and response
- Python-based automation
- Security event correlation
- Incident response documentation

---

## 📦 Project Structure

```

├── setup/                 # Wazuh & Agent Installation
├── detections/           # Log-based threat detection guides
├── automation/           # Python scripts for enrichment & parsing
├── playbooks/            # Incident response templates
├── docs/                 # Architecture, kanban board, diagrams

````

---

## 🎯 Project Goals

| Goal | Description |
|------|-------------|
| ✅ SIEM Setup | Deploy Wazuh with Elastic Stack and connect endpoints |
| ✅ Log Collection | Ingest logs from Linux and Windows VMs |
| ✅ Threat Detection | Write rules to detect brute force, privilege escalation |
| ✅ Automation | Use Python to parse logs and enrich alerts with VirusTotal |
| ✅ Kanban Workflow | Track tasks and sprints using GitHub Projects |
| ✅ Playbooks | Document response for incidents like malware or data exfiltration |

---

## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/tfasanya79/siem-log-analysis-lab.git
cd siem-log-analysis-lab
````

### 2. Follow Lab Setup

* 📁 [`setup/wazuh-server.md`](setup/wazuh-server.md): Deploy Wazuh server and ELK
* 📁 [`setup/endpoint-setup.md`](setup/endpoint-setup.md): Add agents (Windows + Linux)

---

## 🔍 Detection Labs

| Detection Use Case   | Guide                                                                      |
| -------------------- | -------------------------------------------------------------------------- |
| SSH Brute Force      | [`detections/ssh-brute-force.md`](detections/ssh-brute-force.md)           |
| Privilege Escalation | [`detections/privilege-escalation.md`](detections/privilege-escalation.md) |

---

## ⚙️ Automation Scripts

| Script                        | Purpose                                 |
| ----------------------------- | --------------------------------------- |
| `automation/parse_logs.py`    | Parse Wazuh alerts and extract IOCs     |
| `automation/vt_enrichment.py` | Enrich IPs/domains using VirusTotal API |

---

## 📘 Playbooks

| Scenario                  | Template                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------ |
| Generic IR Template       | [`playbooks/incident-response-template.md`](playbooks/incident-response-template.md) |
| Windows Malware Detection | [`playbooks/malware-detection-windows.md`](playbooks/malware-detection-windows.md)   |

---

## 🧠 Docs & Diagrams

* 🗂 [`docs/kanban-board-setup.md`](docs/kanban-board-setup.md): GitHub Project Kanban guide
* 🖼 [`docs/architecture-diagram.png`](docs/architecture-diagram.png): High-level lab topology

---

## ✅ GitHub Workflow

* Track progress in [Projects](../../projects)
* Use labels like `setup`, `automation`, `playbook`, `detection`
* Each folder has its own scoped task backlog and detection goals

---

## 🤖 Coming Soon

* 💡 Sysmon + Winlogbeat integration
* 📡 MITRE ATT\&CK mapping
* 📊 Kibana dashboard customization
* 🧪 Custom Wazuh rules + decoders
* 🎯 Blue Team CTF/Detection Challenges

---

## 💬 Feedback / Contributions

Feel free to fork, improve, or ask questions via issues. This lab is meant to evolve.

---

````

---

