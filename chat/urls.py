from django.urls import path

from chat.views import SignUpView, LoginView, LogoutView, \
    ListUsersView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('list/', ListUsersView.as_view(), name='list'),
]