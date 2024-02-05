from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models import query
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .models import AcuTest, QuizInfo, ValuTest
from .serializers import AcuTestSerializer  # , QuizInfoSerializer

#
# def startQuiz(request):
#     print(timezone.now())
#     quiz = QuizInfo.objects.filter(user__username='barbodak').update(
#         start_time=timezone.now() - timedelta(hours=15))
#     return HttpResponse(status=200)
#


class QuizViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_quiz(self, quiz_type, user) -> AcuTest | ValuTest:
        match quiz_type:
            case "AcuTest":
                quiz = AcuTest.objects.all().get(user=user)
            case "ValuTest":
                quiz = ValuTest.objects.all().get(user=user)
            case _:  # Default case for unmatched quiz_type
                raise ValueError(f"Unrecognized quiz type: {quiz_type}")
        return quiz

    def startQuiz(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        quiz.quiz_info.start_time = timezone.now()
        quiz.save()
        return HttpResponse(status=200)

    def submitAnswer(self, request, quiz_type, serializer):
        quiz = self.get_quiz(quiz_type, request.user)
        return HttpResponse(status=200)
