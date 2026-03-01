from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('manager', 'Manager'),
    ]


    employee_number = models.IntegerField(unique=True, null=True, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='student')
    tel = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name} ({self.employee_number})"


class Program(models.Model):
    id_program = models.AutoField(primary_key=True)
    program_number = models.CharField(max_length=8)
    program_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.program_name} ({self.program_number})'


class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
    name_group = models.CharField(max_length=10)
    id_program = models.ForeignKey(Program, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name_group


class Subject(models.Model):
    id_subject = models.AutoField(primary_key=True)
    subject_number = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.subject_name


class TeacherSubjects(models.Model):
    id_teacher_subject = models.AutoField(primary_key=True)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_user.first_name} {self.id_user.last_name} - {self.id_subject.subject_name}"


class TeacherSubjectsEvent(models.Model):
    id_teacher_subject_event = models.ForeignKey(TeacherSubjects, on_delete=models.CASCADE)
    id_event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_teacher_subject_event} - {self.id_event}"


class GroupFlow(models.Model):
    id_flow = models.AutoField(primary_key=True)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    flow_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    flow_type = models.CharField(max_length=20)

    def __str__(self):
        return self.flow_name


class StudentFlow(models.Model):
    id_student_flow = models.AutoField(primary_key=True)
    id_student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_flow = models.ForeignKey(GroupFlow, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_flow.flow_name} - {self.id_student.employee_number}"


class Event(models.Model):
    id_event = models.AutoField(primary_key=True)
    id_flow = models.ForeignKey(GroupFlow, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recomended_number_students = models.IntegerField()
    note = models.CharField(max_length=512, blank=True)
    is_scheduled = models.BooleanField(default=False)
    time_on_one_student = models.IntegerField()
    event_location = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.id_event}"


class WroteTime(models.Model):
    id_time = models.AutoField(primary_key=True)
    time = models.CharField(max_length=25)
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)


class StudentEvent(models.Model):
    id_wrote = models.AutoField(primary_key=True)
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_time = models.ForeignKey(WroteTime, on_delete=models.CASCADE)
    note_student = models.CharField(max_length=255, blank=True)
    note_teacher = models.CharField(max_length=255, blank=True)
    is_visit = models.BooleanField(default=False)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    register_time = models.DateTimeField()


class UserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class ProgramSubjects(models.Model):
    id_program = models.ForeignKey(Program, on_delete=models.CASCADE)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class EventGroup(models.Model):
    id_event_group = models.AutoField(primary_key=True)
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)


class EventFlow(models.Model):
    id_event_flow = models.AutoField(primary_key=True)
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_flow = models.ForeignKey(GroupFlow, on_delete=models.CASCADE)

    