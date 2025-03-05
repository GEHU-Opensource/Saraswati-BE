from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import timedelta, time
import random
import uuid

from .models import Exam
from .serializers import ExamSerializer


@api_view(["POST"])
def create_exam(request):
    if request.method == "POST":
        serializer = ExamSerializer(data=request.data)

        if serializer.is_valid():
            # Parse start_date and end_date from request data
            start_date_str = request.data.get("start_date")
            end_date_str = request.data.get("end_date")

            start_date = parse_datetime(start_date_str) if start_date_str else None
            end_date = parse_datetime(end_date_str) if end_date_str else None

            # Ensure timezone-awareness
            if start_date and start_date.tzinfo is None:
                start_date = timezone.make_aware(
                    start_date, timezone.get_current_timezone()
                )

            if end_date and end_date.tzinfo is None:
                end_date = timezone.make_aware(
                    end_date, timezone.get_current_timezone()
                )

            # Generate a random exam prefix (integer)
            exam_prefix = random.randint(1000, 9999)

            # Parse duration and time_per_ques
            duration_str = request.data.get(
                "duration", "00:30:00"
            )  # Default 30 minutes
            time_per_ques_str = request.data.get(
                "time_per_ques", "00:01:00"
            )  # Default 1 minute

            duration = time.fromisoformat(duration_str)
            time_per_ques = time.fromisoformat(time_per_ques_str)

            # Save the instance with additional fields
            serializer.save(
                creation_date=timezone.now().date(),
                start_date=start_date,
                end_date=end_date,
                exam_prefix=exam_prefix,
                reset_token=uuid.uuid4(),  # Ensure a new reset_token is generated
                duration=duration,
                time_per_ques=time_per_ques,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
