from datetime import date, datetime
from collections import defaultdict, deque

# Configurable weights (you can expose these later as user preferences)
WEIGHTS = {
    "urgency": 0.35,
    "importance": 0.35,
    "effort": 0.15,       # quick wins
    "dependency": 0.15,
}

def parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None

def detect_cycle(tasks):
    # tasks: list of dicts with 'id' keys (strings)
    graph = defaultdict(list)
    nodes = set()
    for t in tasks:
        tid = str(t.get("id", t.get("title")))
        nodes.add(tid)
        for d in t.get("dependencies", []):
            graph[tid].append(str(d))
            nodes.add(str(d))
    visited = {}
    def dfs(node):
        if node in visited:
            return visited[node]  # True if currently in stack
        visited[node] = True  # in stack
        for nei in graph.get(node, []):
            if nei not in visited:
                if dfs(nei):
                    return True
            else:
                if visited[nei] is True:
                    return True
        visited[node] = False
        return False
    for n in nodes:
        if n not in visited:
            if dfs(n):
                return True
    return False

def calculate_scores(tasks, weights=None):
    """
    tasks: list of dicts (each task contains: id, title, due_date(YYYY-MM-DD), estimated_hours, importance, dependencies)
    returns: list of tasks with 'score' and 'explanation' added, sorted desc by score
    """
    if weights is None:
        weights = WEIGHTS

    # Validate tasks and normalize fields
    normalized = []
    for i, t in enumerate(tasks):
        tid = t.get("id", str(i))
        title = t.get("title", f"Task {i}")
        due = parse_date(t.get("due_date"))
        est = float(t.get("estimated_hours") or 1.0)
        imp = int(t.get("importance") or 5)
        deps = [str(x) for x in (t.get("dependencies") or [])]
        normalized.append({
            "id": str(tid),
            "title": title,
            "due_date": due,
            "estimated_hours": max(0.1, est),
            "importance": max(1, min(10, imp)),
            "dependencies": deps,
            "raw": t,
        })

    if detect_cycle(normalized):
        # Return error flag in response tasks if cycle detected.
        return {"error": "circular_dependency_detected"}

    today = date.today()
    # Precompute dependency counts: how many tasks this task blocks (inverse relationship)
    depends_on = {t["id"]: set(t["dependencies"]) for t in normalized}
    blocked_count = {t["id"]: 0 for t in normalized}
    for t in normalized:
        for dep in t["dependencies"]:
            if dep in blocked_count:
                blocked_count[dep] += 1

    results = []
    for t in normalized:
        # URGENCY score: 0..10 (overdue=10, far future close to 0)
        if t["due_date"] is None:
            urgency = 0.0
            urgency_reason = "no due date"
        else:
            days = (t["due_date"] - today).days
            if days < 0:
                urgency = 10.0
                urgency_reason = f"overdue by {-days} day(s)"
            else:
                urgency = max(0.0, 10.0 - days)  # each day reduces urgency
                urgency_reason = f"due in {days} day(s)"

        # IMPORTANCE: 1..10 map directly
        importance = float(t["importance"])
        importance_reason = f"importance {t['importance']}/10"

        # EFFORT quick-win: lower estimated_hours => higher score (scale to 0..10)
        quick_win = 10.0 / (1.0 + t["estimated_hours"])  # if est=0.5 -> ~6.66; if est=10 -> ~0.99
        effort_reason = f"estimated {t['estimated_hours']} hour(s)"

        # DEPENDENCY score: tasks blocking many tasks get higher priority (scale)
        dep_score = float(blocked_count.get(t["id"], 0))
        dep_reason = f"blocks {blocked_count.get(t['id'], 0)} task(s)"

        # Normalize components to 0..10 (urgency and importance already 0..10)
        # Quick win already roughly 0..10 (for est >=0.1 <-> ~9.09)
        # dep_score might be >10; we'll cap
        dep_score_capped = min(dep_score, 10.0)

        # Weighted sum
        score = (
            weights["urgency"] * urgency +
            weights["importance"] * importance +
            weights["effort"] * quick_win +
            weights["dependency"] * dep_score_capped
        )

        # Build explanation
        explanation = [
            f"urgency: {urgency:.2f} ({urgency_reason})",
            f"importance: {importance:.2f} ({importance_reason})",
            f"effort(quick-win): {quick_win:.2f} ({effort_reason})",
            f"dependency: {dep_score_capped:.2f} ({dep_reason})",
            f"weights: {weights}"
        ]

        results.append({
            "id": t["id"],
            "title": t["title"],
            "due_date": t["due_date"].isoformat() if t["due_date"] else None,
            "estimated_hours": t["estimated_hours"],
            "importance": t["importance"],
            "dependencies": t["dependencies"],
            "score": round(score, 4),
            "explanation": explanation,
        })

    # Sort descending by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
