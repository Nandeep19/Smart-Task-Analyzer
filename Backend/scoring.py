from datetime import datetime, timezone
from dateutil.parser import parse as parse_date

def parse_due_date(due_date_str):
    if not due_date_str:
        return None
    try:
        dt = parse_date(due_date_str)
        return dt
    except Exception:
        return None

def detect_cycles(tasks):
    graph = {t['id']: set(t.get('dependencies', [])) for t in tasks}
    visited = {}
    def dfs(node, stack):
        if node in visited: return False
        if node in stack: return True
        stack.add(node)
        for nei in graph.get(node, []):
            if dfs(nei, stack): return True
        stack.remove(node)
        visited[node] = True
        return False
    for n in graph:
        if dfs(n, set()): return True
    return False

def compute_scores(tasks, weights=None, today=None):
    if weights is None:
        weights = {'urgency':0.4, 'importance':0.3, 'effort':0.15, 'dependency':0.15}
    if today is None:
        today = datetime.now(timezone.utc)
    id_map = {t['id']: t for t in tasks}
    dependents_count = {t['id']: 0 for t in tasks}
    for t in tasks:
        for dep in t.get('dependencies', []):
            if dep in dependents_count:
                dependents_count[dep] += 1
    results = []
    for t in tasks:
        title = t.get('title','<untitled>')
        importance = float(t.get('importance', 5)) if t.get('importance') is not None else 5.0
        est = float(t.get('estimated_hours', 4)) if t.get('estimated_hours') is not None else 4.0
        due_date = parse_due_date(t.get('due_date'))
        if due_date:
            delta = (due_date - today).total_seconds() / 86400.0
            days = delta
            window = 30.0
            if days <= 0:
                urgency = 1.0 + min(30.0, -days) / 30.0
            else:
                urgency = max(0.0, (window - days) / window)
        else:
            urgency = 0.0
        importance_score = max(0.0, min(1.0, importance / 10.0))
        max_effort = 40.0
        effort_score = 1.0 - min(est, max_effort) / max_effort
        dep_score = min(1.0, dependents_count.get(t['id'], 0) / 5.0)
        score = (weights.get('urgency',0)*urgency +
                 weights.get('importance',0)*importance_score +
                 weights.get('effort',0)*effort_score +
                 weights.get('dependency',0)*dep_score)
        explanation = []
        explanation.append(f"urgency={urgency:.3f}")
        explanation.append(f"importance={importance_score:.3f}")
        explanation.append(f"effort={effort_score:.3f}")
        explanation.append(f"dependency={dep_score:.3f}")
        results.append({
            'id': t['id'],
            'title': title,
            'score': round(score,4),
            'explanation': '; '.join(explanation),
            'details': {
                'due_date': t.get('due_date'),
                'importance': importance,
                'estimated_hours': est,
                'dependencies': t.get('dependencies', [])
            }
        })
    results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)
    return results_sorted

def strategy_weights(strategy):
    strat = (strategy or '').lower()
    if strat == 'fastest':
        return {'urgency':0.2,'importance':0.1,'effort':0.6,'dependency':0.1}
    if strat == 'highimpact':
        return {'urgency':0.2,'importance':0.6,'effort':0.1,'dependency':0.1}
    if strat == 'deadline':
        return {'urgency':0.7,'importance':0.15,'effort':0.05,'dependency':0.1}
    return {'urgency':0.4,'importance':0.3,'effort':0.15,'dependency':0.15}
