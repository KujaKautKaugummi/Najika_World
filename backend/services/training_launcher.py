"""
Training Launcher Service
Unified interface for all training types, wrapping existing training scripts
"""

import os
import sys
import subprocess
import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from sqlalchemy.orm import Session

from backend.models.training import TrainingJob, TrainingProgress
from backend.config import settings, get_training_data_path, get_model_output_path


class TrainingLauncher:
    """Unified training launcher for all training types"""

    def __init__(self):
        self.backend_dir = Path(__file__).parent.parent
        self.project_root = self.backend_dir.parent

        # Training script paths
        self.scripts = {
            "lora": self.backend_dir / "najika_lora_training.py",
            "session": self.backend_dir / "NAJIKA_SESSION_TRAINING.py",
            "code": self.backend_dir / "NAJIKA_CODE_TRAINING.py",
            "voice": self.backend_dir / "NAJIKA_VIDEO_TO_VOICE_TRAINING.py",
            "personality": self.backend_dir / "najika_emotional_intelligence_training.py",
        }

    def launch_training(
        self,
        job_id: int,
        training_type: str,
        config: Dict[str, Any],
        db: Session,
        on_progress: Optional[Callable] = None
    ) -> bool:
        """
        Launch training job in background thread

        Args:
            job_id: Training job ID from database
            training_type: Type of training (lora, session, code, voice, personality)
            config: Training configuration dict
            db: Database session
            on_progress: Optional callback for progress updates

        Returns:
            True if launched successfully, False otherwise
        """

        # Get job from database
        job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
        if not job:
            print(f"❌ Training job {job_id} not found")
            return False

        # Check if script exists
        script_path = self.scripts.get(training_type)
        if not script_path or not script_path.exists():
            error_msg = f"Training script not found for type: {training_type}"
            job.status = "failed"
            job.error_message = error_msg
            db.commit()
            print(f"❌ {error_msg}")
            return False

        # Start training in background thread
        thread = threading.Thread(
            target=self._run_training_thread,
            args=(job_id, training_type, config, script_path),
            daemon=True
        )
        thread.start()

        print(f"✅ Training job {job_id} ({training_type}) launched in background")
        return True

    def _run_training_thread(
        self,
        job_id: int,
        training_type: str,
        config: Dict[str, Any],
        script_path: Path
    ):
        """Background thread that runs the training script"""

        # Import here to avoid circular imports
        from backend.database import SessionLocal

        db = SessionLocal()

        try:
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if not job:
                return

            # Update job status
            job.status = "running"
            job.started_at = datetime.utcnow()
            db.commit()

            # Log start
            self._add_progress_log(
                db, job_id,
                message=f"Started {training_type} training",
                log_level="info"
            )

            # Route to appropriate training function
            if training_type == "lora":
                success = self._run_lora_training(db, job_id, config, script_path)
            elif training_type == "session":
                success = self._run_session_training(db, job_id, config, script_path)
            elif training_type == "code":
                success = self._run_code_training(db, job_id, config, script_path)
            elif training_type == "voice":
                success = self._run_voice_training(db, job_id, config, script_path)
            elif training_type == "personality":
                success = self._run_personality_training(db, job_id, config, script_path)
            else:
                success = False
                job.error_message = f"Unknown training type: {training_type}"

            # Update final status
            job.status = "completed" if success else "failed"
            job.completed_at = datetime.utcnow()
            job.progress = 100.0 if success else job.progress

            db.commit()

            # Log completion
            self._add_progress_log(
                db, job_id,
                message=f"Training {'completed' if success else 'failed'}",
                log_level="info" if success else "error"
            )

        except Exception as e:
            # Handle errors
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if job:
                job.status = "failed"
                job.error_message = str(e)
                job.completed_at = datetime.utcnow()
                db.commit()

            self._add_progress_log(
                db, job_id,
                message=f"Training failed: {e}",
                log_level="error"
            )

            print(f"❌ Training job {job_id} failed: {e}")

        finally:
            db.close()

    def _run_lora_training(
        self,
        db: Session,
        job_id: int,
        config: Dict[str, Any],
        script_path: Path
    ) -> bool:
        """Run LoRA training"""

        try:
            # Import the LoRA trainer
            sys.path.insert(0, str(self.backend_dir))
            from najika_lora_training import NajikaLoRATrainer

            # Create trainer instance
            trainer = NajikaLoRATrainer(
                base_model=config.get("base_model", "unsloth/Meta-Llama-3.1-8B-Instruct"),
                output_dir=get_model_output_path(f"lora_job_{job_id}"),
                logs_dir=get_model_output_path(f"logs_job_{job_id}")
            )

            # Update progress
            self._update_progress(db, job_id, 10.0, message="Preparing training data...")

            # Prepare data
            train_dataset = trainer.prepare_training_data(
                min_samples=config.get("min_samples", 10)
            )

            if train_dataset is None:
                raise Exception("Failed to prepare training data")

            self._update_progress(db, job_id, 30.0, message="Training data prepared")

            # Train
            self._update_progress(db, job_id, 40.0, message="Starting LoRA training...")

            trainer.train(
                train_dataset=train_dataset,
                num_epochs=config.get("num_epochs", 3),
                learning_rate=config.get("learning_rate", 2e-4),
                batch_size=config.get("batch_size", 4)
            )

            self._update_progress(db, job_id, 80.0, message="Training completed, saving model...")

            # Save model
            output_path = trainer.save_model()

            # Update job with output path
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            job.output_model_path = str(output_path)
            db.commit()

            self._update_progress(db, job_id, 100.0, message="LoRA training complete!")

            return True

        except Exception as e:
            print(f"❌ LoRA training error: {e}")
            self._add_progress_log(db, job_id, message=str(e), log_level="error")
            return False

    def _run_session_training(
        self,
        db: Session,
        job_id: int,
        config: Dict[str, Any],
        script_path: Path
    ) -> bool:
        """Run session training (import Claude Code sessions)"""

        try:
            # Run as subprocess (simpler for existing scripts)
            self._update_progress(db, job_id, 10.0, message="Starting session import...")

            cmd = [sys.executable, str(script_path)]

            # Add config args if needed
            if "session_path" in config:
                cmd.extend(["--session-path", config["session_path"]])

            # Run subprocess
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=3600  # 1 hour timeout
            )

            if result.returncode == 0:
                self._update_progress(db, job_id, 100.0, message="Session training complete!")
                return True
            else:
                error_msg = result.stderr or "Unknown error"
                self._add_progress_log(db, job_id, message=error_msg, log_level="error")
                return False

        except subprocess.TimeoutExpired:
            self._add_progress_log(db, job_id, message="Training timeout", log_level="error")
            return False
        except Exception as e:
            print(f"❌ Session training error: {e}")
            self._add_progress_log(db, job_id, message=str(e), log_level="error")
            return False

    def _run_code_training(
        self,
        db: Session,
        job_id: int,
        config: Dict[str, Any],
        script_path: Path
    ) -> bool:
        """Run code training (learn from project code)"""

        try:
            self._update_progress(db, job_id, 10.0, message="Analyzing code...")

            # Run as subprocess
            cmd = [sys.executable, str(script_path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=1800  # 30 minutes
            )

            if result.returncode == 0:
                self._update_progress(db, job_id, 100.0, message="Code training complete!")
                return True
            else:
                error_msg = result.stderr or "Unknown error"
                self._add_progress_log(db, job_id, message=error_msg, log_level="error")
                return False

        except Exception as e:
            print(f"❌ Code training error: {e}")
            self._add_progress_log(db, job_id, message=str(e), log_level="error")
            return False

    def _run_voice_training(
        self,
        db: Session,
        job_id: int,
        config: Dict[str, Any],
        script_path: Path
    ) -> bool:
        """Run voice training (video to voice training data)"""

        try:
            self._update_progress(db, job_id, 10.0, message="Processing voice data...")

            cmd = [sys.executable, str(script_path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=3600  # 1 hour
            )

            if result.returncode == 0:
                self._update_progress(db, job_id, 100.0, message="Voice training complete!")
                return True
            else:
                error_msg = result.stderr or "Unknown error"
                self._add_progress_log(db, job_id, message=error_msg, log_level="error")
                return False

        except Exception as e:
            print(f"❌ Voice training error: {e}")
            self._add_progress_log(db, job_id, message=str(e), log_level="error")
            return False

    def _run_personality_training(
        self,
        db: Session,
        job_id: int,
        config: Dict[str, Any],
        script_path: Path
    ) -> bool:
        """Run personality training (emotional intelligence)"""

        try:
            self._update_progress(db, job_id, 10.0, message="Training personality...")

            cmd = [sys.executable, str(script_path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=1800
            )

            if result.returncode == 0:
                self._update_progress(db, job_id, 100.0, message="Personality training complete!")
                return True
            else:
                error_msg = result.stderr or "Unknown error"
                self._add_progress_log(db, job_id, message=error_msg, log_level="error")
                return False

        except Exception as e:
            print(f"❌ Personality training error: {e}")
            self._add_progress_log(db, job_id, message=str(e), log_level="error")
            return False

    def _update_progress(
        self,
        db: Session,
        job_id: int,
        progress: float,
        message: str = ""
    ):
        """Update job progress"""

        job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
        if job:
            job.progress = progress
            db.commit()

        if message:
            self._add_progress_log(db, job_id, message=message)

    def _add_progress_log(
        self,
        db: Session,
        job_id: int,
        message: str,
        log_level: str = "info",
        epoch: Optional[int] = None,
        step: Optional[int] = None,
        loss: Optional[float] = None
    ):
        """Add progress log entry"""

        log_entry = TrainingProgress(
            job_id=job_id,
            message=message,
            log_level=log_level,
            epoch=epoch,
            step=step,
            loss=loss
        )

        db.add(log_entry)
        db.commit()

        print(f"[Job {job_id}] {message}")


# Global instance
training_launcher = TrainingLauncher()
