from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from .scoring import calculate_scores

class AnalyzeTasksView(APIView):
    """
    POST /api/tasks/analyze/  - Accepts { "tasks": [ ... ] } and returns tasks with scores sorted
    """
    def post(self, request):
        tasks = request.data.get("tasks")
        if tasks is None:
            return Response({"error": "Missing 'tasks' list in body."}, status=status.HTTP_400_BAD_REQUEST)

        # Basic validation using serializer per-item
        valid_tasks = []
        errors = []
        for i, t in enumerate(tasks):
            ser = TaskSerializer(data=t)
            if ser.is_valid():
                valid_tasks.append(ser.validated_data)
            else:
                errors.append({"index": i, "errors": ser.errors})

        if errors:
            return Response({"error": "validation_failed", "details": errors}, status=status.HTTP_400_BAD_REQUEST)

        scored = calculate_scores(valid_tasks)
        if isinstance(scored, dict) and scored.get("error"):
            return Response(scored, status=status.HTTP_400_BAD_REQUEST)
        return Response({"tasks": scored})

class SuggestTasksView(APIView):
    """
    GET /api/tasks/suggest/ - Return top 3 tasks for today with short explanations
    Accepts optional query param strategy to choose behavior (fastest, highimpact, deadline, smart)
    """
    def get(self, request):
        # Accept tasks via query param (JSON string) OR (prefer) clients call analyze first.
        # For simplicity, expect a 'tasks' JSON in GET body is not standard; so accept sample via query param 'data' (JSON string)
        import json
        data = request.query_params.get("tasks") or request.query_params.get("data")
        if data:
            try:
                tasks = json.loads(data)
            except Exception:
                return Response({"error": "invalid_tasks_json"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # No tasks provided - return helpful message
            return Response({"error": "Provide tasks via query string param 'tasks' (JSON array). Example: ?tasks=[{...}]"}, status=400)

        scored = calculate_scores(tasks)
        if isinstance(scored, dict) and scored.get("error"):
            return Response(scored, status=status.HTTP_400_BAD_REQUEST)

        top3 = scored[:3]
        # Build short explanation for each
        suggestions = []
        for t in top3:
            # pick top reason from explanation lines (urgency/importance/dependency/effort with highest numeric)
            suggestions.append({
                "id": t["id"],
                "title": t["title"],
                "score": t["score"],
                "reason_summary": t["explanation"][0] + "; " + t["explanation"][1]
            })
        return Response({"suggestions": suggestions})
