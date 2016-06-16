import unittest, responses, json
from resource import Resource, API

class FooAPI(API):
	base_url = "https://api.foo.com"
	headers = {"foo": "bar"}

class SimpleResource(Resource):
	resource_path = '/api/v1/foo/{id}'
	api_class=FooAPI

class BarResource(Resource):
	resource_path = '/api/v1/{user}/{id}'
	api_class=FooAPI

class ResourceTestCase(unittest.TestCase):

	def setUp(self):
		self.resource = BarResource()

	def test_init_resource(self):
		pass

	def test_init_resource_sets_base_url_from_api_class(self):	
		assert self.resource.base_url == 'https://api.foo.com'

	def test_init_resource_sets_headers_from_api_class(self):	
		assert self.resource.headers.get('foo') == 'bar'

	def test_extract_params(self):
		
		params = self.resource.extract_params('/test/{user}/{id}')
		assert params == ['user', 'id']

	def test_get_url(self):
		test_urls = [
			('/repo/{user}/{id}', {"user": "test", "id": "123"}, '/repo/test/123',),
			('/repo/{user}/{id}', {"user": "test"}, '/repo/test/',),
			('/repo/{id}', {"id": "123"}, '/repo/123',),
		]
		for url, keys, expected_path in test_urls:
			actual_url = self.resource.get_url(url, keys)
			expected_url = "{}{}" . format ("https://api.foo.com", expected_path)
			assert actual_url == expected_url, \
				'Expected {} with keys: {} to be: {}, but it was: {}' \
					. format (url, keys, expected_url, actual_url)

class ResourceGetTestCase(unittest.TestCase):

	def setUp(self):
		self.resource = BarResource()

	@responses.activate
	def test_get(self):

		responses.add(responses.GET, 'https://api.foo.com/api/v1/test/123',
                  body='{"some": "result"}', status=200,
                  content_type='application/json')

		keys = {"user":"test", "id":123}
		result = self.resource.get(keys)

	@responses.activate
	def test_get_custom_headers(self):

		responses.add(responses.GET, 'https://api.foo.com/api/v1/test/123')

		keys = {"user":"test", "id":123}
		result = self.resource.get(keys, headers= {"baz": "bus"})

		responses.calls[0].request.headers['foo'] == 'bar'
		responses.calls[0].request.headers['baz'] == 'bus'	

	@responses.activate
	def test_get_with_basic_auth(self):
		responses.add(responses.GET, 'https://api.foo.com/api/v1/test/123')

		keys = {"user":"test", "id":123}
		extra_args = {"auth": ('username','password')}
		result = self.resource.get(keys, **extra_args)

		call = responses.calls[0]
		
		assert call.request.headers.get('Authorization') == 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='


	@responses.activate
	def test_can_define_custom_resource_path_for_method(self):
		
		class MultiPathResource(Resource):
			resource_path = '/api/v1/{user}/{id}'
			get_resource_path = '/special/get/endpoint/{id}'
			api_class=FooAPI

		responses.add(responses.GET, 'https://api.foo.com/special/get/endpoint/123',
                  body='{"some": "result"}', status=200,
                  content_type='application/json')

		resource = MultiPathResource()
		resource.get({"id": "123"})

class ResourceQueryTestCase(unittest.TestCase):

	def setUp(self):
		self.resource = BarResource()
		self.simple_resource = SimpleResource()

	@responses.activate
	def test_query(self):

		expected_url = "https://api.foo.com/api/v1/test/"
		response = [
			{"id": 1},
			{"id": 2},
			{"id": 3},
		]
		responses.add(responses.GET, expected_url, body=json.dumps(response), status=200)
		qs = "?q=a%3D1%3Ab%3D2&s=something"
		keys = {'user': 'test'}
		params = {'q': 'a=1:b=2', 's': 'something'}
		result = self.resource.list(keys=keys, params=params)

		call = responses.calls[0]

		expected_params = [
			'q=a%3D1%3Ab%3D2',
			's=something'
		]
		for param in expected_params:
			assert param in call.request.url, \
				"Expected {} to be in {}" . format (param, call.request.url)

class ResourceCreateTestCase(unittest.TestCase):

	@responses.activate
	def test_create_simple_resource_with_data(self):

		responses.add(responses.POST, "https://api.foo.com/api/v1/foo/")
		data = {"first_name": "John", "last_name": "Snow"}
		repo = SimpleResource().create(data)

	@responses.activate
	def test_create_with_custom_resource_path(self):

		responses.add(responses.POST, "https://api.foo.com/special/create/endpoint")

		class MultiPathResource(Resource):
			resource_path = '/api/v1/{user}/{id}'
			create_resource_path = '/special/create/endpoint'
			api_class=FooAPI

		data = {"foo": "bar"}
		MultiPathResource().create(data)

class ResourceUpdateTestCase(unittest.TestCase):

	def setUp(self):
		self.resource = SimpleResource()

	@responses.activate
	def test_update(self):
		
		responses.add(responses.PUT, "https://api.foo.com/api/v1/foo/123")		
		result = self.resource.update(keys={"id": 123}, data={"foo":"bar"})
		call = responses.calls[0]
		assert call.request.body == '{"foo": "bar"}'

	@responses.activate
	def test_partial_update(self):
		
		responses.add(responses.PATCH, "https://api.foo.com/api/v1/foo/123")		
		result = self.resource.partial_update(keys={"id": 123}, data={"foo":"bar"})
		call = responses.calls[0]
		assert call.request.body == '{"foo": "bar"}'

class ResourceDeleteTestCase(unittest.TestCase):

	@responses.activate
	def test_delete_simple_resource_with_data(self):

		responses.add(responses.DELETE, "https://api.foo.com/api/v1/foo/123")
		repo = SimpleResource().delete({"id": 123})


if __name__ == '__main__':
    unittest.main() 		