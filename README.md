## Installation

(coming soon to a pip near you ..)
```
pip install py-resource
```

## Usage

<a href="https://codeclimate.com/github/toast38coza/python-resource"><img src="https://codeclimate.com/github/toast38coza/python-resource/badges/gpa.svg" /></a>
[![Build Status](https://travis-ci.org/toast38coza/python-resource.svg?branch=master)](https://travis-ci.org/toast38coza/python-resource)


## Example Usage

**Define the API you want to consume:**

**api.py**

```python

class GithubAPI(API):
	base_url = "https://api.github.com"
	headers = {"Authorization": "token {}" . format (os.environ.get('token'))}

class RepositoryRepo(Resource):
	api_class = GithubAPI
	resource_path = "/repos/{owner}/{repo}"
	
	# you only need to define resource_path, but 
	# if you need to, you can specify other paths too
	create_resource_path = "/user/repos"
	list_resource_path = "/users/{owner}/repos"
	
..
```

**Now you can consume it:**

**List**
```python
keys = {"owner": user}
repos = RepositoryRepo().list(keys=keys)
```

**Get a repo:**
```python
keys = {"owner": owner, "repo": name}
repo = RepositoryRepo().get(keys=keys)
```

**Create a resource**
```python
data = {"name": repo_name}
repo = RepositoryRepo().create(data)
```

**Partial update: (PATCH)**

```python
keys = {"owner": owner, "repo": repo}
data = {
	"name": repo,
	"private": private
	}
result = RepositoryRepo().partial_update(keys=keys, data=data)
```

**Update: (PUT)**

```python
keys = {"owner": owner, "repo": repo}
data = {
	"name": repo,
	"private": private
}
result = RepositoryRepo().update(keys=keys, data=data)
```

**Delete**

```python
keys = {"owner": owner, "repo": repo}
result = RepositoryRepo().delete(keys=keys)
```

### Coming soon: 

* add `update_or_create(keys, data, search_fields)`



**Extra goodies (todo):**

* Generate slate docs 
  * Generate entire docs
  * Generate snippets
* Generate API mocks
* Build Resources from API
* Install available clients

**Features:**

It can:

**Basics:**

- [x] GET a resource
- [x] update a resource
- [x] create a resource
- [x] delete a resource
- [ ] update_or_create a resource if it doesnt exist
- [x] can query a list endpoint
- [x] provides access to the raw response
- [x] maps JSON map to a Python object for ease of access
- [ ] supports nested json objects

**Authentication and security**

- [x] authenticate with token auth
- [x] authenticate with basic auth


**Meta and ease of use**

- [ ] Can provide useful information if missing fields are not included
- [ ] Can print what a request would look like as 
  * curl: `resource.get(out='curl')`
  * python: `resource.get(out='python')`
  * javascript: `resource.get(out='js')`  
  * ..
- [ ] Generate Slate-style docs (`python -m resources.cli generate docs`)
- [ ] Generate Slate-style mocks (`python -m resources.cli generate mocks`)


**Low level**

- [x] Accept custom headers
- [x] Accept custom params
- [x] Accept custom credentials
- [x] Optionally pass any kwargs to requests constructor