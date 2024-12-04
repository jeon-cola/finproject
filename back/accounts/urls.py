from django.urls import path
from .views import SignUpView, ProfileView, LoginView, LogoutView, DeleteAccountView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),  # 회원탈퇴 경로 추가
]
