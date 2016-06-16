from resource import Resource, API
import sys, os

"""
Usage: 
export token=".."
export user=".."
python github.py
"""

class GithubAPI(API):
	base_url = "https://api.github.com"
	headers = {"Authorization": "token {}" . format (os.environ.get('token'))}

class RepositoryRepo(Resource):
	api_class = GithubAPI
	resource_path = "/repos/{owner}/{repo}"
	create_resource_path = "/user/repos"
	list_resource_path = "/users/{owner}/repos"
	

## Read

## list all repos for user: 
def list_repos(user):
	print ("Getting all repos for {}" . format (user))
	
	resource = RepositoryRepo()
	keys = {"owner": user}
	repos = resource.list(keys=keys)

	if repos.status_code == 200:
		for repo in repos.objects: 
			print (repo.name)
	else: 
		print (repos.response.content)

## Create:
def create_repo(repo_name):
	print ("Creating repo {}" . format (user))
	data = {"name": repo_name}
	repo = RepositoryRepo().create(data)

	if repo.status_code == 201:
		print (repo.resource.name)

	else:
		print (repo.response.content)

def get_repo(owner, name):
	print ("Getting repo {}{}" . format (owner, name))

	keys = {"owner": owner, "repo": name}
	repo = RepositoryRepo().get(keys=keys)

	if repo.status_code == 200:
		print ("Repo: {}. Private: {}" . format (repo.resource.name, repo.resource.private))

	else:
		print (repo.response.content)

## Update
def update_repo(owner, repo, private=True):
	print ("Updating private on {} to be {}" . format (repo, private))
	keys = {"owner": owner, "repo": repo}
	data = {
		"name": repo,
		"private": private
		}
	result = RepositoryRepo().partial_update(keys=keys, data=data)

	if result.status_code == 200:
		print ("Privacy: {}" . format (result.resource.private))
	else:
		print (result.response.content)


## Delete
def delete_repo(owner, repo):
	print ("Deleting {}" . format (repo))
	keys = {"owner": owner, "repo": repo}
	result = RepositoryRepo().delete(keys=keys)
	print (result.status_code)

def print_break():
	print ("************************************")

user = os.environ.get("user")
repo = "test-repo"

list_repos(user)
print_break()
create_repo(repo)
print_break()
get_repo(user, repo)
print_break()
update_repo(user, repo)
print_break()
delete_repo(user, repo)


