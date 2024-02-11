from datetime import timedelta
from warnings import warn
from django.contrib.auth.models import User
from django.db.models import query
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from account.models import Account
from .models import AcuTest, QuizInfo, ValuTest
from .serializers import AcuTestSerializer, ValuTestSerializer  # , QuizInfoSerializer


class QuizViewSet(viewsets.ViewSet):

    authentication_classes = (TokenAuthentication,)
    ermission_classes = (IsAuthenticated,)

    def get_quiz(self, quiz_type, user) -> AcuTest | ValuTest | None:
        acc = Account.objects.get(user=user)
        match quiz_type:
            case "AcuTest":
                if acc.acuTest_permition is False:
                    return None
                quiz = AcuTest.objects.get(quiz_info__user=user)
            case "ValuTest":
                if acc.valTest_permition is False:
                    return None
                quiz = ValuTest.objects.get(quiz_info__user=user)
            case _:  # Default case for unmatched quiz_type
                raise ValueError(f"Unrecognized quiz type: {quiz_type}")
        return quiz

    def calculateValuTestResult(self, quiz):
        answers = quiz.answers
        for i in range(20):
            if answers[i] in (3, 7, 10, 14, 18, 19):
                quiz.sharayet_kari += (i % 5) + 1
            if answers[i] in (2, 16, 17):
                quiz.hemayat += ((i % 5) + 1) * 2
            if answers[i] in (8, 11, 15):
                quiz.ravabet += ((i % 5) + 1) * 2
            if answers[i] in (4, 5, 12):
                quiz.pishraft += ((i % 5) + 1) * 2
            if answers[i] in (9, 13, 20):
                quiz.esteghlal += ((i % 5) + 1) * 2
            if answers[i] in (1, 6):
                quiz.tofigh += ((i % 5) + 1) * 3
            quiz.save()

    def startQuiz(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        if quiz is None:
            return HttpResponse(status=400)
        if quiz.quiz_info.start_time is None:
            quiz.quiz_info.start_time = timezone.now()
            quiz.quiz_info.save()
            print(quiz.quiz_info.start_time)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    def submitAnswer(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        if quiz is None or quiz.quiz_info.start_time is None:
            return HttpResponse(status=400)
        match quiz_type:
            case "AcuTest":
                if (timezone.now() - quiz.quiz_info.start_time).seconds > 60 * 5 + 10:
                    return HttpResponse(status=400)
            case "ValuTest":
                if (timezone.now() - quiz.quiz_info.start_time).seconds > 60 * 180:
                    return HttpResponse(status=400)
                else:
                    self.calculateValuTestResult(quiz)

        print(request.data.get('answers'))
        quiz.answers = request.data.get('answers')
        quiz.save()
        return HttpResponse(status=200)

    def retrieve(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        print(quiz)
        if quiz is None or quiz.quiz_info.start_time is None:
            return JsonResponse({f"quiz_info": "not_started"})
        match quiz_type:
            case "AcuTest":
                return JsonResponse(AcuTestSerializer(quiz).data)
            case "ValuTest":
                return JsonResponse(ValuTestSerializer(quiz).data)
            case _:
                return HttpResponse(status=400)

    def hasQuizEnded(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        if quiz is None or (timezone.now() - quiz.quiz_info.start_time).seconds > 60 * 5:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
