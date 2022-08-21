from django.urls import path
from . import views

urlpatterns = [
    path('api/query/',views.QueryListCreate.as_view() ),
]

## Tried to get session based authentication / cookies to work.
##path('login/', views.LoginView.as_view())