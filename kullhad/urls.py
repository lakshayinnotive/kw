from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('product/', views.product, name='product'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('passwordchange/', views.passwordchange, name='passwordchange'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset/<uidb64>', views.reset, name='reset'),
    path('finalreset', views.finalreset, name='finalreset'),
    path('news/', views.news, name='news'),
    path('blog/', views.blog, name='blog'),


    # forgot password
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
