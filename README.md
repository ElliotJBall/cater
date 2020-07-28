# cater
"Provide with what is needed or required"

A (probably weird) way to convert JSON structures into python classes.

## Why
I wanted a quick and easy way that I could generate a series of classes representing a JSON structure and subsequently use instead of dictionaries/raw JSON. 

## Usage
cater attempts to support JSON provided either as an argument or a path to a JSON file:

```python
# File based usage
python main.py -f /path/to/file.json
```

```python
# Argument based usage
python main.py -s '{ "name": "John", "age": 30, "car": null }'
```


## Tests
Tests can be run with the following command:

```python
python test.py
```

## Example usage
1. Running the following python command:
```python
    python main.py -f examples/basic.json
```
2. Generates a new folder called 'output' with a single file called 'TopLevelParent.py' that contains the following python code:
```python
class Toplevelparent:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.age = kwargs.get('age', None)
        self.car = kwargs.get('car', None)
```
3. My inteded usage from here was to simply use the built-in json module and pass the parsed JSON string into the 'Parent' class like so:
```python
obj = Toplevelparent(**json.loads(raw))
```
4. Now you have a series of python classes representing the JSON:
```python
print(obj.name)
> John
```


### License
MIT License

Copyright (c) 2019 Elliot Ball

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
