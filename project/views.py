
import uuid
from rest_framework import generics
from django.shortcuts import render
from .models import Profile, Account, DailyUpdate
from .serializers import ProfileSerializer, AccountSerializer, DailyUpdateSerializer, RegisterSerializer, LoginSerializer
from rest_framework.generics import GenericAPIView  ,RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.viewsets import ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminStaffReadOnly,  ProfileOwnerReadOnly, ProfileOwnerCanEdit, DailyUpdateOwnerCanEdit
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
'''
class ProfileDetailView(generics.UpdateAPIView):        #path('profile/<uuid:pk>'
    #permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
'''


class ProfileListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
         return self.create(request, *args, **kwargs)

class AccountView(GenericAPIView, ListModelMixin):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(userID=self.request.user.userID)
        return queryset
 
class DailyUpdateView(generics.ListAPIView):                              # path('dailyupdate/',
    queryset = DailyUpdate.objects.all()
    permission_classes = [IsAdminStaffReadOnly, ]
    serializer_class = DailyUpdateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'datetime']
    
class RegisterView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LogInView(generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = LoginSerializer


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([ProfileOwnerCanEdit, IsAuthenticated])
def ProfileDetailView(request, pk):
    
    if request.method == 'GET': 
        try:
            profile = Profile.objects.get(user=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            profile = Profile.objects.get(user=pk)  # Retrieve profile associated with the provided uuid
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([DailyUpdateOwnerCanEdit, IsAuthenticated])
def CreateDailyUpdateView(request, pk):

    if request.method == 'GET':
        #dailyupdates = DailyUpdate.objects.filter(account=account)
        serializer = DailyUpdateSerializer(dailyupdates, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        data = {
           # 'account': account.userID,
            'accomplishedTask': request.data.get('accomplishedTask'),
            'inProgressTask': request.data.get('inProgressTask'),
            'blocker': request.data.get('blocker'),
            'datetime': request.data.get('datetime'),
        }
        serializer = DailyUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        try:
            dailyupdate = DailyUpdate.objects.get(pk=pk)  # Retrieve daily update associated with the provided uuid
        except DailyUpdate.DoesNotExist:
            return Response({"error": "Update not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Only the owner of the daily update can edit it
       # if dailyupdate.account != account:
        #    return Response({"error": "You are not authorized to edit this daily update."}, status=status.HTTP_401_UNAUTHORIZED)
            
        serializer = DailyUpdateSerializer(dailyupdate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
