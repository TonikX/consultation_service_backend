from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    """Чтение/обновление юзера"""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "employee_number",
            "role",
            "tel",
            "full_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_full_name(self, obj):
        parts = [obj.last_name, obj.first_name, obj.middle_name]
        return " ".join(filter(None, parts))


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Создание юзера"""

    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    re_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, label="Подтверждение пароля"
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "re_password",
            "first_name",
            "last_name",
            "middle_name",
            "employee_number",
            "role",
            "tel",
        ]

    def validate(self, data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        """Создание пользователя с хешированием пароля"""
        validated_data.pop("re_password")
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сокращенный для списка юзеров"""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "full_name", "email", "role", "employee_number"]

    def get_full_name(self, obj):
        parts = [obj.last_name, obj.first_name, obj.middle_name]
        return " ".join(filter(None, parts))


class EventCreateSerializer(serializers.ModelSerializer):
    """Создание мероприятия"""

    group_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True,
        help_text="Список ID групп для проверки пересечений (опционально)",
    )

    class Meta:
        model = Event
        fields = [
            "flow",
            "event_name",
            "start_time",
            "end_time",
            "recommended_number_students",
            "note",
            "event_location",
            "time_on_one_student",
            "group_ids",
        ]

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError(
                "Время окончания должно быть позже времени начала"
            )

        group_ids = data.get("group_ids")
        if group_ids is not None:
            existing_groups = Group.objects.filter(id__in=group_ids)
            if len(existing_groups) != len(group_ids):
                raise serializers.ValidationError("Некоторые группы не найдены")

        return data


class EventListSerializer(serializers.ModelSerializer):
    """Список мероприятий со статистикой"""

    flow_name = serializers.CharField(source="flow.flow_name", read_only=True)
    subject_name = serializers.CharField(
        source="flow.subject.subject_name", read_only=True
    )
    teachers = serializers.SerializerMethodField()
    registered_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    groups = serializers.StringRelatedField(
        many=True, source="groups.group", read_only=True
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "event_name",
            "flow_name",
            "subject_name",
            "start_time",
            "end_time",
            "event_location",
            "teachers",
            "registered_count",
            "is_registered",
            "recommended_number_students",
            "groups",
            "note",
        ]

    def get_teachers(self, obj):
        teachers = CustomUser.objects.filter(
            teacher_subjects__events__event=obj
        ).distinct()
        return [f"{t.last_name} {t.first_name}" for t in teachers]

    def get_registered_count(self, obj):
        return StudentEvent.objects.filter(event=obj).count()

    def get_is_registered(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return StudentEvent.objects.filter(event=obj, user=request.user).exists()
        return False


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
