from py_patterns.adapters import Field, Adapter
from absl.testing import absltest


# Test adapter class
class PersonAdapter(Adapter):
    last_name = Field(source="person.last_name", dtype=str)
    first_name = Field(source="person.first_name", dtype=str)
    age = Field(source="person.age", dtype=int)


class AdapterTest(absltest.TestCase):
    def setUp(self):
        super().setUp()

    def test_adapter(self):
        """test if adapter is working correct"""
        source_data = {
            "person": {"last_name": "Smith", "first_name": "John", "age": 30}
        }
        expected_data = {"last_name": "Smith", "first_name": "John", "age": 30}
        self.assertTrue(PersonAdapter(source_data=source_data).convert(), expected_data)