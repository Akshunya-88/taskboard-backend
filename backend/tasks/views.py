from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count
from django.db.models.functions import TruncWeek
import requests

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority', 'due_date']
    ordering = ['-created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    user = request.user

    # Status counts
    status_counts = Task.objects.filter(user=user).values('status').annotate(count=Count('id'))

    # Category counts
    category_counts = (
        Task.objects.filter(user=user, category__isnull=False)
        .values('category__name')
        .annotate(count=Count('id'))
    )

    # Priority counts
    priority_counts = Task.objects.filter(user=user).values('priority').annotate(count=Count('id'))

    # Weekly trend (tasks created)
    weekly_trend = (
        Task.objects.filter(user=user)
        .annotate(week=TruncWeek('created_at'))
        .values('week')
        .annotate(count=Count('id'))
        .order_by('week')
    )

    total_tasks = Task.objects.filter(user=user).count()

    return Response({
        "total_tasks": total_tasks,
        "status_counts": {item['status']: item['count'] for item in status_counts},
        "category_counts": {item['category__name']: item['count'] for item in category_counts},
        "priority_counts": {item['priority']: item['count'] for item in priority_counts},
        "weekly_trend": [{"week": i['week'], "count": i['count']} for i in weekly_trend]
    })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def advice_view(request):
    title = request.data.get('title', '')
    category = request.data.get('category', 'General')
    
    api_key = "AIzaSyAtZ8xXxr8_UNMp41pNhL6RfBKWTHhstk4"
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"Write exactly one short, professional description (max 2 sentences) for a task titled '{title}' in the category '{category}'. Do not provide multiple options. Focus on actionable steps."
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        if 'error' in data:
            error_msg = data['error'].get('message', 'Unknown API error')
            print(f"Gemini API Error: {error_msg}")
            return Response({"advice": f"AI Error: {error_msg}"})

        if 'candidates' in data and len(data['candidates']) > 0:
            advice = data['candidates'][0]['content']['parts'][0]['text']
            return Response({"advice": advice})
        else:
            print(f"Unexpected Gemini Response: {data}")
            return Response({"advice": "Could not generate suggestion. Unexpected response format."}, status=200)
            
    except Exception as e:
        print(f"Gemini Connection Error: {str(e)}")
        return Response({"error": "Failed to connect to AI service"}, status=500)
