# ArgumentParser Kwargs Extension

A Python utility for easily parsing keyword arguments (kwargs) from command-line arguments.

## Overview

This module extends argparse to provide functionality for parsing command-line arguments in `key=value` format into dictionaries. It's particularly useful when you need to dynamically pass multiple parameters to your application.

## Features

- Automatically converts `key=value` format arguments into dictionaries
- Automatic type inference for values (numbers, booleans, strings, etc.)
- Seamless integration with argparse
- Simple and intuitive API

## Usage

### Basic Usage

```python:script.py
import argparse
from your_module import opt_action

parser = argparse.ArgumentParser()
parser.add_argument(
    '--config',
    nargs='*',
    action=opt_action('parse_kwargs'),
    help='Configuration parameters in key=value format'
)

args = parser.parse_args()
print(args.config)
```

### Command Line Examples

```bash
# Basic usage
python script.py --config name=test age=25 active=True

# Result: {'name': 'test', 'age': 25, 'active': True}
```

```bash
# Mixed types
python script.py --config host=localhost port=8080 debug=False timeout=30.5

# Result: {'host': 'localhost', 'port': 8080, 'debug': False, 'timeout': 30.5}
```

### Complete Example

```python
import argparse
from your_module import opt_action

def main():
    parser = argparse.ArgumentParser(description='Example with kwargs parsing')
    parser.add_argument('--params', nargs='*', action=opt_action('parse_kwargs'))
    
    args = parser.parse_args()
    
    if args.params:
        print("Parsed parameters:")
        for key, value in args.params.items():
            print(f"  {key}: {value} (type: {type(value).__name__})")

if __name__ == '__main__':
    main()
```

## Type Conversion

The module automatically recognizes the following types:

- **Integers**: `42` → `42` (int)
- **Floats**: `3.14` → `3.14` (float)  
- **Booleans**: `True`, `False` → `True`, `False` (bool)
- **Lists**: `[1,2,3]` → `[1, 2, 3]` (list)
- **Dictionaries**: `{"key":"value"}` → `{"key": "value"}` (dict)
- **Strings**: Everything else → kept as string

## API Reference

### `opt_action(key: str)`

Action factory function.

**Parameters:**

- `key`: Action name. When `'parse_kwargs'` is specified, returns the `ParseKwargs` action

**Returns:**

- Action class corresponding to the specified key

### `ParseKwargs`

Custom action class that inherits from argparse.Action.

**Functionality:**

- Converts a list of `key=value` strings into a dictionary
- Safe type conversion using `ast.literal_eval()`
- Falls back to string if conversion fails

## Notes

- Wrap values containing spaces in quotes: `name="John Doe"`
- Complex data structures (nested dictionaries, etc.) are supported, but be careful with shell escaping
- For security, uses `ast.literal_eval()` so executable code is not evaluated

## Requirements

- Python 3.9+
- Standard library only (no external dependencies)

## License

This project is released under [appropriate license].
