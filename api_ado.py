import requests

organization = "mi-organizacion"
personal_access_token = "mi-token-de-acceso-personal"
headers = {"Authorization": f"Basic {personal_access_token}"}
base_url = f"https://dev.azure.com/{organization}"

def get_projects():
    url = f"{base_url}/_apis/projects?api-version=7.1-preview.4"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

def get_repositories(project):
    url = f"{base_url}/{project}/_apis/git/repositories?api-version=7.1-preview.1"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

def get_branch_policies(project, repository_id):
    url = f"{base_url}/{project}/_apis/policy/configurations?repositoryId={repository_id}&refName=refs/heads/main&api-version=7.1-preview.1"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

# Iterar sobre todos los proyectos y repositorios
for project in get_projects():
    project_name = project["name"]
    print(f"Project: {project_name}")
    
    for repo in get_repositories(project_name):
        repo_name = repo["name"]
        print(f"  Repository: {repo_name}")
        
        branch_policies = get_branch_policies(project_name, repo["id"])
        if branch_policies:
            print(f"    Policies on 'main': {branch_policies}")
        else:
            print("    No policies found on 'main'")
