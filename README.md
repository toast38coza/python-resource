## Usage

<a href="https://codeclimate.com/github/toast38coza/python-resource"><img src="https://codeclimate.com/github/toast38coza/python-resource/badges/gpa.svg" /></a>


**api.py**

```
from resource import API, Resource

class GithubAPI(API):
  base_url='..'
  token_headers='..'
  headers={}


@allowed_methods=['get','put','post','delete']
class RepositoryResource(Resource)
  api_class = 'GitHubAPI'
  path = "/users/{user}/repos/{repo}"
  # optional
  authentication_class = 'resources.authentication.{Token,Basic,None:default('None')}' # or provide your own
  # for validation
  required_fields = []
  # for accessing like an object
  fields = []

data = {
  "token": "..",
}
repo_resource - RepositoryResource(**data)
repos = repo_resource.query()
repo = repo_resource.get(user='toast38coza', repo='PyResource')
repo.homepage = "http://pyresource.github.io"
repo.save()

# create a new repo: 

data = {
  ..
}
repo = Repo.save(**data)

## or: 

repo = Repo()
repo.name = '..'
..
repo.save()

# will perform a query with `search_params`, if no results return, will create. Else: update
repo.create_or_update(search_params={}, data={})
```

**Extra goodies:**

* Generate slate docs 
  * Generate entire docs
  * Generate snippets
* Generate API mocks
* Build Resources from API
* Install available clients

**Spec**

It can:

**Basics:**

* GET a resource
* update a resource
* create a resource
* delete a resource
* update_or_create a resource if it doesnt exist
* can query a list endpoint
* provides access to the raw response
* maps JSON map to a Python object for ease of access
* supports nested json objects

**Authentication and security**

* authenticate with token auth
* authenticate with basic auth
* limit verbs that are available 

**Meta and ease of use**

* Can provide useful information if missing fields are not included
* Can print what a request would look like as 
  * curl: `resource.get(out='curl')`
  * python: `resource.get(out='python')`
  * javascript: `resource.get(out='js')`  
  * ..
* Generate Slate-style docs (`python -m resources.cli generate docs`)
* Generate Slate-style mocks (`python -m resources.cli generate mocks`)


**Low level**

* Accept custom headers
* Accept custom params
* Accept custom credentials
* Optionally pass any kwargs prefixed with `requests__` to requests constructor


**Restrictions**

* Only works on RESTful APIs which communicate over JSON
