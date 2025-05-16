import os
from dotenv import load_dotenv
import requests

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "siem-log-analysis-lab"
OWNER = "tfasanya79"

GRAPHQL_API_URL = 'https://api.github.com/graphql'

HEADERS = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def run_graphql_query(query, variables):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(GRAPHQL_API_URL, json=payload, headers=headers)
    print(f"GraphQL Response: {response.json()}")
    return response.json()

GET_PROJECT_QUERY = '''
query {
  viewer {
    projectsV2(first: 20) {
      nodes {
        id
        title
      }
    }
  }
}
'''

CREATE_PROJECT_QUERY = '''
mutation CreateProject($input: CreateProjectV2Input!) {
  createProjectV2(input: $input) {
    projectV2 {
      id
      title
    }
  }
}
'''

GET_PROJECT_FIELDS_QUERY = '''
query GetProjectFields($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
          ... on ProjectV2FieldCommon {
            id
            name
            dataType
          }
        }
      }
    }
  }
}
'''

ADD_ISSUE_TO_PROJECT_QUERY = """
mutation AddIssueToProject($projectId: ID!, $issueId: ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $issueId}) {
    item {
      id
    }
  }
}
"""

GET_ISSUE_NODE_ID_QUERY = '''
query getIssueNodeId($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      id
    }
  }
}
'''

def create_project_if_not_exists(title):
    existing = run_graphql_query(GET_PROJECT_QUERY, {})
    for node in existing["data"]["viewer"]["projectsV2"]["nodes"]:
        if node["title"] == title:
            print(f"✅ Project '{title}' already exists.")
            return node["id"]

    variables = {"input": {"ownerId": get_user_id(OWNER), "title": title}}
    created = run_graphql_query(CREATE_PROJECT_QUERY, variables)
    project = created["data"]["createProjectV2"]["projectV2"]
    print(f"✅ Project '{title}' created.")
    return project["id"]

def get_user_id(username):
    query = '''
    query getUserId($username: String!) {
      user(login: $username) {
        id
      }
    }
    '''
    result = run_graphql_query(query, {"username": username})
    return result["data"]["user"]["id"]

def get_issue_node_id(issue_number):
    variables = {
        "owner": OWNER,
        "repo": REPO_NAME,
        "issueNumber": issue_number
    }
    result = run_graphql_query(GET_ISSUE_NODE_ID_QUERY, variables)
    return result["data"]["repository"]["issue"]["id"]

def create_issue(title, body, labels=[], assignees=[], draft=True):
    url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/issues"
    data = {
        "title": title,
        "body": body,
        "labels": labels,
        "assignees": assignees
    }
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        issue = response.json()
        print(f"📝 Issue '{title}' created.")
        return issue["number"]
    else:
        print(f"❌ Failed to create issue: {response.status_code} {response.text}")
        return None

def set_project_status(project_id, item_id, status_option_name="Todo"):
    result = run_graphql_query(GET_PROJECT_FIELDS_QUERY, {"projectId": project_id})
    fields = result["data"]["node"]["fields"]["nodes"]

    status_field_id = None
    status_option_id = None

    for field in fields:
        if field.get("name", "").lower() == "status" and "options" in field:
            status_field_id = field["id"]
            for option in field["options"]:
                if option["name"].lower() == status_option_name.lower():
                    status_option_id = option["id"]
                    break
            break

    if not status_field_id or not status_option_id:
        print(f"⚠️ Could not find field or option for status '{status_option_name}'")
        return

    mutation = '''
    mutation UpdateItemField($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId,
        itemId: $itemId,
        fieldId: $fieldId,
        value: {
          singleSelectOptionId: $optionId
        }
      }) {
        projectV2Item {
          id
        }
      }
    }
    '''

    variables = {
        "projectId": project_id,
        "itemId": item_id,
        "fieldId": status_field_id,
        "optionId": status_option_id
    }

    result = run_graphql_query(mutation, variables)
    if "errors" in result:
        print(f"❌ Failed to update status: {result['errors']}")
    else:
        print(f"✅ Status set to '{status_option_name}'")

def add_issue_to_project(project_id, issue_number, status_value="Todo"):
    issue_node_id = get_issue_node_id(issue_number)
    if not issue_node_id:
        print(f"❌ Could not get node ID for issue {issue_number}")
        return

    result = run_graphql_query(ADD_ISSUE_TO_PROJECT_QUERY, {
        "projectId": project_id,
        "issueId": issue_node_id
    })

    item_id = result["data"]["addProjectV2ItemById"]["item"]["id"]
    print(f"✔️ Issue {issue_number} added to project.")

    set_project_status(project_id, item_id, status_option_name=status_value)

def main():
    project_title = "SIEM Lab Progress"
    project_id = create_project_if_not_exists(project_title)

    issues = [
        {"title": "Set up SIEM architecture", "body": "Deploy infrastructure", "labels": ["infra"], "assignees": ["tfasanya79"]},
        {"title": "Ingest Windows logs", "body": "Configure log ingestion", "labels": ["logs"], "assignees": ["tfasanya79"]},
        {"title": "Write detection rules", "body": "Implement detection rules", "labels": ["detections"], "assignees": ["tfasanya79"]},
        {"title": "Test alerting workflows", "body": "Simulate attacks to test alerts", "labels": ["testing"], "assignees": ["tfasanya79"]}
    ]

    for issue in issues:
        number = create_issue(issue["title"], issue["body"], labels=issue["labels"], assignees=issue["assignees"])
        if number:
            add_issue_to_project(project_id, number, status_value="Todo")

if __name__ == "__main__":
    main()
