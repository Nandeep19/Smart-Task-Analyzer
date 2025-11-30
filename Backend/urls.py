from django.urls import path, include
urlpatterns = [
    path('api/tasks/', include('tasks.urls')),
    path('frontend/', include('tasks.frontend_urls')),
]
