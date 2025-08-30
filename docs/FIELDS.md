# Field Types for DataClass Configuration

A collection of specialized field types for use with DataClass configuration parsers, providing enhanced command-line argument handling with type-specific behaviors.

## Overview

This module defines field types that extend basic dataclass fields with argparse-specific functionality. Each field type encapsulates both the value and the argument parsing configuration, making it easy to create sophisticated command-line interfaces from dataclass definitions.

## Features

- **Type-Specific Fields**: Specialized fields for different data types (args, dicts)
- **Flexible Argument Configuration**: Support for custom destinations, actions, and parsing options
- **Dictionary Parsing**: Built-in support for key=value argument parsing
- **Type Conversion**: Automatic type conversion with built-in Python type support

## Field Types

### `ArgField`

Base field type for standard command-line arguments.

```python
from dataclasses import dataclass
from con24ma import DataClassConfig, ArgField

@dataclass
class Config(DataClassConfig):
    name: str = ArgField("default_name", help="Application name")
    port: int = ArgField(8080, help="Port number")
    debug: bool = ArgField(False, help="Enable debug mode")
    
    # Custom destination
    verbose: bool = ArgField(False, dest=['-v', '--verbose'], help="Verbose output")
```

#### Parameters

- `value`: Default value for the field
- `dest`: Custom argument name(s) - can be string or list of strings
- `**kwargs`: Additional argparse arguments (action, nargs, const, choices, required, help, metavar)

#### Magic Methods

- `__bool__()`, `__float__()`, `__int__()`, `__str__()`: Type conversion support

#### ArgField Example Usage

```python
@dataclass
class AppConfig(DataClassConfig):
    # Basic arguments
    name: str = ArgField("myapp", help="Application name")
    port: int = ArgField(8080, help="Port to listen on")
    debug: bool = ArgField(False, help="Enable debug mode")
    
    # Multiple argument names
    verbose: bool = ArgField(False, 
                            dest=['-v', '--verbose'], 
                            help="Enable verbose output")
    
    # Choices constraint
    log_level: str = ArgField("INFO", 
                             choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                             help="Logging level")
    
    # Required argument
    api_key: str = ArgField(None, 
                           required=True,
                           help="API key (required)")
    
    # Multiple values
    files: list = ArgField([], 
                          nargs='+',
                          help="Input files")
```

### `DictField`

Specialized field for parsing dictionary arguments using key=value syntax.

- Automatically sets `action='parse_kwargs'` and `nargs='*'`
- Parses `key=value` pairs into dictionary
- Supports type inference for values using `ast.literal_eval()`

```python
@dataclass
class Config(DataClassConfig):
    # Parse arguments like: --config key1=value1 key2=value2
    config: dict = DictField({}, help="Configuration key=value pairs")
    
    # With default values
    settings: dict = DictField({"debug": False, "timeout": 30}, 
                              help="Application settings")
```

#### CLI Usage Examples

```bash
python script.py --config host=localhost port=8080 debug=True
# Results in: {"host": "localhost", "port": 8080, "debug": True}
```

#### Type Conversion

The DictField automatically recognizes the following types:

- **Integers**: `42` → `42` (int)
- **Floats**: `3.14` → `3.14` (float)  
- **Booleans**: `True`, `False` → `True`, `False` (bool)
- **Lists**: `[1,2,3]` → `[1, 2, 3]` (list)
- **Dictionaries**: `{"key":"value"}` → `{"key": "value"}` (dict)
- **Strings**: Everything else → kept as string

#### DictField Examples

```bash
# Basic usage
python script.py --params name=test age=25 active=True
# Result: {'name': 'test', 'age': 25, 'active': True}

# Mixed types
python script.py --params host=localhost port=8080 debug=False timeout=30.5
# Result: {'host': 'localhost', 'port': 8080, 'debug': False, 'timeout': 30.5}

# Complex types (be careful with shell escaping)
python script.py --params "data=[1,2,3]" "config={\"key\":\"value\"}"
```

## Utility Functions

### `argument_of_AP()`

Helper function that creates argparse argument dictionaries with proper action resolution.

```python
def argument_of_AP(action=None, nargs=None, const=None, 
                   choices=None, required=None, help=None, metavar=None):
    # Returns configured argument dictionary for argparse
```

### `argfield()`

Factory function for creating ArgField instances with flexible parameter handling.

```python
# Using default value
field1 = argfield(default="value", help="Help text")

# Using default factory
field2 = argfield(default_factory=list, help="List field")
```

## Practical Usage Examples

### Basic Configuration

```python
from dataclasses import dataclass
from con24ma import DataClassConfig, ArgField, DictField

@dataclass
class AppConfig(DataClassConfig):
    # Basic arguments
    name: str = ArgField("myapp", help="Application name")
    port: int = ArgField(8080, help="Port to listen on")
    debug: bool = ArgField(False, help="Enable debug mode")
    
    # Dictionary configuration
    settings: dict = DictField({}, help="Additional settings as key=value pairs")
```

### Advanced Field Configuration

```python
@dataclass
class AdvancedConfig(DataClassConfig):
    # Multiple argument names
    verbose: bool = ArgField(False, 
                            dest=['-v', '--verbose'], 
                            help="Enable verbose output")
    
    # Choices constraint
    log_level: str = ArgField("INFO", 
                             choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                             help="Logging level")
    
    # Required argument
    api_key: str = ArgField(None, 
                           required=True,
                           help="API key (required)")
    
    # Multiple values
    files: list = ArgField([], 
                          nargs='+',
                          help="Input files")
    
    # Dictionary with defaults
    model_config: dict = DictField({"layers": 3, "units": 128}, 
                                  help="Model configuration")
```

### Command Line Usage

```bash
# Basic usage
python app.py --name "MyApp" --port 3000 --debug

# With dictionary settings
python app.py --settings timeout=30 retries=3 ssl=True

# Advanced options
python app.py -v --log-level DEBUG --api-key abc123 --files file1.txt file2.txt

# Model configuration
python app.py --model-config layers=5 units=256 dropout=0.1
```

## Integration with DataClassConfig

These field types are designed to work seamlessly with the DataClassConfig system:

```python
@dataclass
class Config(DataClassConfig):
    app_name: str = ArgField("default", help="Application name")
    config: dict = DictField({}, help="Configuration parameters")
    
    @classmethod
    def prep_parsed(cls, parsed: dict) -> dict:
        # Custom validation/processing
        if parsed.get('app_name') == 'forbidden':
            raise ValueError("Invalid app name")
        return parsed

# Automatic parser generation and argument handling
config, remaining = Config.parse_args()
```

## Notes

- DictField automatically integrates with the kwargs parsing system via `ParseKwargs` action
- All fields support the standard argparse argument options
- Custom destinations allow for both short and long argument forms
- Type conversion in DictField uses `ast.literal_eval()` for safety
