import argparse
import json
import os
import re
from typing import Dict

OUTPUT_DIR = os.path.join(os.getcwd(), "output")


def cater():
    remove_output_folder()

    os.makedirs(OUTPUT_DIR)

    parsed_json = get_json()
    build_classes_from_json(parsed_json)


def remove_output_folder():
    """Remove all files (and folders) from the output directory, then remove the output directory itself.
     Taken directly from the Python docs:
        https://docs.python.org/3/library/os.html#os.walk
     """
    for root, dirs, files in os.walk(OUTPUT_DIR, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
        os.rmdir(root)


def get_json() -> Dict:
    """Parse incoming string / file and retrieve the JSON"""
    parser = argparse.ArgumentParser(description='Generate python classes directly from JSON')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', type=str, help='Provide the JSON directly via the command line')
    group.add_argument('-f', help='The file location for the JSON to parse')

    args = parser.parse_args()

    if args.s:
        value = json.loads(''.join(args.s))
    elif args.f:
        if os.path.isfile(args.f):
            with open(args.f) as json_file:
                value = json.load(json_file)
        else:
            raise ValueError("Please provide a valid file that contains JSON")
    else:
        raise ValueError('No JSON has been provided')

    return value


def build_classes_from_json(p_json: Dict) -> None:
    """Use the parsed JSON and generate the skeleton python classes.

    Keyword arguments:
    p_json (str) -- The JSON in Dict format after being parsed by json.load / json.loads
    """

    # Build a class for each key in the incoming JSON whose value is a dict

    # TODO - Nested dict's inside dict, traverse all child objects, create a stack to build in right order and have
    #  parent -> child relationship
    for key in p_json.keys():

        if isinstance(p_json[key], list) and len(p_json[key]) > 1 and isinstance(p_json[key][0], dict):
            build_class(key, p_json[key][0])
        elif isinstance(p_json[key], dict):
            build_class(key, p_json[key])


def build_class(key: str, p_dict: Dict) -> None:
    """Using a subset of the parsed JSON, parse the Dict and build a new Python class.

    Keyword arguments:
    key (str) -- The JSON key that points to the parsed dict. Used for filename + class name
    p_dict (Dict) -- A dict subset of the parsed JSON, represents an object we want to build
    """
    filename = os.path.join(OUTPUT_DIR, key.capitalize() + '.py')
    classname = key.capitalize()

    with open(filename, 'w') as pyfile:
        pyfile.write('class {}:'.format(classname))
        pyfile.write('\n')
        pyfile.write('    def __init__(self, **kwargs):')
        pyfile.write('\n')

        for prop in p_dict.keys():
            prop = convert(prop)

            pyfile.write('        self.{} = kwargs.get(\'{}\', None)'.format(prop, prop))
            pyfile.write('\n')


def convert(word: str) -> str:
    """Convert the incoming JSON property to snake_case if deemed to be
    camelCase.

    Keyword arguments:
    word (str) -- The incoming JSON property
    """
    if len(re.findall(r'(?:[A-Z][a-z]*)+', word)) > 0:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    else:
        return word


if __name__ == "__main__":
    cater()