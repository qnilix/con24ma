# CONfiguration tools for MAnaging your environment (con24ma)

A practical guide showing how to use the DataClass Configuration system with real-world examples, including model configuration management.

## Quick Start

### 1. Basic Setup

```python:script.py
from dataclasses import dataclass
from typing import Optional
from con24ma import DataClassConfig, ArgField, DictField

@dataclass
class Config(DataClassConfig):
    name: str = ArgField('myapp', help="Application name")
    debug: bool = ArgField(False, help="Enable debug mode")
    config: dict = DictField(help="Additional configuration")

# Parse and use
config, _ = Config.parse_args()
print(f"Running {config.name} with debug={config.debug}")
```

### 2. Command Line Usage

```bash
python script.py --name MyApp --debug --config timeout=30 retries=3
# Running MyApp with config={timeout: 30, retries=3}
```

## Real-World Example: Model Configuration

Here's a complete example based on machine learning model configuration:

### Model Configuration Class

```python
from dataclasses import dataclass
from typing import Optional
from your_module import DataClassConfig, ArgField, DictField

@dataclass
class ModelCfg(DataClassConfig):
    # Core model settings
    model: str = ArgField('resnet50', ['-m'], help="Model architecture name")
    model_kwargs: dict = DictField(help="Additional model parameters as key=value")

    # Training settings
    pretrained: Optional[bool] = ArgField(None, help="Use pretrained weights")
    trained_file: Optional[str] = ArgField(None, help="Path to trained model file")

```

### Usage Examples

#### Basic Model Creation

```python
# Create default ResNet50
config, _ = ModelCfg.parse_args([])
model = config.create_model()
```

#### Command Line Examples

```bash
# Use different model
python train.py -m efficientnet_b0 --pretrained

# With custom parameters
python train.py -m resnet50 --model-kwargs drop_rate=0.2 num_classes=1000

# Export-ready model
python export.py -m mobilenet_v3 --scriptable --exportable

# Load trained model
python inference.py -m resnet50 --trained-file ./models/best.pth

# Complex configuration
python train.py \
    --model efficientnet-b3 \
    --model-kwargs drop_rate=0.3 drop_path_rate=0.2 \
    --task-name classification \
    --pretrained \
    --scriptable
```

## More Quick Use Examples

### 1. Training Configuration

```python
@dataclass
class TrainingConfig(DataClassConfig):
    # Model config as nested dataclass
    model: ModelCfg = ModelCfg
    
    # Training parameters
    batch_size: int = ArgField(32, help="Batch size")
    learning_rate: float = ArgField(0.001, help="Learning rate")
    epochs: int = ArgField(100, help="Number of epochs")
    
    # Data settings
    data_dir: str = PathField("./data", help="Data directory")
    train_split: float = ArgField(0.8, help="Training split ratio")
    
    # Optimization
    optimizer: str = ArgField('adam', choices=['adam', 'sgd', 'rmsprop'])
    scheduler: dict = DictField(help="Scheduler parameters")

# Usage
config, _ = TrainingConfig.parse_args()
model = config.model.create_model()
```

```bash
python train.py \
    --model resnet50 \
    --batch-size 64 \
    --learning-rate 0.01 \
    --optimizer sgd \
    --scheduler step_size=30 gamma=0.1
```

### 2. Data Processing Pipeline

```python
@dataclass
class DataConfig(DataClassConfig):
    input_path: str = PathField(required=True, help="Input data path")
    output_path: str = PathField("./output", help="Output directory")
    
    # Processing options
    resize: Optional[tuple] = ArgField(None, help="Resize dimensions (width,height)")
    normalize: bool = ArgField(True, help="Apply normalization")
    augment: dict = DictField(help="Data augmentation parameters")
    
    # Performance
    num_workers: int = ArgField(4, help="Number of worker processes")
    batch_size: int = ArgField(32, help="Processing batch size")

# Usage
config, _ = DataConfig.parse_args()
```

