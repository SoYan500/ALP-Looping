import pytest
from src.alp_config import (
    AdaptiveLearningProcessConfig,
    LearningAlgorithm,
    LoggingLevel,
    validate_alp_config
)


def test_default_configuration():
    """Test that the default configuration is created correctly."""
    config = AdaptiveLearningProcessConfig()
    
    assert config.learning_algorithm == LearningAlgorithm.ADAM
    assert config.logging_level == LoggingLevel.INFO
    assert config.performance_metrics == ["accuracy", "loss"]
    assert config.random_seed is None


def test_custom_configuration():
    """Test creating a configuration with custom parameters."""
    config_data = {
        "learning_algorithm": LearningAlgorithm.SGD,
        "logging_level": LoggingLevel.DEBUG,
        "performance_metrics": ["f1_score"],
        "random_seed": 42,
        "iteration_config": {
            "max_iterations": 500,
            "early_stopping_tolerance": 1e-3
        }
    }
    
    config = AdaptiveLearningProcessConfig(**config_data)
    
    assert config.learning_algorithm == LearningAlgorithm.SGD
    assert config.logging_level == LoggingLevel.DEBUG
    assert config.performance_metrics == ["f1_score"]
    assert config.random_seed == 42
    assert config.iteration_config.max_iterations == 500
    assert config.iteration_config.early_stopping_tolerance == 1e-3


def test_validation_helper():
    """Test the validate_alp_config helper function."""
    config_data = {
        "learning_algorithm": LearningAlgorithm.GRADIENT_DESCENT,
        "hyperparameters": {
            "learning_rate": 0.001,
            "batch_size": 64
        }
    }
    
    validated_config = validate_alp_config(config_data)
    
    assert isinstance(validated_config, AdaptiveLearningProcessConfig)
    assert validated_config.learning_algorithm == LearningAlgorithm.GRADIENT_DESCENT
    assert validated_config.hyperparameters.learning_rate == 0.001
    assert validated_config.hyperparameters.batch_size == 64


def test_invalid_configuration():
    """Test that invalid configurations raise appropriate errors."""
    with pytest.raises(Exception, match="Input should be greater than 0"):
        AdaptiveLearningProcessConfig(
            iteration_config={"max_iterations": 0}
        )
    
    with pytest.raises(Exception, match="Input should be greater than 0"):
        AdaptiveLearningProcessConfig(
            hyperparameters={"learning_rate": -0.1}
        )


def test_custom_parameters():
    """Test custom parameters configuration."""
    config = AdaptiveLearningProcessConfig(
        custom_parameters={"experimental_feature": True}
    )
    
    assert config.custom_parameters == {"experimental_feature": True}
    
    with pytest.raises(ValueError):
        AdaptiveLearningProcessConfig(
            custom_parameters="not a dictionary"
        )