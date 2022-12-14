from django.urls import path,include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'projects'

urlpatterns = [
    path('',login_required(ProjectListView.as_view()), name='projects'),
    # path('add/',login_required(ProjectCreateView.as_view()),name='add_project'),
    path('add/',login_required(ProjectSimpleCreateView.as_view()),name='add_project'),
    path('pop/',ProjectPopView.as_view(),name='project_pop'),
    path('<int:pk>/',login_required(ProjectDetailView.as_view()),name='project_detail'),
    path('<int:pk>/return',login_required(MaterialReturnView.as_view()),name='project_return'),
    path('<int:pk>/update',login_required(ProjectSimpleUpdateView.as_view()),name='project_update'),
    path('<int:pk>/delete',login_required(ProjectDeleteView.as_view()),name='project_delete'),
    path('upload/',login_required(handle_upload_file),name='upload'),
    path('file/<int:pk>/delete',login_required(ProjectFileDeleteView.as_view()),name='file_delete'),
    path('kanban/',login_required(KanbanBoard.as_view()),name='kanbanboard'),
    path('status/',StatusView.as_view(),name='status'),
    path('status/<int:pk>',StatusDeleteView.as_view(),name='status_delete'),
    path('status/new/',StatusCreateView.as_view(),name='status_create'),
    path('<int:pk>/delivery',DeliveryChallanCreateView.as_view(),name='delivery_challan_create'),
]