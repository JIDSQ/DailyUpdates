from django.urls import path
from .views import DailyUpdateView, AccountView, RegisterView, LogInView, ProfileListView, CreateDailyUpdateView, ProfileDetailView,  CreateDailyUpdateView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),                               #register  (tama)
    path('login/', LogInView.as_view(), name = 'Login'),                                                                    
    #logout
    path('profile/', ProfileListView.as_view(), name='profile_list'),
    path('profile/<uuid:pk>/', ProfileDetailView, name='Profile-Detail'),                    #Shows user profile, Get:UserID, POST: fname, lname, position    (tama)
    path('dailyupdate/', DailyUpdateView.as_view(), name='daily-updates'),                       #Show the daily update posted by user, Filter (UserID, Date)
    path('dailyupdate/<int:pk>',  CreateDailyUpdateView, name='view-daily-update'),    #Post daily updates , UserID, Accomplished task, In Progress Task, Blocker (tama)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),                 #(tama)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
