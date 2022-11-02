from django.urls import path
from jobs import views

urlpatterns = [
    path('joblist',views.JobsListView.as_view(),name='joblist'),
    path('jobgrid',views.JobsGridView.as_view(),name='jobgrid'),
    path('jobs-apply',views.JobsApplyView.as_view(),name='jobs-apply'),
    path('jobs-details',views.JobsDetailsView.as_view(),name='jobs-details'),
    path('jobs-categories',views.JobsCategoriesView.as_view(),name='jobs-categories'),

    path('candidate-list',views.CandidateListView.as_view(),name='candidate-list'),
    path('candidate-overview',views.CandidateOverviewView.as_view(),name='candidate-overview'),

]