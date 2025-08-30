# ArgumentParser Kwargs Extension

A Python utility for parsing keyword arguments (kwargs) from command-line arguments in `key=value` format.

## Overview

This module extends argparse to provide functionality for parsing command-line arguments in `key=value` format into dictionaries. It's particularly useful when you need to dynamically pass multiple parameters to your application without predefining every possible argument.

## Features

- **Key-Value Parsing**: Converts `key=value` format arguments into dictionaries
- **Automatic Type Inference**: Smart conversion of values to appropriate Python types (numbers, booleans, strings, etc.)
- **Seamless Integration**: Works naturally with argparse's existing functionality
- **Simple API**: Intuitive interface that requires minimal configuration

## Usage

### Basic Setup

```python
import argparse
from con24ma.action import opt_action

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

# Mixed data types
python script.py --config host=localhost port=8080 debug=False timeout=30.5
# Result: {'host': 'localhost', 'port': 8080, 'debug': False, 'timeout': 30.5}

# Complex data structures
python script.py --config "items=[1,2,3]" "metadata={\"version\":\"1.0\"}"
# Result: {'items': [1, 2, 3], 'metadata': {'version': '1.0'}}
```

### Complete Example

```python
import argparse
from con24ma.action import opt_action

def main():
    parser = argparse.ArgumentParser(description='Application with dynamic configuration')
    
    # Regular arguments
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    # Dynamic configuration parameters
    parser.add_argument('--params', nargs='*', action=opt_action('parse_kwargs'),
                       help='Additional parameters in key=value format')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Verbose mode enabled")
    
    if args.params:
        print("Configuration parameters:")
        for key, value in args.params.items():
            print(f"  {key}: {value} (type: {type(value).__name__})")
    else:
        print("No configuration parameters provided")

if __name__ == '__main__':
    main()
```

### Running the Example

```bash
python example.py --verbose --params host=localhost port=8080 debug=True

#Output:
Verbose mode enabled
Configuration parameters:
  host: localhost (type: str)
  port: 8080 (type: int)
  debug: True (type: bool)
```

## Type Conversion

The module automatically recognizes and converts the following Python literal types:

| Input Format | Python Type | Example |
|--------------|-------------|---------|
| `42` | `int` | `42` |
| `3.14` | `float` | `3.14` |
| `True`, `False` | `bool` | `True`, `False` |
| `[1,2,3]` | `list` | `[1, 2, 3]` |
| `{"key":"value"}` | `dict` | `{"key": "value"}` |
| `(1,2)` | `tuple` | `(1, 2)` |
| `None` | `NoneType` | `None` |
| Everything else | `str` | `"text"` |

## API Reference

### `opt_action(key: str)`

Factory function that returns the appropriate action class for the given key.

**Parameters:**

- `key` (str): The action identifier. Use `'parse_kwargs'` to get the kwargs parsing action.

**Returns:**

- Action class for use with argparse, or the original key if no special action is found.

**Example:**

```python
action = opt_action('parse_kwargs')  # Returns ParseKwargs class
parser.add_argument('--config', nargs='*', action=action)
```

### `ParseKwargs`

Custom argparse Action class that handles kwargs parsing.

**Inherits from:** `argparse.Action`

**Behavior:**

- Expects a list of `key=value` strings as input
- Splits each string on the first `=` character
- Attempts type conversion using `ast.literal_eval()`
- Falls back to string type if conversion fails
- Sets the parsed dictionary as the argument value

## Integration with DataClass Configuration

This module is designed to work seamlessly with the broader configuration system:

```python
from dataclasses import dataclass
from con24ma import DataClassConfig, DictField

@dataclass
class AppConfig(DataClassConfig):
    # Automatically uses ParseKwargs action
    runtime_config: dict = DictField(help="Runtime configuration parameters")

# Usage
config, remaining = AppConfig.parse_args()
# Command: python app.py --runtime-config host=localhost port=8080
```

## Requirements

- Python 3.9+
- No external dependencies (uses only standard library)

## Limitations

- Keys cannot contain `=` characters (first `=` is used as delimiter)
- Complex nested structures may require careful shell escaping
- Type inference is limited to Python literal types
