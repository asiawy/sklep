from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from .views import logout_view
from . import views
from .forms import LoginForm
from django.contrib.auth import logout


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),

]