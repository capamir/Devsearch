from django.urls import path, include
from . import views

skill = [
    path('create/', views.CreateSkillView.as_view(), name='create-skill'),
    path('update/<str:pk>', views.UpdateSkillView.as_view(), name='update-skill'),
    path('delete/<str:pk>', views.CreateSkillView.as_view(), name='create-skill'),

]

message = [
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('create/', views.CreateMessageView.as_view(), name='create-message'),
    path('<str:pk>/', views.MessageView.as_view(), name='message-view'),
]

app_name = 'accounts'
urlpatterns = [
    path('', views.ProfilesView.as_view(), name='profiles'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('account/', views.UserProfileView.as_view(), name='account'),
    path('account-update/', views.UserProfileView.as_view(), name='account-update'),
    path('<str:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),

    path('skill/', include(skill)),
    path('message/', include(message)),

]
