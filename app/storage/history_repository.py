"""
Lottery History Repository - Handles reading and writing historical lottery data.

This module provides the LotteryHistoryRepository class for managing
the historical lottery dataset stored in Excel format.
"""

from datetime import date
from pathlib import Path
from typing import Dict

import pandas as pd

from app.config import LOTTERY_HISTORY_FILE


class LotteryHistoryRepository:
    """
    Repository for managing historical lottery data.
    
    This class handles:
    - Loading the historical dataset from Excel
    - Checking if a contest already exists
    - Appending new results without duplication
    """

    def __init__(self, file_path: Path = LOTTERY_HISTORY_FILE):
        """
        Initialize the repository.
        
        Args:
            file_path: Path to the Excel file containing lottery history.
                      Defaults to the configured LOTTERY_HISTORY_FILE.
        """
        self.file_path = file_path

    def load_history(self) -> pd.DataFrame:
        """
        Load the historical lottery data from Excel.
        
        Returns:
            pd.DataFrame: DataFrame containing the historical lottery data.
                         Expected columns: concurso, data, and number columns.
        
        Raises:
            FileNotFoundError: If the history file does not exist.
            ValueError: If the file is empty or has an invalid format.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Lottery history file not found: {self.file_path}\n"
                f"Please ensure the file exists in the data/raw/ directory."
            )

        try:
            df = pd.read_excel(self.file_path)
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}")

        if df.empty:
            raise ValueError("The lottery history file is empty.")

        # Validate that we have at least the basic columns
        if "concurso" not in df.columns:
            raise ValueError(
                "Invalid file format: 'concurso' column not found. "
                "Expected columns: concurso, data, and number columns."
            )

        return df

    def has_concurso(self, concurso: int) -> bool:
        """
        Check if a specific contest number already exists in the history.
        
        Args:
            concurso: The contest number to check.
        
        Returns:
            bool: True if the contest exists, False otherwise.
        """
        df = self.load_history()
        return concurso in df["concurso"].values

    def append_result(self, result: Dict[str, any]) -> None:
        """
        Append a new lottery result to the history file.
        
        This method safely appends a new result without creating duplicates.
        If the contest already exists, it will not be added again.
        
        Args:
            result: Dictionary containing:
                - concurso (int): Contest number
                - data (date): Draw date
                - numeros (list[int]): Drawn numbers
        
        Raises:
            ValueError: If the result is invalid or the contest already exists.
        """
        # Validate input
        if not isinstance(result, dict):
            raise ValueError("Result must be a dictionary.")

        required_keys = {"concurso", "data", "numeros"}
        if not required_keys.issubset(result.keys()):
            raise ValueError(f"Result must contain keys: {required_keys}")

        concurso = result["concurso"]

        # Check for duplicates
        if self.has_concurso(concurso):
            raise ValueError(
                f"Contest {concurso} already exists in the history. "
                "Duplicate entries are not allowed."
            )

        # Load existing data
        df = self.load_history()

        # Create new row (this is a simplified version - actual implementation
        # would need to match the exact column structure of the Excel file)
        new_row = {
            "concurso": concurso,
            "data": result["data"],
        }

        # Add number columns (assuming they're named like bola_1, bola_2, etc.)
        for i, num in enumerate(result["numeros"], start=1):
            new_row[f"bola_{i}"] = num

        # Append and save
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(self.file_path, index=False)
