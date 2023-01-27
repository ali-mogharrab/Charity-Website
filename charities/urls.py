from django.urls import path

from . import views

urlpatterns = [
    path('benefactors/', views.BenefactorRegistration.as_view()),
    path('charities/', views.CharityRegistration.as_view()),
    path('tasks/', views.Tasks.as_view()),
    path('tasks/<int:task_id>/request/', views.TaskRequest.as_view()),
]
