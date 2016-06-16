import unittest, responses
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

		responses.add(responses.GET, 'https://api.foo.com/api/v1/test/123',
                  body='{"some": "result"}', status=200,
                  content_type='application/json')

		keys = {"user":"test", "id":123}
		result = self.resource.get(keys, headers= {"baz": "bus"})

		responses.calls[0].request.headers['foo'] == 'bar'
		responses.calls[0].request.headers['baz'] == 'bus'

	def test_result_populates_objects_list_if_top_level_result_is_list(self):
		result_json = [
			{"first_name": "John", "last_name": "Snow"},
			{"first_name": "Daenerys", "last_name": "Targaryen"},
			{"first_name": "Sansa", "last_name": "Start"},
			{"first_name": "Cersei", "last_name": "Lannnister"},
		]

		responses.add(responses.GET, 'https://api.foo.com/api/v1/test/123',
                  body='{"some": "result"}', status=200,
                  content_type='application/json')


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
		responses.add(responses.GET, expected_url, body=response, status=200)
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

	def setUp(self):
		self.resource = SimpleResource()

	def test_create_simple_resource_with_data(self):
		
		self.resource.create(data)


if __name__ == '__main__':
    unittest.main() 		