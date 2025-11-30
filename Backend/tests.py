from django.test import TestCase
from .scoring import compute_scores, detect_cycles, strategy_weights
from datetime import datetime, timezone, timedelta

class ScoringTests(TestCase):
    def test_simple_scoring_ranks_overdue_high(self):
        today = datetime.now(timezone.utc)
        tasks = [
            {'id':'a','title':'overdue','due_date':(today - timedelta(days=5)).isoformat(), 'estimated_hours':2, 'importance':5, 'dependencies':[]},
            {'id':'b','title':'later','due_date':(today + timedelta(days=10)).isoformat(), 'estimated_hours':1, 'importance':5, 'dependencies':[]},
        ]
        res = compute_scores(tasks, today=today)
        self.assertGreater(res[0]['score'], res[1]['score'])
    def test_effort_prefers_quick_wins_when_strategy_fastest(self):
        today = datetime.now(timezone.utc)
        tasks = [
            {'id':'a','title':'big','due_date':(today + timedelta(days=5)).isoformat(), 'estimated_hours':20, 'importance':5, 'dependencies':[]},
            {'id':'b','title':'small','due_date':(today + timedelta(days=5)).isoformat(), 'estimated_hours':1, 'importance':5, 'dependencies':[]},
        ]
        weights = strategy_weights('fastest')
        res = compute_scores(tasks, weights=weights, today=today)
        self.assertGreater(res[0]['score'], res[1]['score'])
    def test_detect_cycles(self):
        tasks = [
            {'id':'1','dependencies':['2']},
            {'id':'2','dependencies':['1']},
        ]
        self.assertTrue(detect_cycles(tasks))
