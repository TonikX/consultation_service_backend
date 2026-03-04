from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


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
            "id_teacher_subject",
            "subject_id",
            "subject_name",
            "teacher_id",
            "teacher_str",
        ]
