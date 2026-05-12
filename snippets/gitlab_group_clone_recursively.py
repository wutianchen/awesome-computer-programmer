import os
import gitlab

# Set the GitLab access token and the URL of the GitLab server
GITLAB_TOKEN = "PERSONAL_ACCESS_TOKEN"
GITLAB_URL = "https://DOMAIN_NAME"

# Create a GitLab API client
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

# Get the GitLab group ID and name
group_id = gl.groups.get("ROOT_GROUP_NAME").id
group_name = gl.groups.get(group_id).name

# Define a function to clone a GitLab project
def clone_project(project):
    project_path = project.path_with_namespace
    project_url = project.ssh_url_to_repo
    # do not clone archived projects
    if not project.archived:
        os.system(f"git clone {project_url} {project_path}")


# Define a function to recursively clone all projects in a group and its subgroups
def clone_group_projects(group):
    # Clone projects in the current group
    projects = group.projects.list(all=True)
    for project in projects:
        clone_project(project)

    # Recursively clone projects in subgroups
    subgroups = group.subgroups.list()
    for subgroup in subgroups:
        subgroup_path = subgroup.path
        subgroup_id = subgroup.id
        subgroup = gl.groups.get(subgroup_id)
        clone_group_projects(subgroup)


# Clone all projects in the group and its subgroups
clone_group_projects(gl.groups.get(group_id))
