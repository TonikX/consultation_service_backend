from django.shortcuts import render
from rest_framework import filters

# Create your views here.

from rest_framework import viewsets, permissions
from .serializers import *

class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'employee_number']
    ordering_fields = ['last_name', 'created_at', 'role']

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomUserListSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    def get_serializer_class(self):
        if self.action == 'list':
            return CustomUserListSerializer  # упрощенный для списка
        return CustomUserSerializer
    


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
  

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class TeacherSubjectsViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubjects.objects.all()
    serializer_class = TeacherSubjectsSerializer

class WroteTimeViewSet(viewsets.ModelViewSet):
    queryset =  WroteTime.objects.all()
    serializer_class = WroteTimeSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class StudentEventViewSet(viewsets.ModelViewSet):
    queryset = StudentEvent.objects.all()
    serializer_class = StudentEventSerializer
