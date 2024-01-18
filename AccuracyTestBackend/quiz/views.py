from datetime import timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .models import QuizInfo


def startQuiz(request):
    print(timezone.now())
    quiz = QuizInfo.objects.filter(user__username='barbodak').update(start_time=timezone.now() - timedelta(hours=15))
    return HttpResponse(status=200)
# Create your views here.
