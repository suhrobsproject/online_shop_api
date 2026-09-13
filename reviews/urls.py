from django.urls import path
from .views import CommentListAPIView, CommentDetailAPIView

app_name = 'reviews'

urlpatterns = [
    path('', CommentListAPIView.as_view(), name='comment-list'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]