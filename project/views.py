
import uuid
from rest_framework import generics
from django.shortcuts import render
from .models import Profile, Account, DailyUpdate, Announcement
from .serializers import ProfileSerializer, RegisterSerializer, UpdateCreateSerializer, UpdateSerializer, UpdateCreateSerializer, ProfileCreateSerializer,AnnouncementCreateSerializer, AnnouncementSerialier
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwner, UpdateIsOwner, IsAdmin


# Create your views here.

#Register
class RegisterView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


#path('profile/')
class ProfileCreateView(generics.ListCreateAPIView):        
    serializer_class = ProfileCreateSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
#path('profile/<uuid:pk>')
class ProfileListView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Profile.objects.all()
    lookup_field = 'pk'                                             #nilalagay sa parameter sa url, kailangan pag gumagamit ng Retrieve


#path('dailyupdate/') with filter
class DailyUpdateView(generics.ListCreateAPIView):
    serializer_class =  UpdateCreateSerializer                    
    queryset = DailyUpdate.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'updateID': ['exact'],
        'datetime': ['date'],
    }


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#path('dailyupdate/<int:pk>',
class UpdateListView(generics.RetrieveUpdateDestroyAPIView):        
    serializer_class =  UpdateSerializer     
    permission_classes = [IsAuthenticated, UpdateIsOwner]
    queryset =  DailyUpdate.objects.all()
    lookup_field = 'pk' 

    
   
class AnnouncementView(generics.ListCreateAPIView):
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'datetime': ['date']}
    

    def perform_create(self, serializer):
            serializer.save(adminID=self.request.user)


class AnnouncementListView(generics.RetrieveUpdateDestroyAPIView):     
    serializer_class =  AnnouncementSerialier           
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Announcement.objects.all()
    lookup_field = 'pk' 
