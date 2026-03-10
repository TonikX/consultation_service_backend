from django.forms import ValidationError
from rest_framework import filters

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .services import EventService

# Create your views here.

from rest_framework import viewsets, permissions
from .serializers import *

class CustomUserViewSet(viewsets.ModelViewSet):
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
            return CustomUserListSerializer  
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
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        elif self.action == 'list':
            return EventListSerializer
        return EventSerializer
    
    def perform_create(self, serializer):
        """Создание мероприятия с проверками"""
        group_ids = serializer.validated_data.pop('group_ids')
        groups = Group.objects.filter(id__in=group_ids)
        
        event, warnings = EventService.create_event(
            serializer.validated_data,
            self.request.user,
            groups
        )
        serializer.instance = event
        
        if warnings:
            self.warnings = warnings
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        
        if hasattr(self, 'warnings') and self.warnings:
            response_data['warnings'] = {
                'message': 'Обнаружены пересечения с существующими мероприятиями',
                'conflicts': self.warnings
            }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class StudentEventViewSet(viewsets.ModelViewSet):
    queryset = StudentEvent.objects.all()
    serializer_class = StudentEventSerializer
