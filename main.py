import argparse
import json
import os
import re
from typing import Dict

OUTPUT_DIR = os.path.join(os.getcwd(), "output")


def banner():
    print("""
 ______     ______     ______   ______     ______    
/\  ___\   /\  __ \   /\__  _\ /\  ___\   /\  == \   
\ \ \____  \ \  __ \  \/_/\ \/ \ \  __\   \ \  __<   
 \ \_____\  \ \_\ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_____/   \/_/\/_/     \/_/   \/_____/   \/_/ /_/ 
     """)


def cater():
    remove_output_folder()
    os.makedirs(OUTPUT_DIR)

    parsed_json = get_json()
    classes_props = extract_classes_from_json(parsed_json, {})

    print('About to generate the following classes: {}'.format(classes_props.keys()))

    for key_prop in classes_props.keys():
        build_class(key_prop, classes_props[key_prop])


def remove_output_folder():
    """Remove all files (and folders) from the output directory, then remove the output directory itself.
     Taken directly from the Python docs: https://docs.python.org/3/library/os.html#os.walk
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


def extract_classes_from_json(p_json: Dict, keys_props: Dict) -> Dict:
    """Recursively traverse JSON tree and check for child 'complex' objects (dicts), also
    add them to the dict of classes that needs building.

    Keyword arguments:
    p_json (str) -- The JSON
    keys_props (dict) -- The key is the complex objects name, value is the list of properties of that object.
    """
    for key in p_json.keys():
        if isinstance(p_json[key], list) and len(p_json[key]) > 1 and isinstance(p_json[key][0], dict):
            keys_props[key] = p_json[key][0]
            extract_classes_from_json(p_json[key][0], keys_props)
        elif isinstance(p_json[key], dict):
            keys_props[key] = p_json[key]
            extract_classes_from_json(p_json[key], keys_props)

    return keys_props


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
    banner()
    cater()
