from django.urls import path,include
from .views import *
from django.contrib.auth.decorators import login_required
app_name = 'projects'



urlpatterns = [
    path('',login_required(ProjectListView.as_view()), name='projects'),
    path('add/',login_required(ProjectCreateView.as_view()),name='add_project'),
    path('pop/',ProjectPopView.as_view(),name='project_pop'),
    path('<int:pk>/',login_required(ProjectDetailView.as_view()),name='project_detail'),
    path('<int:pk>/update',login_required(ProjectUpdateView.as_view()),name='project_update'),
    path('<int:pk>/delete',login_required(ProjectDeleteView.as_view()),name='project_delete'),
    path('upload/',login_required(handle_upload_file),name='upload'),
    path('file/<int:pk>/delete',login_required(ProjectFileDeleteView.as_view()),name='file_delete'),
    path('kanban/',login_required(kanbanboard),name='kanbanboard'),
    path('status/',StatusView.as_view(),name='status'),
    path('status/<int:pk>',StatusDeleteView.as_view(),name='status_delete'),
    path('status/new/',StatusCreateView.as_view(),name='status_create'),
]