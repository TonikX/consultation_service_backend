from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import (
    Event,
    StudentEvent,
    WroteTime,
    CustomUser,
    Group,
    EventGroup,
    TeacherSubjects,
    TeacherSubjectsEvent,
    StudentGroup,
)
from django.db.models import Q


class EventService:
    """Сервис для управления мероприятиями, включая проверку пересечений
    и создание/обновление мероприятий"""

    @staticmethod
    def check_event_conflict(groups, start_time, end_time, exclude_event_id=None):
        """
        Проверка пересечений мероприятий для групп.
        Возвращает список конфликтующих мероприятий
        """
        conflicting_events = Event.objects.filter(
            start_time__lt=end_time, end_time__gt=start_time
        )

        if exclude_event_id:
            conflicting_events = conflicting_events.exclude(id=exclude_event_id)

        conflicting_events = conflicting_events.filter(
            groups__group__in=groups
        ).distinct()

        return conflicting_events

    @staticmethod
    def get_conflict_warnings(groups, start_time, end_time, exclude_event_id=None):
        """
        Получить предупреждения о пересечениях для групп
        """
        conflicts = EventService.check_event_conflict(
            groups, start_time, end_time, exclude_event_id
        )

        if not conflicts.exists():
            return None

        warnings = []
        for group in groups:
            group_conflicts = conflicts.filter(groups__group=group)
            if group_conflicts.exists():
                warnings.append(
                    {
                        "group_id": group.id,
                        "group_name": group.name_group,
                        "conflicting_events": [
                            {
                                "id": e.id,
                                "name": e.event_name,
                                "start": e.start_time,
                                "end": e.end_time,
                            }
                            for e in group_conflicts
                        ],
                    }
                )

        return warnings

    @staticmethod
    def create_event(data, teacher, groups=None):
        """
        Создание мероприятия с проверкой пересечений
        """
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        warnings = None
        if groups:
            warnings = EventService.get_conflict_warnings(groups, start_time, end_time)

        flow = data.get("flow")
        teacher_subject = TeacherSubjects.objects.filter(
            teacher=teacher, subject=flow.subject
        ).exists()

        if not teacher_subject and teacher.role != "admin":
            raise ValidationError(
                "Вы не можете создавать мероприятия по этому предмету"
            )

        # Создание мероприятия в транзакции
        with transaction.atomic():
            event = Event.objects.create(**data)

            TeacherSubjectsEvent.objects.create(
                teacher_subject=TeacherSubjects.objects.get(
                    teacher=teacher, subject=flow.subject
                ),
                event=event,
            )

            if groups:
                for group in groups:
                    EventGroup.objects.create(event=event, group=group)

        return event, warnings

    @staticmethod
    def update_event(event_id, data, teacher, groups=None):
        """
        Обновление мероприятия с проверкой пересечений
        (только предупреждение)
        """
        event = Event.objects.get(id=event_id)
        start_time = data.get("start_time", event.start_time)
        end_time = data.get("end_time", event.end_time)

        event_teacher = TeacherSubjectsEvent.objects.filter(event=event).first()

        if (
            event_teacher
            and event_teacher.teacher_subject.teacher != teacher
            and teacher.role != "admin"
        ):
            raise ValidationError("Вы не можете редактировать это мероприятие")

        if "flow" in data:
            new_flow = data.get("flow")
            teacher_subject = TeacherSubjects.objects.filter(
                teacher=teacher, subject=new_flow.subject
            ).exists()

            if not teacher_subject and teacher.role != "admin":
                raise ValidationError(
                    "Вы не можете создать мероприятие по этому предмету"
                )

        warnings = None
        if groups:
            warnings = EventService.get_conflict_warnings(
                groups, start_time, end_time, exclude_event_id=event_id
            )

        if start_time >= end_time:
            raise ValidationError("Время окончания должно быть позже времени начала")

        with transaction.atomic():
            for key, value in data.items():
                setattr(event, key, value)
            event.save()

            if "flow" in data:
                TeacherSubjectsEvent.objects.filter(event=event).delete()
                TeacherSubjectsEvent.objects.create(
                    teacher_subject=TeacherSubjects.objects.get(
                        teacher=teacher, subject=event.flow.subject
                    ),
                    event=event,
                )

            if groups is not None:
                EventGroup.objects.filter(event=event).delete()
                for group in groups:
                    EventGroup.objects.create(event=event, group=group)

        return event, warnings
