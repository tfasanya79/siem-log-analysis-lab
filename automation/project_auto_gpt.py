def add_issue_to_project(project_id, issue_number):
    """Add an issue to the project board."""
    issue_node_id = get_issue_node_id(OWNER, REPO_NAME, issue_number)
    if not issue_node_id:
        return
    variables = {
        "projectId": project_id,
        "issueId": issue_node_id
    }
    
    print(f"Attempting to add issue {issue_number} (Node ID: {issue_node_id}) to project {project_id}...")
    
    result = run_graphql_query(ADD_ISSUE_TO_PROJECT_QUERY, variables)
    
    if result and result.get("data"):
        print(f"✔️ Issue {issue_number} added to project.")
    else:
        print(f"❌ Failed to add issue {issue_number} to project.")
        print(f"Response from GraphQL query: {result}")  # Enhanced error logging for debugging

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
        print(f"GraphQL result: {result}")  # Print out GraphQL result for debugging
        return None
