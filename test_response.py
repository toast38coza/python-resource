import unittest
from resource import Response, ResourceItem

class MockResponse(object):
	id = None
	status_code = None 
	json_in = None

	def __init__(self, id, status_code, json):
		self.id = id
		self.status_code = status_code
		self.json_in = json 

	def json(self):
		return self.json_in

class ResponseTestCase(unittest.TestCase):
	"""
	Testing the basic use-case
	"""

	def setUp(self):

		json = {
			"foo": "bar",
			"baz": "bus",
		}

		self.mock_response = MockResponse(id=123, status_code=200, json=json)
		self.response = Response(self.mock_response)

	def test_init_sets_status_code(self):
		assert self.response.status_code == 200

	def test_init_sets_http_response(self):
		assert self.response.response.id == 123

	def test_init_sets_resource(self):
		assert isinstance(self.response.resource, ResourceItem) 

	def test_json_response_to_resource_item(self):

		assert self.response.resource.foo == "bar"
		assert self.response.resource.baz == "bus"

	@unittest.skip("Coming soon")
	def test_it_handles_nested_objects(self):
		pass
		
class ResponseManyTestCase(unittest.TestCase):

	def setUp(self):
		json = [
			{"first_name": "John"},
			{"first_name": "Peter"},
			{"first_name": "Clark"},
		]
		mock_response = MockResponse(id=123, status_code=200, json=json)
		self.response = Response(mock_response, many=True)

	def test_sets_resource_objects(self):
		num_objects = len(self.response.objects)
		assert num_objects == 3, \
			'Expected 3 objects, got: {}' . format (num_objects)

	def test_objects_are_correctly_set(self):
		first_names = ["John", "Peter", "Clark"]
		for index, item in enumerate(self.response.objects):
			assert item.first_name == first_names[index]
		


if __name__ == '__main__':
    unittest.main() 		

