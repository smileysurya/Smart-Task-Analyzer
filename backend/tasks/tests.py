from django.test import TestCase
from .scoring import calculate_scores, detect_cycle
from datetime import date, timedelta

class ScoringTests(TestCase):
    def test_urgency_overdue_high_score(self):
        today = date.today()
        tasks = [
            {"id": "1", "title": "Old task", "due_date": (today - timedelta(days=3)).isoformat(), "estimated_hours": 2, "importance": 5, "dependencies": []},
            {"id": "2", "title": "Future task", "due_date": (today + timedelta(days=10)).isoformat(), "estimated_hours": 1, "importance": 5, "dependencies": []},
        ]
        results = calculate_scores(tasks)
        # Overdue task should have higher score than future task
        self.assertTrue(results[0]["id"] == "1")

    def test_detect_cycle_true(self):
        tasks = [
            {"id": "A", "dependencies": ["B"]},
            {"id": "B", "dependencies": ["C"]},
            {"id": "C", "dependencies": ["A"]},
        ]
        self.assertTrue(detect_cycle(tasks))

    def test_sorting_by_score(self):
        today = date.today()
        tasks = [
            {"id": "t1", "title": "Quick high imp", "due_date": (today + timedelta(days=2)).isoformat(), "estimated_hours": 0.5, "importance": 9, "dependencies": []},
            {"id": "t2", "title": "Low imp long", "due_date": (today + timedelta(days=30)).isoformat(), "estimated_hours": 8, "importance": 3, "dependencies": []},
        ]
        results = calculate_scores(tasks)
        self.assertEqual(results[0]["id"], "t1")
