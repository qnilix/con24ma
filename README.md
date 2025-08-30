# CONfiguration tools for MAnaging your environment (con24ma)

A practical Python package for creating command-line interfaces from dataclasses with powerful argument parsing capabilities.

## Installation

```bash
pip install ./con24ma
```

## Quick Start

### Basic Setup

```python
from dataclasses import dataclass
from con24ma import DataClassConfig, ArgField, DictField

@dataclass
class Config(DataClassConfig):
    name: str = ArgField('myapp', help="Application name")
    debug: bool = ArgField(False, help="Enable debug mode")
    config: dict = DictField(help="Additional configuration")

# Parse and use
config, remaining_args = Config.parse_args()
print(f"Running {config.name} with debug={config.debug}")
```

### Command Line Usage

```bash
python script.py --name MyApp --debug --config timeout=30 retries=3
# Output: Running MyApp with debug=True
# config.config = {'timeout': 30, 'retries': 3}
```

## Real-World Example

```python
from dataclasses import dataclass
from typing import Optional
from con24ma import DataClassConfig, ArgField, DictField

@dataclass
class ModelConfig(DataClassConfig):
    # Core model settings
    model: str = ArgField('resnet50', ['-m'], help="Model architecture name")
    model_kwargs: dict = DictField(help="Additional model parameters as key=value")

    # Training settings
    pretrained: Optional[bool] = ArgField(None, help="Use pretrained weights")
    trained_file: Optional[str] = ArgField(None, help="Path to trained model file")

# Usage
config, _ = ModelConfig.parse_args()
```

```bash
python train.py -m efficientnet_b0 --pretrained --model-kwargs drop_rate=0.2 num_classes=1000
```

## Key Features

- **Type-safe**: Full dataclass type support with automatic CLI generation
- **DictField**: Built-in support for `key=value` argument parsing
- **Flexible**: Custom argument destinations, choices, validation
- **Serializable**: Easy JSON configuration save/load
- **Extensible**: Hook methods for custom processing

## Documentation

For detailed documentation and advanced usage examples:

- **[Field Types Guide](docs/FIELDS.md)** - Complete reference for ArgField, DictField, and other field types
- **[Argument Parsing Details](docs/ARG_PARSE.md)** - Deep dive into the kwargs parsing system and advanced argument handling

## Basic API

### DataClassConfig

Main base class for configuration dataclasses.

```python
@dataclass
class Config(DataClassConfig):
    # Define fields with ArgField/DictField
    pass

# Parse arguments
config, remaining = Config.parse_args()
```

### ArgField

Standard command-line argument field.

```python
# Basic usage
name: str = ArgField("default", help="Help text")

# With custom options
verbose: bool = ArgField(False, ['-v', '--verbose'], help="Verbose mode")
mode: str = ArgField("train", choices=['train', 'test'], help="Mode")
```

### DictField

Dictionary field for key=value parsing.

```python
# Parse --config key1=value1 key2=value2
config: dict = DictField(help="Configuration parameters")
```

## Best Practices

### Configuration Validation

```python
@dataclass
class Config(DataClassConfig):
    learning_rate: float = ArgField(0.001, help="Learning rate")
    
    @classmethod
    def prep_parsed(cls, parsed: dict) -> dict:
        if parsed.get('learning_rate', 0) <= 0:
            raise ValueError("Learning rate must be positive")
        return parsed
```

### Configuration Persistence

```python
import json

# Save configuration
config, _ = Config.parse_args()
with open('config.json', 'w') as f:
    json.dump(config.asdict(), f, indent=2)

# Load and merge with CLI args
with open('config.json', 'r') as f:
    saved_config = json.load(f)
config, _ = Config.parse_args(base_dict=saved_config)
```

## Requirements

- Python 3.9+
- Standard library only (no external dependencies)

## License

This project is released under MIT License.
