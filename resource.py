import requests, re, inspect, json, types

class API(object):
	base_url = None
	headers = {}

class ResourceItem(object):
	pass

class Response(object):
	status_code = 200
	resource = None 
	objects = [] # list of resource (for query)
	response = None # requests HttpResponse

	def __init__(self, response, many=False):
		
		self.status_code = response.status_code
		self.response = response 

		# 2xx is ok
		if response.status_code < 300: 
			if many:
				self.objects = []
				for item in response.json():
					resource = self.dict_to_resource_item(item)
					self.objects.append(resource)
			else:
				try:
					self.resource = self.dict_to_resource_item(response.json())
				except ValueError:
					pass

	def dict_to_resource_item(self, dict_item):
		"""
		Takes a dictionary. e.g.: {'foo': 'bar'}
		and returns a ResourceItem object.
		e.g.: resource_item.foo = 'bar'
		"""
		resource = ResourceItem()
		for key, value in dict_item.items():
			setattr(resource, key, value)
		return resource

	"""
	TODO: allow save() to be called on resource
	it should: 
	  * record any changes to fields 
	    (e.g.: create getters for all fields on resource)
	    record which fields have changes
	    send this to partial_update on save
	    .. or .. 
	    simply update the json when changes are made to
	    fields on resource 
	    send data as PATCH
	
	"""

class Resource(object):

	resouce_path = None
	objects = []


	interface = {
		"get": {"verb": "get"},
		"list": {"verb": "get"},
		"update": {"verb": "put"},
		"partial_update": {"verb": "patch"},
		"create": {"verb": "post"},
		"delete": {"verb": "delete"},
	} 

	def __init__(self, interface = {}):
		self.base_url = getattr(self.api_class, 'base_url')
		self.headers = getattr(self.api_class, 'headers')
		self.interface.update(interface)

	def extract_params(self, path):
		return re.findall(r'{(.*?)}', path)

	def get_headers(self, headers={}):
		request_headers = self.headers.copy()
		request_headers.update(headers)
		return request_headers

	def get_url(self, path, keys):

		key_options = self.extract_params(path)
		for key in key_options:
			if keys.get(key, None) is None:
				keys[key] = ""
		
		path = path . format(**keys)
		return "{}{}" . format (self.base_url, path)

	def call(self, caller, keys, data={}, params = {}, headers={}, *args, **kwargs):
		
		verb = self.interface.get(caller).get("verb")
		request_headers = self.get_headers(headers)	
		custom_resource_path = "{}_resource_path" . format (caller)
		resource_path = getattr(self, custom_resource_path, self.resource_path)	
		url = self.get_url(resource_path, keys)

		# make the call:		
		return getattr(requests, verb)(url, data=data, headers=request_headers, params=params, **kwargs)
		
	## todo: we can actually probably make these into a factory
	def get(self, keys, params = {}, headers={}, *args, **kwargs):
		http_response = self.call('get', keys, params = params, headers=headers, *args, **kwargs)
		return Response(http_response)

	def list(self, keys = {}, params = {}, headers={}, *args, **kwargs):
		http_response = self.call('list', keys, params = params, headers=headers, *args, **kwargs)
		return Response(http_response, many=True)

	def create(self, data, keys = {}, params = {}, headers={}, *args, **kwargs):

		http_response = self.call('create', keys, data=json.dumps(data), params = params, headers=headers, *args, **kwargs)
		return Response(http_response)

	def update(self, data, keys = {}, params = {}, headers={}, *args, **kwargs):
		http_response = self.call('update', keys, data=json.dumps(data), params = params, headers=headers, *args, **kwargs)
		return Response(http_response)

	def partial_update(self, data, keys = {}, params = {}, headers={}, *args, **kwargs):
		http_response = self.call('partial_update', keys, data=json.dumps(data), params = params, headers=headers, *args, **kwargs)
		return Response(http_response)

	def create_or_update(self):
		pass

	def delete(self, keys, params = {}, headers={}, *args, **kwargs):
		http_response = self.call('delete', keys, params = params, headers=headers, *args, **kwargs)
		return Response(http_response)

