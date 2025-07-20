# Field Types for DataClass Configuration

A collection of specialized field types for use with DataClass configuration parsers, providing enhanced command-line argument handling with type-specific behaviors.

## Overview

This module defines field types that extend basic dataclass fields with argparse-specific functionality. Each field type encapsulates both the value and the argument parsing configuration, making it easy to create sophisticated command-line interfaces from dataclass definitions.

## Features

- **Type-Specific Fields**: Specialized fields for different data types (args, dicts, paths)
- **Flexible Argument Configuration**: Support for custom destinations, actions, and parsing options
- **Path Handling**: Intelligent path field with file/directory detection
- **Dictionary Parsing**: Built-in support for key=value argument parsing
- **Type Conversion**: Automatic type conversion with built-in Python type support

## Field Types

### `ArgField`

Base field type for standard command-line arguments.

```python
from dataclasses import dataclass
from your_module import ArgField

@dataclass
class Config:
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

### `DictField`

Specialized field for parsing dictionary arguments using key=value syntax.

```python
@dataclass
class Config:
    # Parse arguments like: --config key1=value1 key2=value2
    config: dict = DictField({}, help="Configuration key=value pairs")
    
    # With default values
    settings: dict = DictField({"debug": False, "timeout": 30}, 
                              help="Application settings")
```

#### Features
- Automatically sets `action='parse_kwargs'` and `nargs='*'`
- Parses `key=value` pairs into dictionary
- Supports type inference for values

#### Command Line Usage
```bash
python script.py --config host=localhost port=8080 debug=True
# Results in: {"host": "localhost", "port": 8080, "debug": True}
```

### `PathField`

Specialized field for file and directory path arguments with intelligent path handling.

```python
@dataclass
class Config:
    input_file: str = PathField("input.txt", help="Input file path")
    output_dir: str = PathField("./output", as_rootdir=True, help="Output directory")
    config_file: str = PathField("config.json", as_cfgpath=True, help="Config file")
```

#### Parameters
- `value`: Default path value
- `dest`: Custom argument name(s)
- `as_rootdir`: Boolean flag for directory handling
- `as_cfgpath`: Boolean flag for configuration file handling
- `**kwargs`: Additional argparse arguments

#### Features
- Uses `getpath()` utility for path resolution
- Automatic file/directory detection
- Special handling for configuration files and root directories

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

## Usage Examples

### Basic Configuration

```python
from dataclasses import dataclass
from your_module import ArgField, DictField, PathField

@dataclass
class AppConfig:
    # Basic arguments
    name: str = ArgField("myapp", help="Application name")
    port: int = ArgField(8080, help="Port to listen on")
    debug: bool = ArgField(False, help="Enable debug mode")
    
    # Dictionary configuration
    settings: dict = DictField({}, help="Additional settings as key=value pairs")
    
    # Path handling
    config_file: str = PathField("app.conf", as_cfgpath=True, help="Configuration file")
    data_dir: str = PathField("./data", as_rootdir=True, help="Data directory")
```

### Advanced Field Configuration

```python
@dataclass
class AdvancedConfig:
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

### Command Line Usage

```bash
# Basic usage
python app.py --name "MyApp" --port 3000 --debug

# With dictionary settings
python app.py --settings timeout=30 retries=3 ssl=True

# With paths
python app.py --config-file /etc/myapp.conf --data-dir /var/data

# Advanced options
python app.py -v --log-level DEBUG --api-key abc123 --files file1.txt file2.txt
```

## Integration with DataClassConfig

These field types are designed to work seamlessly with the DataClassConfig system:

```python
@dataclass
class Config(DataClassConfig):
    app_name: str = ArgField("default", help="Application name")
    config: dict = DictField({}, help="Configuration parameters")
    log_file: str = PathField("app.log", help="Log file path")

# Automatic parser generation and argument handling
config, remaining = Config.parse_args()
```

## Type Conversion

ArgField supports automatic type conversion through magic methods:

```python
field = ArgField(42)
print(str(field))    # "42"
print(int(field))    # 42
print(float(field))  # 42.0
print(bool(field))   # True
```

## Dependencies

- `con24ma.action`: For `opt_action()` function
- `con24ma.pathutil`: For `getpath()` utility
- Standard library: `typing`

## Notes

- PathField appears to have some incomplete implementation (see `self.admin` assignment)
- DictField automatically integrates with the kwargs parsing system
- All fields support the standard argparse argument options
- Custom destinations allow for both short and long argument forms

## Requirements

- Python 3.9+
- Dependencies: con24ma.action, con24ma.pathutil modules

## License

This project is released under [appropriate license].