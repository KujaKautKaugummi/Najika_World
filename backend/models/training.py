"""
Training Models
Database models for AI training jobs and progress tracking
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class TrainingJob(Base):
    """AI Training job model"""

    __tablename__ = "training_jobs"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Ownership
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Job Info
    job_name = Column(String(200), nullable=False)
    training_type = Column(String(50), nullable=False)  # "lora", "session", "code", "voice", "personality"
    description = Column(Text, nullable=True)

    # Status
    status = Column(String(20), default="pending")  # pending, running, completed, failed, cancelled
    progress = Column(Float, default=0.0)  # 0.0 - 100.0

    # Configuration
    config = Column(JSON, default=dict)  # Training hyperparameters and settings

    # Results
    output_model_path = Column(String(500), nullable=True)
    metrics = Column(JSON, default=dict)  # Loss, accuracy, etc.
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Resource Usage
    estimated_duration_minutes = Column(Integer, nullable=True)
    actual_duration_minutes = Column(Integer, nullable=True)

    # Relationships
    user = relationship("User", back_populates="training_jobs")
    progress_logs = relationship("TrainingProgress", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TrainingJob(id={self.id}, name='{self.job_name}', type='{self.training_type}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_name": self.job_name,
            "training_type": self.training_type,
            "description": self.description,
            "status": self.status,
            "progress": self.progress,
            "config": self.config,
            "output_model_path": self.output_model_path,
            "metrics": self.metrics,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "actual_duration_minutes": self.actual_duration_minutes,
        }


class TrainingProgress(Base):
    """Training progress log entries"""

    __tablename__ = "training_progress"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Job Reference
    job_id = Column(Integer, ForeignKey("training_jobs.id"), nullable=False)

    # Progress Info
    epoch = Column(Integer, nullable=True)
    step = Column(Integer, nullable=True)
    loss = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    learning_rate = Column(Float, nullable=True)

    # Log Message
    message = Column(Text, nullable=True)
    log_level = Column(String(20), default="info")  # info, warning, error

    # Timestamp
    logged_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    job = relationship("TrainingJob", back_populates="progress_logs")

    def __repr__(self):
        return f"<TrainingProgress(job_id={self.job_id}, epoch={self.epoch}, loss={self.loss})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "job_id": self.job_id,
            "epoch": self.epoch,
            "step": self.step,
            "loss": self.loss,
            "accuracy": self.accuracy,
            "learning_rate": self.learning_rate,
            "message": self.message,
            "log_level": self.log_level,
            "logged_at": self.logged_at.isoformat() if self.logged_at else None,
        }
