from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("manager", "Manager"),
    ]

    employee_number = models.IntegerField(unique=True, null=True, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    role = models.CharField(
        max_length=15, choices=ROLE_CHOICES, default="student", db_index=True
    )
    tel = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name", "middle_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name} ({self.employee_number})"


class Program(models.Model):
    program_number = models.CharField(max_length=8)
    program_name = models.CharField(max_length=100)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["program_number"]

    def __str__(self):
        return f"{self.program_name} ({self.program_number})"


class Group(models.Model):
    name_group = models.CharField(max_length=10)
    program = models.ForeignKey(
        Program, on_delete=models.PROTECT, related_name="groups"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_date", "name_group"]

    def __str__(self):
        return f"{self.name_group} ({self.start_date} - {self.end_date})"


class Subject(models.Model):
    subject_number = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["subject_name"]

    def __str__(self):
        return self.subject_name


class TeacherSubjects(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name="teachers"
    )
    teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="teacher_subjects"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("subject", "teacher")
        ordering = ["subject__subject_name"]

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name} - {self.subject.subject_name}"


class TeacherSubjectsEvent(models.Model):
    teacher_subject = models.ForeignKey(
        TeacherSubjects, on_delete=models.CASCADE, related_name="events"
    )
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="teacher_assignments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("teacher_subject", "event")
        ordering = ["event__start_time"]

    def __str__(self):
        return f"{self.teacher_subject} - {self.event}"


class Flow(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="flows")
    flow_name = models.CharField(max_length=100)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField()
    flow_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["flow_name", "start_date"]

    def __str__(self):
        return self.flow_name


class StudentFlow(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_flows"
    )
    flow = models.ForeignKey(
        Flow, on_delete=models.CASCADE, related_name="students_in_flow"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "flow")

    def __str__(self):
        return f"{self.flow.flow_name} - {self.student.employee_number}"


class Event(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="events")
    event_name = models.CharField(max_length=100)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()
    recommended_number_students = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=512, blank=True)
    is_scheduled = models.BooleanField(default=False)
    time_on_one_student = models.IntegerField(null=True, blank=True)
    event_location = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_time", "event_name"]

    def __str__(self):
        return f"{self.event_name}"


class WroteTime(models.Model):
    time = models.DateTimeField()
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="written_times"
    )

    class Meta:
        ordering = ["event__start_time", "time"]

    def __str__(self):
        return f"{self.event} - {self.time}"


class StudentEvent(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_events",
    )
    time = models.OneToOneField(
        WroteTime, on_delete=models.CASCADE, related_name="student_event"
    )
    note_student = models.CharField(max_length=255, blank=True)
    note_teacher = models.CharField(max_length=255, blank=True)
    is_visit = models.BooleanField(default=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_events"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["event__start_time", "created_at"]

    def __str__(self):
        return f"{self.event} - {self.user}"


class UserGroup(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_groups"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_users"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")
        ordering = ["user__last_name", "user__first_name", "start_date"]

    def __str__(self):
        return f"{self.user.employee_number} - {self.group.name_group}"


class ProgramSubjects(models.Model):
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="program_subjects"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name="subject_programs"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("program", "subject")
        ordering = ["program__program_number", "subject__subject_name"]

    def __str__(self):
        return f"{self.program.program_name} - {self.subject.subject_name}"


class EventGroup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="groups")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "group")
        ordering = ["event__start_time", "group__name_group"]

    def __str__(self):
        return f"{self.event} - {self.group.name_group}"


class EventFlow(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_flows"
    )
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="event_flows")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "flow")
        ordering = ["event__start_time", "flow__flow_name"]

    def __str__(self):
        return f"{self.event} - {self.flow.flow_name}"
