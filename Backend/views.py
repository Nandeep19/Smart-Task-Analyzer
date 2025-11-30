import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .scoring import compute_scores, detect_cycles, strategy_weights
from datetime import datetime, timezone

@csrf_exempt
def analyze_tasks(request):
    if request.method != 'POST':
        return HttpResponseBadRequest(json.dumps({'error':'Use POST with JSON payload'}), content_type='application/json')
    try:
        payload = json.loads(request.body)
    except Exception:
        return HttpResponseBadRequest(json.dumps({'error':'Invalid JSON'}), content_type='application/json')
    tasks = payload if isinstance(payload, list) else payload.get('tasks', [])
    for i,t in enumerate(tasks):
        if 'id' not in t:
            return HttpResponseBadRequest(json.dumps({'error':f'Task at index {i} missing id field'}), content_type='application/json')
    if detect_cycles(tasks):
        return JsonResponse({'error':'Circular dependency detected'}, status=400)
    strategy = None
    if isinstance(payload, dict):
        strategy = payload.get('strategy')
    weights = strategy_weights(strategy)
    results = compute_scores(tasks, weights=weights, today=datetime.now(timezone.utc))
    return JsonResponse({'results': results})

def suggest_tasks(request):
    data = request.GET.get('data')
    if data:
        try:
            tasks = json.loads(data)
        except Exception:
            return HttpResponseBadRequest(json.dumps({'error':'Invalid JSON in data parameter'}), content_type='application/json')
    else:
        tasks = [
            {'id':'t1','title':'Fix login bug','due_date':None,'estimated_hours':3,'importance':8,'dependencies':[]},
            {'id':'t2','title':'Update docs','due_date':None,'estimated_hours':1,'importance':4,'dependencies':[]},
            {'id':'t3','title':'Release v1.2','due_date':None,'estimated_hours':8,'importance':9,'dependencies':['t1']},
        ]
    if detect_cycles(tasks):
        return JsonResponse({'error':'Circular dependency detected'}, status=400)
    weights = strategy_weights(request.GET.get('strategy'))
    results = compute_scores(tasks, weights=weights)
    top3 = results[:3]
    suggestions = []
    for r in top3:
        suggestions.append({
            'id': r['id'],
            'title': r['title'],
            'score': r['score'],
            'why': f"Score components: {r['explanation']}"
        })
    return JsonResponse({'suggestions': suggestions})
