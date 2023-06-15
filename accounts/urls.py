from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

password = [
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password/reset_password.html"),
         name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password/reset_password_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password/reset.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password/reset_password_complete.html"),
         name="password_reset_complete"),
]

skill = [
    path('create/', views.CreateSkillView.as_view(), name='create-skill'),
    path('update/<str:pk>/', views.UpdateSkillView.as_view(), name='update-skill'),
    path('delete/<str:pk>/', views.CreateSkillView.as_view(), name='delete-skill'),

]

message = [
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('<str:pk>/', views.MessageView.as_view(), name='message'),
    path('create-message/<str:pk>/', views.CreateMessageView.as_view(),
         name='send-message'),
]

urlpatterns = [
    path('', views.ProfilesView.as_view(), name='profiles'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('account/', views.UserProfileView.as_view(), name='account'),
    path('account-update/', views.UserProfileView.as_view(), name='edit-account'),
    path('<str:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),

    path('skill/', include(skill)),
    path('message/', include(message)),
    path('password/', include(password)),

]
