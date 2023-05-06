from django.urls import path
from .views import *
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import (
    MyPasswordResetView,
    MyPasswordResetDoneView,
    MyPasswordResetConfirmView,
    MyPasswordResetCompleteView,
)
from . import views

urlpatterns = [
    path('signup/',signUp, name="signup"),
    path('',logIn, name="login"),
    path('index/',Index, name="index"),
    path('logout/',logOut, name="logout"),
    path('about/', aboutUs, name="about"),
    path('user_account/', userAccount, name="user_account"),
    path('profile/', user_profile, name='user_profile'),
    path('index1/', recettes_view, name='recettes'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('ajouter_commentaire/', ajouter_commentaire, name='ajouter_commentaire'),

    path('ajouter_rank/<int:recette_id>/',  ajouter_rank, name='ajouter_rank'),

    
    path('reset_password/', MyPasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/',MyPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/',MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
]
