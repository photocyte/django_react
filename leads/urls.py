from django.urls import path
from . import views

urlpatterns = [
    path('api/lead/', views.LeadListCreate.as_view() ),
    path('api/query/',views.QueryListCreate.as_view() ),
    path('login/', views.LoginView.as_view()),
]
