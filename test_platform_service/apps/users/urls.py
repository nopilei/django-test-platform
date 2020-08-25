from django.urls import path
from .views import *


urlpatterns = [
    path('login', TestLoginView.as_view(), name='login'),
    path('logout', TestLogoutView.as_view(), name='logout'),
    path('register', register, name='register'),
    path('activate/<str:uid>/<str:token>', activate, name='activate'),
    path('password_reset', TestPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>', TestPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('profile_configuration/', profile_configuration, name='profile_configuration'),
]