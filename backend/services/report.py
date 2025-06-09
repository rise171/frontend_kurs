from datetime import date
from typing import Optional, Dict
from pathlib import Path
import os
from sqlalchemy.ext.asyncio import AsyncSession
from services.mood import MoodService
from services.test import TestService
from services.thought import ThoughtService
from settings.config import REPORT_DIR
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ReportService:
    @staticmethod
    async def generate_mood_report(
            user_id: int,
            start_date: date,
            end_date: date,
            session: AsyncSession
    ) -> str:
        moods = await MoodService.get_moods(user_id, start_date, end_date, session)

        if not os.path.exists(REPORT_DIR):
            os.makedirs(REPORT_DIR)

        filename = f"mood_{user_id}_{start_date}_{end_date}.pdf"
        filepath = os.path.join(REPORT_DIR, filename)

        c = canvas.Canvas(filepath, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add report title
        c.drawString(100, 750, f"Mood Report ({start_date} to {end_date})")

        # Add mood data
        y_position = 700
        for mood in moods:
            c.drawString(100, y_position, f"{mood.date}: {mood.mood}")
            y_position -= 20
            if y_position < 50:
                c.showPage()
                y_position = 750

        c.save()
        return filepath

    @staticmethod
    async def generate_thoughts_pdf(
            user_id: int,
            start_date: str,
            end_date: str,
            session: AsyncSession
    ) -> str:
        thoughts = await ThoughtService.get_thoughts(user_id, start_date, end_date, session)

        if not os.path.exists(REPORT_DIR):
            os.makedirs(REPORT_DIR)

        filename = f"thoughts_{user_id}_{start_date}_{end_date}.pdf"
        filepath = os.path.join(REPORT_DIR, filename)

        c = canvas.Canvas(filepath, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add report title
        c.drawString(100, 750, f"Thought Diary Report ({start_date} to {end_date})")

        # Add thought data
        y_position = 700
        for thought in thoughts:
            c.drawString(100, y_position, f"Date: {thought.date}")
            y_position -= 20
            c.drawString(120, y_position, f"Situation: {thought.situation}")
            y_position -= 20
            c.drawString(120, y_position, f"Thought: {thought.thought}")
            y_position -= 20
            c.drawString(120, y_position, f"Emotion: {thought.emotion}")
            y_position -= 20
            c.drawString(120, y_position, f"Behavior: {thought.behavior}")
            y_position -= 40

            if y_position < 100:
                c.showPage()
                y_position = 750

        c.save()
        return filepath

    @staticmethod
    async def generate_test_report(
            user_id: int,
            test_id: int,
            session: AsyncSession
    ) -> Optional[str]:
        test_data = await TestService.get_test(test_id, session)
        if not test_data:
            return None

        if not os.path.exists(REPORT_DIR):
            os.makedirs(REPORT_DIR)

        filename = f"test_{user_id}_{test_id}.pdf"
        filepath = os.path.join(REPORT_DIR, filename)

        c = canvas.Canvas(filepath, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add report title
        c.drawString(100, 750, f"Test Report: {test_data.name}")

        # Add test details
        y_position = 700
        for question in test_data.questions:
            c.drawString(100, y_position, f"Question: {question.sentence}")
            y_position -= 40
            if y_position < 50:
                c.showPage()
                y_position = 750

        c.save()
        return filepath

    @staticmethod
    async def get_overall_statistics(user_id: int, session: AsyncSession) -> Dict:
        """Get overall statistics for a user including moods, thoughts, and tests."""
        # Получаем статистику по настроениям за последний месяц
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
        mood_stats = await MoodService.get_statistics(user_id, today.month, today.year, session)

        # Получаем количество записей мыслей
        thoughts = await ThoughtService.get_thoughts(user_id, None, None, session)
        thought_count = len(thoughts)

        # Получаем количество пройденных тестов
        completed_tests = await TestService.get_completed_tests_count(user_id, session)

        return {
            "mood_statistics": mood_stats,
            "total_thoughts": thought_count,
            "completed_tests": completed_tests
        }