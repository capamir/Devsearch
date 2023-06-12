from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.ProfilesView.as_view(), name='profiles'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('<str:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
]
