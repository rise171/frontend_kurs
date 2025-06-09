from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import Dict
from services.report import ReportService
from api.auth import get_current_user
from models.user import User
from datetime import date
from settings.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/mood-pdf")
async def generate_mood_report(
    month: int,
    year: int,
    current_user: User = Depends(get_current_user),
    report_service: ReportService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Generate PDF report for mood tracking."""
    start_date = date(year, month, 1)
    end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
    pdf_path = await report_service.generate_mood_report(current_user.id, start_date, end_date, session)
    return FileResponse(pdf_path, filename=f"mood_report_{month}_{year}.pdf")

@router.get("/thoughts-pdf")
async def generate_thoughts_report(
    start_date: str,
    end_date: str,
    current_user: User = Depends(get_current_user),
    report_service: ReportService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Generate PDF report for thought diary."""
    pdf_path = await report_service.generate_thoughts_pdf(current_user.id, start_date, end_date, session)
    return FileResponse(pdf_path, filename=f"thoughts_report_{start_date}_{end_date}.pdf")

@router.get("/tests-pdf")
async def generate_tests_report(
    test_id: int = None,
    current_user: User = Depends(get_current_user),
    report_service: ReportService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Generate PDF report for psychological tests results."""
    pdf_path = await report_service.generate_test_report(current_user.id, test_id, session)
    return FileResponse(pdf_path, filename="tests_report.pdf")

@router.get("/statistics", response_model=Dict)
async def get_overall_statistics(
    current_user: User = Depends(get_current_user),
    report_service: ReportService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Get overall user statistics."""
    return await report_service.get_overall_statistics(current_user.id, session) 