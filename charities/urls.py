from django.urls import path

from . import views

urlpatterns = [
    path('benefactors/', views.BenefactorRegistration.as_view()),
]
