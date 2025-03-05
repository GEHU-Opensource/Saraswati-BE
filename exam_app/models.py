from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Exam(models.Model):
    exam_id = models.BigIntegerField(primary_key=True)
    exam_name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_for = models.CharField(max_length=255)
    total_questions = models.BigIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creation_date = models.DateField(auto_now_add=True)
    exam_org = models.CharField(max_length=255)
    question_ids = ArrayField(models.BigIntegerField(), blank=True, default=list)
    exam_type = models.CharField(max_length=255)
    total_marks = models.BigIntegerField()
    duration = models.TimeField()
    time_per_ques = models.TimeField()
    exam_prefix = models.CharField(max_length=255)
    reset_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.exam_name} - {self.exam_org}"
