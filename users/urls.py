from django.urls import path
from .views import home, CustomLoginView, custom_logout_view,SignUpView

from .views import CustomLoginView, custom_logout_view, SignUpView

urlpatterns = [
    path('', home , name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
