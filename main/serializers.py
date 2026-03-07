from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения/обновления пользователя"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'middle_name',
            'employee_number', 'role', 'tel', 'full_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        parts = [obj.last_name, obj.first_name, obj.middle_name]
        return ' '.join(filter(None, parts))


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    re_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, label='Подтверждение пароля')

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 're_password',
            'first_name', 'last_name', 'middle_name',
            'employee_number', 'role', 'tel'
        ]

    def validate(self, data):
        if data['password'] != data['re_password']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        """Создание пользователя с хешированием пароля"""
        validated_data.pop('re_password')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CustomUserListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка пользователей"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'email', 'role', 'employee_number']

    def get_full_name(self, obj):
        parts = [obj.last_name, obj.first_name, obj.middle_name]
        return ' '.join(filter(None, parts))


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class TeacherSubjectsSerializer(serializers.ModelSerializer):
    subject_id = serializers.PrimaryKeyRelatedField(source="id_subject", read_only=True)
    subject_name = serializers.CharField(
        source="id_subject_subject_name", read_only=True
    )
    teacher_id = serializers.PrimaryKeyRelatedField(source="id_user", read_only=True)
    teacher_str = serializers.StringRelatedField(source="id_user", read_only=True)

    class Meta:
        model = TeacherSubjects
        fields = [
            "id",
            "subject_id",
            "subject_name",
            "teacher_id",
            "teacher_str",
        ]


class TeacherSubjectsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubjectsEvent
        fields = "__all__"

class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = "__all__"

class StudentFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFlow
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class WroteTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WroteTime
        fields = "__all__"

class StudentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvent
        fields = "__all__"

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = "__all__"

class ProgramSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramSubjects
        fields = "__all__"

class EventGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGroup
        fields = "__all__"

class EventFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFlow
        fields = "__all__"