"""
Pipelines module - Application-level orchestration.

This module contains pipeline functions that orchestrate the various
components of the lottery analysis system.
"""

from app.pipelines.update_and_analyze import run_pipeline

__all__ = ["run_pipeline"]
