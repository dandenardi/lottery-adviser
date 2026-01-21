"""
Lottery History Repository - Handles reading and writing historical lottery data.

This module provides the LotteryHistoryRepository class for managing
the historical lottery dataset stored in Excel format.
"""

from datetime import date
from pathlib import Path
from typing import Dict

import pandas as pd

from app.core.config import settings


class LotteryHistoryRepository:
    """
    Repository for managing historical lottery data.
    
    This class handles:
    - Loading the historical dataset from Excel
    - Checking if a contest already exists
    - Appending new results without duplication
    """

    def __init__(self, file_path: Path = None):
        """
        Initialize the repository.
        
        Args:
            file_path: Path to the Excel file containing lottery history.
                      Defaults to the configured lottery_history_file from settings.
        """
        self.file_path = file_path or settings.lottery_history_file

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
            # Try loading with skiprows=6 first (Lotofácil format from asloterias.com.br - header on line 7)
            # Then fallback to skiprows=0 for standard format
            df = None
            
            for skip in [6, 0]:
                try:
                    temp_df = pd.read_excel(self.file_path, skiprows=skip)
                    # Normalize column names
                    temp_df.columns = [str(col).strip().lower() for col in temp_df.columns]
                    
                    # Check if any column contains 'concurso'
                    if any('concurso' in col for col in temp_df.columns):
                        df = temp_df
                        break
                except Exception as e:
                    continue
            
            if df is None:
                raise ValueError("Could not find valid lottery data format in file")
                
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}")

        if df.empty:
            raise ValueError("The lottery history file is empty.")

        # Validate that we have at least the basic columns
        # Check if any column name contains 'concurso'
        has_concurso = any('concurso' in str(col).lower() for col in df.columns)
        
        if not has_concurso:
            raise ValueError(
                "Invalid file format: 'concurso' column not found. "
                f"Found columns: {df.columns.tolist()}\n"
                "Expected columns: concurso, data, and number columns."
            )
        
        # Rename first column to 'concurso' if it contains 'concurso'
        for i, col in enumerate(df.columns):
            if 'concurso' in str(col).lower():
                df.columns.values[i] = 'concurso'
                break

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
