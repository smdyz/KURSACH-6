from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import res_password, ProfileView, RegisterView, verify_view, UsersView, UsersDetail, block_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/user_login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm/<token>/', verify_view, name='verify_success'),
    path('password/reset/', res_password, name='reset_password'),
    path('manage/users/', UsersView.as_view(), name='manager_users'),
    path('manage/users/view/<int:pk>', UsersDetail.as_view(), name='manager_users_detail'),
    path('manage/users/block/<int:pk>', block_user, name='manager_users_block'),
]