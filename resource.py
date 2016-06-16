import requests
import re

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

		if response.status_code == 200: 
			if many:
				self.objects = []
				for item in response.json():
					resource = self.dict_to_resource_item(item)
					self.objects.append(resource)
			else:
				self.resource = self.dict_to_resource_item(response.json())

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


class Resource(object):

	resouce_path = None
	objects = []

	def __init__(self):
		self.base_url = getattr(self.api_class, 'base_url')
		self.headers = getattr(self.api_class, 'headers')

	def extract_params(self, path):
		return re.findall(r'{(.*?)}', path)

	def get_url(self, path, keys):

		key_options = self.extract_params(path)
		for key in key_options:
			if keys.get(key, None) is None:
				keys[key] = ""
		
		path = path . format(**keys)
		return "{}{}" . format (self.base_url, path)

	def get(self, keys, params = {}, headers={}, *args, **kwargs):

		request_headers = self.headers.copy()
		request_headers.update(headers)
		
		url = self.get_url(self.resource_path, keys)
		http_response = requests.get(url, headers=request_headers, params=params)

		if http_response.status_code == 200:
			return Response(http_response)

	def list(self, keys = {}, params = {}, headers={}, *args, **kwargs):
		request_headers = self.headers.copy()
		url = self.get_url(self.resource_path, keys)
		http_response = requests.get(url, headers=request_headers, params=params)
		return Response(http_response)

	def create(self, data, keys = {}, params = {}, headers={}, *args, **kwargs):
		pass

	def update(self):
		pass

	def delete(self):
		pass