```bash
python process.py \
    --input-path ./raw_data \
    --output-path ./processed \
    --resize "(224,224)" \
    --augment rotation=15 brightness=0.2 \
    --num-workers 8
```

### 3. Experiment Configuration

```python
@dataclass
class ExperimentConfig(DataClassConfig):
    # Experiment metadata
    name: str = ArgField(required=True, help="Experiment name")
    description: str = ArgField("", help="Experiment description")
    tags: list = ArgField(default_factory=list, nargs='*', help="Experiment tags")
    
    # Model and training
    model: ModelCfg = ModelCfg
    training: TrainingConfig = TrainingConfig
    
    # Logging and checkpoints
    log_dir: str = PathField("./logs", help="Logging directory")
    checkpoint_freq: int = ArgField(10, help="Checkpoint frequency (epochs)")
    
    # Evaluation
    eval_freq: int = ArgField(5, help="Evaluation frequency (epochs)")
    metrics: list = ArgField(['accuracy', 'loss'], nargs='*', help="Metrics to track")

def run_experiment():
    config, _ = ExperimentConfig.parse_args()
    
    print(f"Starting experiment: {config.name}")
    print(f"Model: {config.model.model}")
    print(f"Config: {config.asdict()}")
    
    # Create model
    model = config.model.create_model()
    
    # Run training...
    # ... training logic here ...

if __name__ == "__main__":
    run_experiment()
```

```bash
python experiment.py \
    --name "resnet50_baseline" \
    --description "Baseline ResNet50 experiment" \
    --tags baseline resnet50 \
    --model resnet50 \
    --batch-size 64 \
    --learning-rate 0.001 \
    --epochs 200 \
    --metrics accuracy f1_score loss
```

## Best Practices

### 1. Configuration Validation

```python
@dataclass
class Config(DataClassConfig):
    learning_rate: float = ArgField(0.001, help="Learning rate")
    
    @classmethod
    def prep_parsed(cls, parsed: dict) -> dict:
        # Validate learning rate
        if parsed.get('learning_rate', 0) <= 0:
            raise ValueError("Learning rate must be positive")
        return parsed
```

### 2. Configuration Serialization

```python
# Save configuration
config, _ = Config.parse_args()
with open('config.json', 'w') as f:
    json.dump(config.asdict(), f, indent=2)

# Load and modify configuration
with open('config.json', 'r') as f:
    saved_config = json.load(f)
    
# Override with command line
config, _ = Config.parse_args(kwargs=saved_config)
```

### 3. Environment Integration

```python
@dataclass
class Config(DataClassConfig):
    api_key: str = ArgField(None, help="API key")
    
    @classmethod
    def prep_parsed(cls, parsed: dict) -> dict:
        # Fall back to environment variable
        if not parsed.get('api_key'):
            parsed['api_key'] = os.getenv('API_KEY')
        return parsed
```

## Tips for Quick Development

1. **Start Simple**: Begin with basic ArgFields and add complexity gradually
2. **Use Nested Configs**: Organize related settings into separate config classes
3. **Leverage Defaults**: Set sensible defaults for rapid prototyping
4. **Document Everything**: Use help strings for self-documenting CLIs
5. **Test Early**: Test argument parsing before implementing full logic

## Common Patterns

### Configuration Factory

```python
def create_training_config():
    """Factory function for common training configurations"""
    return TrainingConfig.parse_args()

def create_inference_config():
    """Factory function for inference configurations"""
    return InferenceConfig.parse_args()
```

### Configuration Inheritance

```python
@dataclass
class BaseConfig(DataClassConfig):
    verbose: bool = ArgField(False, ['-v'], help="Verbose output")
    log_level: str = ArgField('INFO', help="Log level")

@dataclass
class TrainingConfig(BaseConfig):
    epochs: int = ArgField(100, help="Training epochs")
    
@dataclass
class InferenceConfig(BaseConfig):
    model_path: str = ArgField(required=True, help="Model path")
```

This system provides a powerful, type-safe, and user-friendly way to handle complex application configurations through command-line interfaces.
