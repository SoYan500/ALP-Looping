from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, Optional
import json
import logging
import os
import uuid

class TerminationReason(Enum):
    MAX_ITERATIONS = auto()
    PERFORMANCE_THRESHOLD = auto()
    MANUAL_STOP = auto()
    ERROR = auto()
    UNKNOWN = auto()

@dataclass
class TerminationEvent:
    """
    Represents a complete logging event for ALP loop termination.
    
    Captures comprehensive details about loop termination, including
    reason, performance metrics, and contextual information.
    """
    reason: TerminationReason
    iteration_count: int
    timestamp: datetime
    performance_metrics: Dict[str, Any]
    additional_context: Optional[Dict[str, Any]] = None
    event_id: str = None

    def __post_init__(self):
        """Generate a unique event ID if not provided."""
        if self.event_id is None:
            self.event_id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert termination event to a dictionary for serialization.
        
        Returns:
            Dict containing event details
        """
        return {
            "event_id": self.event_id,
            "reason": self.reason.name,
            "iteration_count": self.iteration_count,
            "timestamp": self.timestamp.isoformat(),
            "performance_metrics": self.performance_metrics,
            "additional_context": self.additional_context or {}
        }

class TerminationLogger:
    """
    Manages logging of ALP loop termination events with multiple output strategies.
    
    Supports logging to:
    - Console
    - File
    - JSON log
    """
    def __init__(
        self, 
        log_dir: str = "logs", 
        log_to_console: bool = True, 
        log_to_file: bool = True
    ):
        """
        Initialize TerminationLogger with configurable logging strategies.
        
        Args:
            log_dir: Directory to store log files
            log_to_console: Enable console logging
            log_to_file: Enable file logging
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure loggers
        self.logger = logging.getLogger("termination_logger")
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(console_handler)
        
        # File handler
        if log_to_file:
            log_file = os.path.join(log_dir, f"termination_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            self.logger.addHandler(file_handler)
    
    def log_termination(
        self, 
        reason: TerminationReason, 
        iteration_count: int, 
        performance_metrics: Dict[str, Any], 
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log a complete termination event.
        
        Args:
            reason: Reason for loop termination
            iteration_count: Number of iterations completed
            performance_metrics: Metrics captured during loop execution
            additional_context: Optional extra contextual information
        
        Returns:
            str: Path to the generated JSON log file
        """
        event = TerminationEvent(
            reason=reason,
            iteration_count=iteration_count,
            timestamp=datetime.now(),
            performance_metrics=performance_metrics,
            additional_context=additional_context
        )
        
        # Generate unique JSON log filename
        json_filename = f"termination_{event.event_id}.json"
        json_log_path = os.path.join(self.log_dir, json_filename)
        
        # Write JSON log
        with open(json_log_path, 'w') as f:
            json.dump(event.to_dict(), f, indent=2)
        
        # Log to configured outputs
        log_message = (
            f"ALP Loop Terminated: "
            f"Reason={reason.name}, "
            f"Iterations={iteration_count}, "
            f"Metrics={performance_metrics}"
        )
        self.logger.info(log_message)
        
        return json_log_path