"""Data fetching service for Lotofácil results from Caixa API."""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import httpx
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.models.lottery import LotteryResult

logger = logging.getLogger(__name__)


class LotofacilFetcher:
    """Service to fetch Lotofácil results from Caixa Econômica Federal API."""
    
    def __init__(self):
        self.base_url = settings.caixa_api_base_url
        self.timeout = 30.0
    
    async def fetch_latest_result(self) -> Optional[Dict]:
        """
        Fetch the most recent Lotofácil contest result.
        
        Returns:
            Dict with contest data or None if request fails
        """
        url = f"{self.base_url}/lotofacil"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Fetched latest result: Contest {data.get('numero')}")
                return data
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching latest result: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching latest result: {e}")
            return None
    
    async def fetch_contest(self, contest_number: int) -> Optional[Dict]:
        """
        Fetch a specific Lotofácil contest result.
        
        Args:
            contest_number: The contest number to fetch
            
        Returns:
            Dict with contest data or None if request fails
        """
        url = f"{self.base_url}/lotofacil/{contest_number}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Fetched contest {contest_number}")
                return data
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching contest {contest_number}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching contest {contest_number}: {e}")
            return None
    
    async def fetch_missing_contests(
        self, 
        from_contest: int, 
        to_contest: int
    ) -> List[Dict]:
        """
        Fetch multiple contests in a range.
        
        Args:
            from_contest: Starting contest number (inclusive)
            to_contest: Ending contest number (inclusive)
            
        Returns:
            List of contest data dictionaries
        """
        results = []
        
        for contest_num in range(from_contest, to_contest + 1):
            data = await self.fetch_contest(contest_num)
            if data:
                results.append(data)
            else:
                logger.warning(f"Failed to fetch contest {contest_num}")
        
        logger.info(f"Fetched {len(results)} contests from {from_contest} to {to_contest}")
        return results
    
    def save_result_to_db(self, result_data: Dict, db: Session) -> bool:
        """
        Parse API response and save to database.
        
        Args:
            result_data: Raw API response data
            db: Database session
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Parse the API response
            contest_number = result_data.get("numero")
            draw_date_str = result_data.get("dataApuracao")
            
            if not contest_number or not draw_date_str:
                logger.error("Missing required fields in API response")
                return False
            
            # Parse date (format: "DD/MM/YYYY")
            draw_date = datetime.strptime(draw_date_str, "%d/%m/%Y").date()
            
            # Extract numbers from listaDezenas
            numbers_str = result_data.get("listaDezenas", [])
            if not numbers_str:
                logger.error(f"No numbers found for contest {contest_number}")
                return False
            
            # Convert string numbers to integers
            numbers = [int(num) for num in numbers_str]
            
            # Check if result already exists
            existing = db.query(LotteryResult).filter(
                LotteryResult.contest_number == contest_number
            ).first()
            
            if existing:
                logger.info(f"Contest {contest_number} already exists in database")
                return True
            
            # Create new result
            lottery_result = LotteryResult(
                contest_number=contest_number,
                draw_date=draw_date,
                numbers=numbers
            )
            
            db.add(lottery_result)
            db.commit()
            db.refresh(lottery_result)
            
            logger.info(f"Saved contest {contest_number} to database")
            return True
            
        except IntegrityError as e:
            db.rollback()
            logger.warning(f"Contest already exists (integrity error): {e}")
            return True  # Not a failure, just already exists
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving result to database: {e}")
            return False
    
    async def update_database(self, db: Session) -> Dict[str, any]:
        """
        Check for new results and update database.
        
        Args:
            db: Database session
            
        Returns:
            Dict with update status and statistics
        """
        try:
            # Get latest result from API
            latest_api_result = await self.fetch_latest_result()
            if not latest_api_result:
                return {
                    "success": False,
                    "error": "Failed to fetch latest result from API"
                }
            
            latest_api_contest = latest_api_result.get("numero")
            
            # Get latest result from database
            latest_db_result = db.query(LotteryResult).order_by(
                LotteryResult.contest_number.desc()
            ).first()
            
            if not latest_db_result:
                # Database is empty, save the latest result
                success = self.save_result_to_db(latest_api_result, db)
                return {
                    "success": success,
                    "contests_added": 1 if success else 0,
                    "latest_contest": latest_api_contest,
                    "message": "Database was empty, added latest result"
                }
            
            latest_db_contest = latest_db_result.contest_number
            
            if latest_db_contest >= latest_api_contest:
                return {
                    "success": True,
                    "contests_added": 0,
                    "latest_contest": latest_db_contest,
                    "message": "Database is up to date"
                }
            
            # Fetch and save missing contests
            missing_contests = await self.fetch_missing_contests(
                latest_db_contest + 1,
                latest_api_contest
            )
            
            contests_added = 0
            for contest_data in missing_contests:
                if self.save_result_to_db(contest_data, db):
                    contests_added += 1
            
            return {
                "success": True,
                "contests_added": contests_added,
                "latest_contest": latest_api_contest,
                "message": f"Added {contests_added} new contests"
            }
            
        except Exception as e:
            logger.error(f"Error updating database: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
_fetcher_instance = None

def get_fetcher() -> LotofacilFetcher:
    """Get singleton instance of LotofacilFetcher."""
    global _fetcher_instance
    if _fetcher_instance is None:
        _fetcher_instance = LotofacilFetcher()
    return _fetcher_instance
