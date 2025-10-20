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

from . import conf

from account.models import Account
from .models import AcuTest_pic, AcuTest_text, ValuTest
from .serializers import (
    AcuTestPicSerializer,
    AcuTestTextSerializer,
    ValuTestSerializer,
)  # , QuizInfoSerializer


class QuizViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    ermission_classes = (IsAuthenticated,)

    def get_quiz(self, quiz_type, user) -> AcuTest_pic | AcuTest_text | ValuTest | None:
        acc = Account.objects.get(user=user)
        match quiz_type:
            case "AcuTest_pic":
                if acc.acuTest_permition is False:
                    return None
                quiz = AcuTest_pic.objects.get(user=user)
            case "AcuTest_text":
                if acc.acuTest_permition is False:
                    return None
                quiz = AcuTest_text.objects.get(user=user)
            case "ValuTest":
                if acc.valTest_permition is False:
                    return None
                quiz = ValuTest.objects.get(user=user)
            case _:  # Default case for unmatched quiz_type
                raise ValueError(f"Unrecognized quiz type: {quiz_type}")
        return quiz

    def calculateValuTestResult(self, quiz):
        answers = quiz.answers
        print("fuck")
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
        print("start")
        quiz = self.get_quiz(quiz_type, request.user)
        if quiz is None:
            return HttpResponse(status=400)
        if quiz.quiz_time.start_time is None:
            quiz.quiz_time.start_time = timezone.now()
            quiz.quiz_time.save()
            print(quiz.quiz_time.start_time)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    def submitAnswer(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        if quiz is None or quiz.quiz_time.start_time is None:
            return HttpResponse(status=400)
        match quiz_type:
            case "AcuTest_pic":
                if (
                    timezone.now() - quiz.quiz_time.start_time
                ).seconds > conf.ACU_TEST_PIC_TIMELIMIT_SECONDS:
                    return HttpResponse(status=400)
            case "AcuTest_time":
                if (
                    timezone.now() - quiz.quiz_time.start_time
                ).seconds > conf.ACU_TEST_TEXT_TIMELIMIT_SECONDS:
                    return HttpResponse(status=400)
            case "ValuTest":
                if (
                    timezone.now() - quiz.quiz_time.start_time
                ).seconds > conf.VALU_TEST_TIMELIMIT_SECONDS:
                    self.calculateValuTestResult(quiz)
                    return HttpResponse(status=400)

        print(request.data.get("answers"))
        quiz.answers = request.data.get("answers")
        quiz.quiz_time.finish_time = timezone.now()
        quiz.save()
        return HttpResponse(status=200)

    def retrieve(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        print(quiz)
        if quiz is None or quiz.quiz_time.start_time is None:
            return JsonResponse({"quiz_time": "not_started"})
        match quiz_type:
            case "AcuTest_pic":
                return JsonResponse(AcuTestPicSerializer(quiz).data)
            case "AcuTest_text":
                return JsonResponse(AcuTestTextSerializer(quiz).data)
            case "ValuTest":
                return JsonResponse(ValuTestSerializer(quiz).data)
            case _:
                return HttpResponse(status=400)

    def hasQuizEnded(self, request, quiz_type):
        quiz = self.get_quiz(quiz_type, request.user)
        if (
            quiz is None
            or (timezone.now() - quiz.quiz_time.start_time).seconds > 60 * 5
        ):
            return HttpResponse(status=400)

        return HttpResponse(status=200)
