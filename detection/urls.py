# App URLs (detection/urls.py)
from django.urls import path
from . import views
from .test_view import test_view

urlpatterns = [
    path('', views.home, name='home'),
    path('process/<int:test_id>/', views.process_test, name='process_test'),
    path('records/', views.records, name='records'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('test/<int:test_id>/cancel/', views.cancel_test, name='cancel_test'),
    path('test/', test_view, name='test'),
]