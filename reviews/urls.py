from django.urls import path
from .views import AddCommentView, DeleteCommentView

app_name = 'reviews'

urlpatterns = [
    path('add/<int:product_id>/', AddCommentView.as_view(), name='add_comment'),
    path('delete/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
]