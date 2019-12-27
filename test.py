import unittest
import main
import os
import json

EXAMPLES_DIR = os.path.join(os.getcwd(), "examples")
PARENT_CLASS_NAME = 'TopLevelParent'


class TestCater(unittest.TestCase):

    def test_can_convert_basic_json_to_class_prop_dict(self):
        with open(os.path.join(EXAMPLES_DIR, 'basic.json')) as json_file:
            value = json.load(json_file)
            result = main.extract_classes_from_json(value, {})

            self.assertTrue(PARENT_CLASS_NAME in result.keys())

            for key in value:
                self.assertTrue(key in result[PARENT_CLASS_NAME])

    def test_can_convert_single_nested_object_to_class_prop_dict(self):
        with open(os.path.join(EXAMPLES_DIR, 'single_nested_objects.json')) as json_file:
            value = json.load(json_file)
            result = main.extract_classes_from_json(value, {})

            self.assertTrue(PARENT_CLASS_NAME in result.keys())
            self.assertTrue('car' in result.keys())

            for key in value:
                self.assertTrue(key in result[PARENT_CLASS_NAME])

    def test_can_convert_multiple_nested_object_to_class_prop_dict(self):
        with open(os.path.join(EXAMPLES_DIR, 'multiple_nested_objects.json')) as json_file:
            value = json.load(json_file)
            result = main.extract_classes_from_json(value, {})

            expected_class_names = [PARENT_CLASS_NAME, 'filters', 'matches', 'competition',
                                    'season', 'winner', 'score', 'fullTime', 'halfTime',
                                    'extraTime', 'penalties', 'homeTeam', 'awayTeam']

            for expected_class in expected_class_names:
                self.assertTrue(expected_class in result.keys())

            for key in value:
                self.assertTrue(key in result[PARENT_CLASS_NAME])


if __name__ == '__main__':
    unittest.main()
