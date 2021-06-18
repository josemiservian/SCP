from django.urls import path
from apps.help import views

from .views import HelpListView, HelpDetailView

urlpatterns = [
    path("help/<int:pk>", HelpDetailView.as_view(), name='help_detail'),
]
