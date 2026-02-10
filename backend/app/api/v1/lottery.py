"""
Lottery API endpoints.
"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.lottery import LotteryResult
from app.schemas.lottery import (
    LatestResultResponse,
    StatisticsResponse,
    GenerateSuggestionsRequest,
    GenerateSuggestionsResponse,
    HistoryResponse,
    LotteryResultResponse,
)
from app.services.statistics_service import LotteryStatisticsService
from app.services.strategy_service import LotteryStrategyGenerator
from app.services.rate_limit_service import RateLimitService

router = APIRouter(tags=["lottery"])


@router.get("/results/latest", response_model=LatestResultResponse)
async def get_latest_result(db: Session = Depends(get_db)):
    """
    Get the latest lottery result.
    
    Returns:
        Latest lottery result
    """
    result = db.query(LotteryResult).order_by(desc(LotteryResult.contest_number)).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="No results found")
    
    return LatestResultResponse(
        contest=result.contest_number,
        date=result.draw_date.isoformat(),
        numbers=result.numbers
    )


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get comprehensive lottery statistics.
    
    Returns:
        Statistical analysis of lottery data
    """
    stats_service = LotteryStatisticsService(db)
    statistics = stats_service.compute_statistics()
    
    if "error" in statistics:
        raise HTTPException(status_code=404, detail=statistics["error"])
    
    return StatisticsResponse(**statistics)


@router.post("/suggestions", response_model=GenerateSuggestionsResponse)
async def generate_suggestions(
    request: GenerateSuggestionsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate lottery number suggestions.
    
    Free users: 3 suggestions per day
    Premium users: Unlimited
    
    Args:
        request: Generation request with strategy and user_id
        
    Returns:
        Generated suggestions with metadata
    """
    # Check rate limit
    rate_limit_service = RateLimitService(db)
    can_generate, remaining = rate_limit_service.check_and_increment(request.user_id)
    
    if not can_generate:
        raise HTTPException(
            status_code=429,
            detail="Daily suggestion limit reached. Upgrade to Premium for unlimited suggestions."
        )
    
    # Get statistics and history
    stats_service = LotteryStatisticsService(db)
    statistics = stats_service.compute_statistics()
    
    # Check if statistics computation was successful
    if "error" in statistics:
        raise HTTPException(status_code=404, detail=statistics["error"])
    
    history = stats_service.get_history_dataframe()
    
    # Generate suggestions
    generator = LotteryStrategyGenerator(statistics, history)
    suggestions = generator.generate_suggestions(request.strategy, request.count)
    
    # Check if premium
    is_premium = rate_limit_service.is_premium(request.user_id)
    
    return GenerateSuggestionsResponse(
        suggestions=suggestions,
        remaining_today=remaining if not is_premium else None,
        is_premium=is_premium
    )


@router.get("/history", response_model=HistoryResponse)
async def get_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db)
):
    """
    Get paginated lottery history.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of results per page
        
    Returns:
        Paginated lottery results
    """
    # Get total count
    total = db.query(LotteryResult).count()
    
    # Calculate pagination
    offset = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size
    
    # Get results
    results = (
        db.query(LotteryResult)
        .order_by(desc(LotteryResult.contest_number))
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    return HistoryResponse(
        results=results,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/results/{contest_number}", response_model=LotteryResultResponse)
async def get_result_by_contest(
    contest_number: int,
    db: Session = Depends(get_db)
):
    """
    Get lottery result by contest number.
    
    Args:
        contest_number: Contest number to retrieve
        
    Returns:
        Lottery result for the specified contest
    """
    result = db.query(LotteryResult).filter(
        LotteryResult.contest_number == contest_number
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Contest {contest_number} not found")
    
    return result


# Admin endpoints
@router.post("/admin/update-results")
async def trigger_update(db: Session = Depends(get_db)):
    """
    Manually trigger data update from Caixa API.
    
    This endpoint allows administrators to manually fetch the latest
    lottery results from the Caixa API and update the database.
    
    Returns:
        Update status and statistics
    """
    from app.services.data.lotofacil_fetcher import get_fetcher
    
    fetcher = get_fetcher()
    result = await fetcher.update_database(db)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=f"Update failed: {result.get('error')}"
        )
    
    return {
        "success": True,
        "message": result.get("message"),
        "contests_added": result.get("contests_added"),
        "latest_contest": result.get("latest_contest"),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/admin/data-status")
async def get_data_status(db: Session = Depends(get_db)):
    """
    Check if database is up to date with Caixa API.
    
    Compares the latest contest in the database with the latest
    contest available from the Caixa API.
    
    Returns:
        Database status information
    """
    from app.services.data.lotofacil_fetcher import get_fetcher
    
    # Get latest from database
    latest_db = db.query(LotteryResult).order_by(
        desc(LotteryResult.contest_number)
    ).first()
    
    # Get latest from API
    fetcher = get_fetcher()
    latest_api_result = await fetcher.fetch_latest_result()
    
    if not latest_api_result:
        raise HTTPException(
            status_code=503,
            detail="Could not fetch data from Caixa API"
        )
    
    latest_api_contest = latest_api_result.get("numero")
    latest_db_contest = latest_db.contest_number if latest_db else 0
    
    is_up_to_date = latest_db_contest >= latest_api_contest
    missing_contests = max(0, latest_api_contest - latest_db_contest)
    
    return {
        "is_up_to_date": is_up_to_date,
        "latest_in_database": latest_db_contest,
        "latest_in_api": latest_api_contest,
        "missing_contests": missing_contests,
        "total_contests_in_db": db.query(LotteryResult).count(),
        "last_update_check": datetime.utcnow().isoformat()
    }

