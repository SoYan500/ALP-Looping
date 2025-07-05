import os
import json
import pytest
import logging
from datetime import datetime
from src.alp.logging.termination_logger import (
    TerminationLogger, 
    TerminationReason, 
    TerminationEvent
)

@pytest.fixture
def temp_log_dir(tmp_path):
    """Provide a temporary directory for log files."""
    return str(tmp_path)

def test_termination_event_creation():
    """Test creating a TerminationEvent with valid data."""
    event = TerminationEvent(
        reason=TerminationReason.MAX_ITERATIONS,
        iteration_count=100,
        timestamp=datetime.now(),
        performance_metrics={"accuracy": 0.95, "loss": 0.05}
    )
    
    assert event.reason == TerminationReason.MAX_ITERATIONS
    assert event.iteration_count == 100
    assert "accuracy" in event.performance_metrics
    assert event.event_id is not None

def test_termination_logger_initialization(temp_log_dir):
    """Test initializing TerminationLogger."""
    logger = TerminationLogger(log_dir=temp_log_dir)
    
    assert os.path.exists(temp_log_dir)
    assert isinstance(logger, TerminationLogger)

def test_termination_logger_log_event(temp_log_dir, caplog):
    """Test logging a termination event."""
    caplog.set_level(logging.INFO)
    
    logger = TerminationLogger(log_dir=temp_log_dir, log_to_console=True)
    logger.log_termination(
        reason=TerminationReason.PERFORMANCE_THRESHOLD,
        iteration_count=250,
        performance_metrics={"f1_score": 0.88}
    )
    
    # Check console log
    assert "ALP Loop Terminated" in caplog.text
    assert "PERFORMANCE_THRESHOLD" in caplog.text
    
    # Check JSON log generation
    json_logs = [f for f in os.listdir(temp_log_dir) if f.endswith('.json')]
    assert len(json_logs) == 1
    
    with open(os.path.join(temp_log_dir, json_logs[0]), 'r') as f:
        log_data = json.load(f)
        
    assert log_data['reason'] == 'PERFORMANCE_THRESHOLD'
    assert log_data['iteration_count'] == 250
    assert log_data['performance_metrics']['f1_score'] == 0.88
    assert 'event_id' in log_data

def test_multiple_log_events(temp_log_dir):
    """Test logging multiple termination events."""
    logger = TerminationLogger(log_dir=temp_log_dir)
    
    log_paths = []
    for i in range(3):
        log_path = logger.log_termination(
            reason=TerminationReason.MAX_ITERATIONS,
            iteration_count=i * 50,
            performance_metrics={"test_metric": i * 0.1}
        )
        log_paths.append(log_path)
    
    json_logs = [f for f in os.listdir(temp_log_dir) if f.endswith('.json')]
    assert len(json_logs) == 3
    assert len(set(log_paths)) == 3  # Ensure unique log paths

def test_event_serialization():
    """Test TerminationEvent dictionary serialization."""
    event = TerminationEvent(
        reason=TerminationReason.ERROR,
        iteration_count=75,
        timestamp=datetime.now(),
        performance_metrics={"error_rate": 0.02},
        additional_context={"error_details": "Overflow"}
    )
    
    event_dict = event.to_dict()
    
    assert "event_id" in event_dict
    assert "reason" in event_dict
    assert "iteration_count" in event_dict
    assert "timestamp" in event_dict
    assert "performance_metrics" in event_dict
    assert "additional_context" in event_dict
    assert event_dict["reason"] == "ERROR"
    assert event_dict["event_id"] is not None