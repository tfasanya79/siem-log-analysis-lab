import requests
import time

# CONFIGURATION
GITHUB_TOKEN = "ghp_your_token_here"
REPO_OWNER = "your-username"
REPO_NAME = "siem-log-analysis-lab"
PROJECT_NUMBER = 1  # This is the project *number* (not ID)

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

issues = [
    {
        "title": "Install Wazuh agent on Ubuntu endpoint",
        "body": "Install and configure Wazuh agent on Ubuntu Desktop VM and register it with the Wazuh server.",
        "labels": ["setup", "log-analysis"]
    },
    {
        "title": "Install Wazuh agent on Windows 10 VM",
        "body": "Install Wazuh agent or configure Winlogbeat on Windows 10 and verify logs are being sent to Wazuh manager.",
        "labels": ["setup", "log-analysis"]
    },
    {
        "title": "Validate log delivery from both endpoints",
        "body": "Ensure that logs from Windows and Ubuntu VMs are visible in Wazuh dashboard (auth.log, event logs, etc).",
        "labels": ["log-analysis"]
    },
    {
        "title": "Simulate brute force attack from Kali to Ubuntu",
        "body": "Use Hydra or similar tools from Kali Linux to simulate SSH brute-force attack. Confirm detection by Wazuh.",
        "labels": ["threat-sim", "log-analysis"]
    },
    {
        "title": "Detect sudo privilege escalation attempts",
        "body": "Test and validate if Wazuh can detect unauthorized sudo usage on Ubuntu.",
        "labels": ["log-analysis", "threat-sim"]
    },
    {
        "title": "Run EICAR malware test on Windows",
        "body": "Download and execute the EICAR test string on Windows to trigger malware detection logs.",
        "labels": ["log-analysis", "threat-sim"]
    },
    {
        "title": "Automate IOC extraction from logs",
        "body": "Create a Python script to extract IP addresses, domains, and hashes from log files.",
        "labels": ["automation"]
    },
    {
        "title": "Integrate VirusTotal for IOC enrichment",
        "body": "Use VirusTotal API to enrich IOCs extracted from logs and add context to alerts.",
        "labels": ["automation", "log-analysis"]
    },
    {
        "title": "Send alert notifications to Slack/Discord",
        "body": "Set up webhook integration to send high severity alerts to Slack or Discord.",
        "labels": ["automation"]
    },
    {
        "title": "Create MITRE ATT&CK mapping documentation",
        "body": "Document detections and map them to ATT&CK techniques.",
        "labels": ["playbook", "research"]
    },
]

# Step 1: Create issues
def create_issue(issue):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    payload = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue["labels"]
    }
    res = requests.post(url, json=payload, headers=headers)
    res.raise_for_status()
    print(f"[+] Created issue: {issue['title']}")
    return res.json()["number"]

# Step 2: Get project ID & field mappings
def get_project_id():
    query = """
    query {
      user(login: "%s") {
        projectV2(number: %d) {
          id
        }
      }
    }
    """ % (REPO_OWNER, PROJECT_NUMBER)
    res = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers=headers
    )
    res.raise_for_status()
    return res.json()["data"]["user"]["projectV2"]["id"]

# Step 3: Add issue to Project (Backlog)
def add_issue_to_project(issue_id, project_id):
    mutation = """
    mutation {
      addProjectV2ItemById(input: {projectId: "%s", contentId: "%s"}) {
        item {
          id
        }
      }
    }
    """ % (project_id, issue_id)
    res = requests.post(
        "https://api.github.com/graphql",
        json={"query": mutation},
        headers=headers
    )
    res.raise_for_status()
    print(f"    ↳ Added to Project")

# MAIN EXECUTION
if __name__ == "__main__":
    print("[*] Fetching Project ID...")
    project_id = get_project_id()

    for issue in issues:
        issue_number = create_issue(issue)
        time.sleep(1)
        issue_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
        res = requests.get(issue_url, headers=headers)
        issue_node_id = res.json()["node_id"]
        add_issue_to_project(issue_node_id, project_id)
        time.sleep(1)
