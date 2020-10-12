from django.urls import path
from django.conf.urls import url
from .views import (FileCreationView,
                    download_file,
                    view_file_embedded,
                    get_catagories,
                    FileSingleCatagoryListView,
                    FileDualCatagoryListView,
                    FileTripleCatagoryListView,
                    FileSearchListView)

urlpatterns = [

    path('upload/', FileCreationView.as_view(), name="upload"),
    path('download/<int:file_id>/', download_file, name="download"),
    path('get_catagories/', get_catagories, name="get_catagories"),
    path('view_file_embedded/<int:file_id>/', view_file_embedded, name="view_file_embedded"),

    path('catagories/<str:catagory1>/', FileSingleCatagoryListView.as_view(), name="files_by_catagory_1"),
    path('catagories/<str:catagory1>/<str:catagory2>/', FileDualCatagoryListView.as_view(), name="files_by_catagory_2"),
    path('catagories/<str:catagory1>/<str:catagory2>/<str:catagory3>/', FileTripleCatagoryListView.as_view(), name="files_by_catagory_3"),

    path('search/<str:search_data>/', FileSearchListView.as_view(), name="search"),

]