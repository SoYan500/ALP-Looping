from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict


class LearningAlgorithm(str, Enum):
    """Enumeration of supported learning algorithms."""
    GRADIENT_DESCENT = "gradient_descent"
    ADAM = "adam"
    SGD = "stochastic_gradient_descent"
    REINFORCEMENT = "reinforcement"


class LoggingLevel(str, Enum):
    """Enumeration of logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class IterationConfig(BaseModel):
    """Configuration for iteration parameters."""
    max_iterations: int = Field(default=1000, gt=0, description="Maximum number of iterations")
    early_stopping_tolerance: float = Field(default=1e-4, ge=0, description="Early stopping threshold")
    gradient_clip_value: Optional[float] = Field(default=None, ge=0, description="Gradient clipping value")


class HyperparameterConfig(BaseModel):
    """Configuration for hyperparameters."""
    learning_rate: float = Field(default=0.01, gt=0, description="Learning rate for optimization")
    batch_size: int = Field(default=32, gt=0, description="Batch size for training")
    regularization_lambda: float = Field(default=0.01, ge=0, description="Regularization strength")


class ModelConfig(BaseModel):
    """Configuration for model architecture and settings."""
    hidden_layers: List[int] = Field(default=[64, 32], description="Sizes of hidden layers")
    activation_function: str = Field(default="relu", description="Activation function for hidden layers")
    dropout_rate: float = Field(default=0.2, ge=0, lt=1, description="Dropout rate for regularization")


class AdaptiveLearningProcessConfig(BaseModel):
    """Comprehensive configuration model for Adaptive Learning Process."""
    model_config = ConfigDict(
        title="Adaptive Learning Process Configuration",
        validate_default=True,
        extra="forbid"  # Prevents additional unexpected configuration keys
    )

    # Core learning configuration
    learning_algorithm: LearningAlgorithm = Field(
        default=LearningAlgorithm.ADAM,
        description="Primary learning algorithm for the process"
    )

    # Configuration sub-models
    iteration_config: IterationConfig = Field(
        default_factory=IterationConfig,
        description="Configuration for iteration control"
    )
    hyperparameters: HyperparameterConfig = Field(
        default_factory=HyperparameterConfig,
        description="Hyperparameter settings"
    )
    model_architecture: ModelConfig = Field(
        default_factory=ModelConfig,
        description="Model architecture configuration"
    )

    # Logging and monitoring
    logging_level: LoggingLevel = Field(
        default=LoggingLevel.INFO,
        description="Logging verbosity level"
    )
    performance_metrics: List[str] = Field(
        default=["accuracy", "loss"],
        description="List of performance metrics to track"
    )

    # Advanced configuration
    random_seed: Optional[int] = Field(
        default=None,
        description="Random seed for reproducibility"
    )
    custom_parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional custom parameters"
    )

    @field_validator('custom_parameters', mode='before')
    @classmethod
    def validate_custom_parameters(cls, v):
        """Validate custom parameters."""
        if v is not None and not isinstance(v, dict):
            raise ValueError("Custom parameters must be a dictionary")
        return v


def validate_alp_config(config: Union[dict, AdaptiveLearningProcessConfig]) -> AdaptiveLearningProcessConfig:
    """
    Validate and potentially convert a configuration to the AdaptiveLearningProcessConfig model.

    Args:
        config (Union[dict, AdaptiveLearningProcessConfig]): Configuration to validate

    Returns:
        AdaptiveLearningProcessConfig: Validated configuration
    """
    if isinstance(config, dict):
        return AdaptiveLearningProcessConfig(**config)
    elif isinstance(config, AdaptiveLearningProcessConfig):
        return config
    else:
        raise TypeError("Configuration must be a dictionary or AdaptiveLearningProcessConfig instance")