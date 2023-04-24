from django.urls import path
from .views import DailyUpdateView,ProfileCreateView, RegisterView, ProfileListView, UpdateListView, DailyUpdateView, AnnouncementView, AnnouncementListView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),                               #register  (tama)                                                               
    path('profile/', ProfileCreateView.as_view(), name='profile_list'),
    path('profile/<uuid:pk>/', ProfileListView.as_view(), name='Profile-Detail'),                    #Shows user profile, Get:UserID, POST: fname, lname, position    (tama)
    path('dailyupdate/', DailyUpdateView.as_view(), name='daily-updates'),                       #Show the daily update posted by user, Filter (UserID, Date)
    path('dailyupdate/<uuid:pk>/',  UpdateListView.as_view(), name='view-daily-update'),    #Post daily updates , UserID, Accomplished task, In Progress Task, Blocker (tama)
    path('announcement/',  AnnouncementView.as_view(), name='daily-updates'),              
    path('announcement/<uuid:pk>/', AnnouncementListView.as_view(), name='view-daily-update'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),                 #(tama)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
