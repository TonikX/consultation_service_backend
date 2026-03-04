from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, permissions
from .serializers import *


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
