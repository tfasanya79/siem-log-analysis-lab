import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get variables from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "siem-log-analysis-lab"
OWNER = "tfasanya79"

GRAPHQL_API_URL = 'https://api.github.com/graphql'

# GraphQL Query to get the GitHub user ID based on the username
GET_USER_ID_QUERY = '''
query getUserId($username: String!) {
  user(login: $username) {
    id
  }
}
'''

# GraphQL Query to create a project in the new Projects V2 API
CREATE_PROJECT_QUERY = '''
mutation createProject($input: CreateProjectV2Input!) {
  createProjectV2(input: $input) {
    projectV2 {
      id
      title
    }
  }
}
'''

# GraphQL Query to add an issue to the project
ADD_ISSUE_TO_PROJECT_QUERY = '''
mutation addIssueToProject($projectId: ID!, $issueId: ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $issueId}) {
    project {
      id
    }
  }
}
'''

# GraphQL Query to get issue node ID from issue number
GET_ISSUE_NODE_ID_QUERY = '''
query getIssueNodeId($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      id
    }
  }
}
'''

HEADERS = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def run_graphql_query(query, variables=None):
    """Run a GraphQL query against GitHub's GraphQL API."""
    response = requests.post(GRAPHQL_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ GraphQL request failed: {response.status_code}, {response.text}")
        return None

def get_user_id(username):
    """Get the user ID from GitHub based on the username."""
    variables = {
        "username": username
    }
    result = run_graphql_query(GET_USER_ID_QUERY, variables)
    if result and result.get("data") and result["data"].get("user"):
        return result["data"]["user"]["id"]
    else:
        print(f"❌ Could not fetch user ID for {username}. Exiting...")
        return None

def create_project(project_title):
    """Create a new project using GraphQL."""
    user_id = get_user_id(OWNER)
    if not user_id:
        return None
    
    variables = {
        "input": {
            "ownerId": user_id,
            "title": project_title
        }
    }
    
    result = run_graphql_query(CREATE_PROJECT_QUERY, variables)
    
    if result is None:
        print("❌ No result returned from GraphQL query. Check the GraphQL response for errors.")
        return None
    if result.get("errors"):
        print("❌ GraphQL errors:", result.get("errors"))
        return None

    if result.get("data"):
        project = result["data"]["createProjectV2"]["projectV2"]
        print(f"✅ Project '{project_title}' created successfully with ID {project['id']}.")
        return project['id']
    else:
        print(f"❌ Failed to create project: {result}")
        return None

def get_issue_node_id(owner, repo_name, issue_number):
    """Get the global node ID of an issue."""
    variables = {
        "owner": owner,
        "repo": repo_name,
        "issueNumber": issue_number
    }
    result = run_graphql_query(GET_ISSUE_NODE_ID_QUERY, variables)
    if result and result.get("data"):
        issue_node_id = result["data"]["repository"]["issue"]["id"]
        return issue_node_id
    else:
        print(f"❌ Failed to fetch issue node ID for issue number {issue_number}.")
        return None

def create_issue(repo_name, issue_title, issue_body=""):
    """Create an issue in the repository."""
    url = f"https://api.github.com/repos/{OWNER}/{repo_name}/issues"
    data = {
        "title": issue_title,
        "body": issue_body
    }
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        issue = response.json()
        print(f"📝 Issue '{issue_title}' created.")
        return issue['number']
    else:
        print(f"❌ Failed to create issue: {response.status_code}")
        return None

def add_issue_to_project(project_id, issue_number):
    """Add an issue to the project board."""
    issue_node_id = get_issue_node_id(OWNER, REPO_NAME, issue_number)
    if not issue_node_id:
        return
    variables = {
        "projectId": project_id,
        "issueId": issue_node_id
    }
    result = run_graphql_query(ADD_ISSUE_TO_PROJECT_QUERY, variables)
    if result and result.get("data"):
        print(f"✔️ Issue {issue_number} added to project.")
    else:
        print(f"❌ Failed to add issue {issue_number} to project.")

def main():
    # Create the project
    project_title = "SIEM Lab Progress"
    project_id = create_project(project_title)
    
    if project_id:
        # Create issues and add them to the project
        issues = [
            {"title": "Set up SIEM architecture", "body": "Configure and deploy SIEM architecture."},
            {"title": "Ingest Windows logs", "body": "Configure log ingestion from Windows devices."},
            {"title": "Write detection rules", "body": "Create detection rules for SIEM."},
            {"title": "Test alerting workflows", "body": "Test the alerting workflows in the SIEM."}
        ]
        
        for issue in issues:
            issue_number = create_issue(REPO_NAME, issue['title'], issue['body'])
            if issue_number:
                add_issue_to_project(project_id, issue_number)
    else:
        print("❌ Could not create project. Exiting...")

if __name__ == '__main__':
    main()
