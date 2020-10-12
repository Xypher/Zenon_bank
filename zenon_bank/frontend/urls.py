from django.urls import path
from files.views import FileListView

urlpatterns = [
    path('', FileListView.as_view(), name="home")
]
