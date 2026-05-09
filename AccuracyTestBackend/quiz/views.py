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

import account

from . import conf

from account.models import Account
from .models import (
    AcuTest_pic,
    AcuTest_text,
    Quiztime,
    ValuTest,
    BelbinTest,
    HexacoTest,
)
from .serializers import (
    AcuTestPicSerializer,
    AcuTestPicAnswerSerializer,
    AcuTestTextSerializer,
    AcuTestTextAnswerSerializer,
    ValuTestSerializer,
    ValuTestAnswerSerializer,
    BelbinTestSerializer,
    HexacoTestSerializer,
)
import logging


class QuizViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    ermission_classes = (IsAuthenticated,)

    def get_quiz(
        self, quiz_type, user
    ) -> AcuTest_pic | AcuTest_text | ValuTest | BelbinTest | HexacoTest | None:
        acc = Account.objects.get(user=user)
        logger = logging.getLogger(__name__)
        logger.warning(acc)
        match quiz_type:
            case "AcuTest_pic":
                if acc.acuTest_permission is False:
                    return None
                quiz = AcuTest_pic.objects.get(account=acc)
            case "AcuTest_text":
                if acc.acuTest_permission is False:
                    return None
                quiz = AcuTest_text.objects.get(account=acc)
            case "ValuTest":
                if acc.valuTest_permission is False:
                    return None
                quiz = ValuTest.objects.get(account=acc)
            case "BelbinTest":
                if acc.belbinTest_permission is False:
                    return None
                quiz = BelbinTest.objects.get(account=acc)
            case "HexacoTest":
                if acc.hexacoTest_permission is False:
                    return None
                quiz = HexacoTest.objects.get(account=acc)
            case _:  # Default case for unmatched quiz_type
                raise ValueError(f"Unrecognized quiz type: {quiz_type}")
        logger.warning(quiz)
        return quiz

    def quizHasEnded(self, quiz, quiz_type):
        logger = logging.getLogger(__name__)
        match quiz_type:
            case "AcuTest_pic":
                if (
                    (timezone.now() - quiz.quiz_time.start_time).seconds
                    > conf.ACU_TEST_PIC_TIMELIMIT_SECONDS
                    or quiz.quiz_time.finish_time is not None
                ):
                    return True
            case "AcuTest_text":
                if (
                    (timezone.now() - quiz.quiz_time.start_time).seconds
                    > conf.ACU_TEST_TEXT_TIMELIMIT_SECONDS
                    or quiz.quiz_time.finish_time is not None
                ):
                    return True
            case "ValuTest":
                if (
                    (timezone.now() - quiz.quiz_time.start_time).seconds
                    > conf.VALU_TEST_TIMELIMIT_SECONDS
                    or quiz.quiz_time.finish_time is not None
                ):
                    logger.warning("ITS FINISHED")
                    return True
            case "BelbinTest":
                if (
                    (timezone.now() - quiz.quiz_time.start_time).seconds
                    > conf.BELBIN_TIMELIMIT_SECONDS
                    or quiz.quiz_time.finish_time is not None
                ):
                    logger.warning("ITS FINISHED")
                    return True
            case "HexacoTest":
                if (
                    (timezone.now() - quiz.quiz_time.start_time).seconds
                    > conf.HEXACO_TIMELIMIT_SECONDS
                    or quiz.quiz_time.finish_time is not None
                ):
                    logger.warning("ITS FINISHED")
                    return True
        return False

    def calculateValuTestResult(self, quiz: ValuTest):
        logger = logging.getLogger(__name__)
        answers = quiz.answers
        quiz.sharayet_kari = 0
        quiz.tofigh = 0
        quiz.hemayat = 0
        quiz.ravabet = 0
        quiz.esteghlal = 0
        quiz.pishraft = 0
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

    def calculateAcuTestPicResult(self, quiz: AcuTest_pic):
        logger = logging.getLogger(__name__)
        user_answers = quiz.answers
        key = conf.ACU_TEST_PIC_RES
        quiz.correct = 0
        quiz.wrong = 0
        for i in range(conf.ACU_TEST_PIC_QUESTION_COUNT):
            if user_answers[i] != 0:
                if user_answers[i] == key[i]:
                    quiz.correct += 1
                else:
                    quiz.wrong += 1
        quiz.save()

    def calculateAcuTestTextResult(self, quiz: AcuTest_text):
        logger = logging.getLogger(__name__)
        logger.warning("enterd_2")
        user_answers = quiz.answers
        key = conf.ACU_TEST_TEXT_RES
        quiz.correct = 0
        quiz.wrong = 0
        quiz.num_of_no = 0
        quiz.num_of_yes = 0
        quiz.no_no = 0
        quiz.no_yes = 0
        quiz.yes_yes = 0
        quiz.yes_no = 0
        for i in range(conf.ACU_TEST_TEXT_QUESTION_COUNT):
            if user_answers[i] == 1:
                quiz.num_of_yes += 1
                if 1 == key[i]:
                    quiz.correct += 1
                    quiz.yes_yes += 1
                else:
                    quiz.wrong += 1
                    quiz.yes_no += 1
            elif user_answers[i] == 2:
                quiz.num_of_no += 1
                if 1 == key[i]:
                    quiz.wrong += 1
                    quiz.no_yes += 1
                else:
                    quiz.correct += 1
                    quiz.no_no += 1
        quiz.save()

    def calculateBelbinTestResult(self, quiz: BelbinTest):
        logger = logging.getLogger(__name__)
        logger.warning("enterd_3")
        user_answers = quiz.answers

        role_patterns = {
            "sh": [(0, 2), (1, 0), (2, 6), (3, 1), (4, 5), (5, 5), (6, 4)],
            "co": [(0, 6), (1, 5), (2, 3), (3, 2), (4, 4), (5, 3), (6, 6)],
            "pl": [(0, 3), (1, 4), (2, 5), (3, 5), (4, 0), (5, 4), (6, 5)],
            "ri": [(0, 5), (1, 7), (2, 1), (3, 3), (4, 6), (5, 0), (6, 2)],
            "me": [(0, 4), (1, 3), (2, 2), (3, 4), (4, 2), (5, 2), (6, 1)],
            "imp": [(0, 0), (1, 6), (2, 4), (3, 0), (4, 3), (5, 7), (6, 0)],
            "tw": [(0, 7), (1, 2), (2, 7), (3, 7), (4, 1), (5, 6), (6, 7)],
            "cf": [(0, 1), (1, 1), (2, 0), (3, 6), (4, 7), (5, 1), (6, 3)],
        }

        for role, patterns in role_patterns.items():
            setattr(
                quiz,
                role,
                sum(user_answers[section * 8 + offset] for section, offset in patterns),
            )
        quiz.save()

    def calculateHexacoTestResult(self, quiz: HexacoTest):
        logger = logging.getLogger(__name__)
        logger.warning("enterd_3")
        user_answers = quiz.answers

        user_results: list[float] = [0] * 31

        for i in range(0, 100):
            if conf.BELBIN_REVERSE[i]:
                user_results[conf.BELBIN_KEY[i]] += (6 - user_answers[i]) / 4
            else:
                user_results[conf.BELBIN_KEY[i]] += user_answers[i] / 4
        user_results[0] = sum(user_results[1:5]) / 4
        user_results[5] = sum(user_results[6:10]) / 4
        user_results[10] = sum(user_results[11:15]) / 4
        user_results[15] = sum(user_results[16:20]) / 4
        user_results[20] = sum(user_results[21:25]) / 4
        user_results[25] = sum(user_results[26:30]) / 4

        quiz.results = user_results

        quiz.save()

    def route_calculation(self, quiz_type: str, quiz):
        logger = logging.getLogger(__name__)
        logger.warning("enterd_1")
        match quiz_type:
            case "ValuTest":
                self.calculateValuTestResult(quiz)

            case "AcuTest_pic":
                self.calculateAcuTestPicResult(quiz)

            case "AcuTest_text":
                self.calculateAcuTestTextResult(quiz)

            case "BelbinTest":
                self.calculateBelbinTestResult(quiz)

            case "HexacoTest":
                self.calculateHexacoTestResult(quiz)

    def startQuiz(self, request, quiz_type):
        logger = logging.getLogger(__name__)
        logger.warning("start")
        quiz = self.get_quiz(quiz_type, request.user)
        if quiz is None:
            return HttpResponse(status=400)
        if quiz.quiz_time.start_time is None:
            quiz.quiz_time.start_time = timezone.now()
            quiz.quiz_time.save()
            logger.warning(quiz.quiz_time.start_time)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    def submitAnswer(self, request, quiz_type):
        logger = logging.getLogger(__name__)
        logger.warning(request.data.get("answers"))
        quiz = self.get_quiz(quiz_type, request.user)
        if (
            quiz is None
            or quiz.quiz_time.start_time is None
            or self.quizHasEnded(quiz, quiz_type)
        ):
            return HttpResponse(status=400)

        logger.warning(request.data.get("answers"))
        quiz.answers = request.data.get("answers")
        quiz.quiz_time.finish_time = timezone.now()
        quiz.quiz_time.save()
        self.route_calculation(quiz_type, quiz)
        quiz.save()
        return HttpResponse(status=200)

    def retrieve(self, request, quiz_type):
        logger = logging.getLogger(__name__)
        logger.warning(quiz_type)
        quiz = self.get_quiz(quiz_type, request.user)
        if quiz is None or quiz.quiz_time.start_time is None:
            return JsonResponse({"quiz_time": "not_started"})
        match quiz_type:
            case "AcuTest_pic":
                return JsonResponse(AcuTestPicSerializer(quiz).data)
            case "AcuTest_text":
                return JsonResponse(AcuTestTextSerializer(quiz).data)
            case "ValuTest":
                return JsonResponse(ValuTestSerializer(quiz).data)
            case "BelbinTest":
                return JsonResponse(BelbinTestSerializer(quiz).data)
            case "HexacoTest":
                return JsonResponse(HexacoTestSerializer(quiz).data)
            case _:
                return HttpResponse(status=400)

    def retrieveAnswer(self, request, quiz_type):
        logger = logging.getLogger(__name__)
        quiz = self.get_quiz(quiz_type, request.user)
        logger.warning(quiz)
        if quiz is None or quiz.quiz_time.start_time is None:
            return JsonResponse({"quiz_time": "not_started"})
        if self.quizHasEnded(quiz, quiz_type) is False:
            return JsonResponse(
                {"quiz_time": "not_ended", "start_time": quiz.quiz_time.start_time}
            )

        match quiz_type:
            case "AcuTest_pic":
                return JsonResponse(AcuTestPicAnswerSerializer(quiz).data)
            case "AcuTest_text":
                # logger.warning(JsonResponse(AcuTestTextAnswerSerializer(quiz).data))
                return JsonResponse(AcuTestTextAnswerSerializer(quiz).data)
            case "ValuTest":
                return JsonResponse(ValuTestAnswerSerializer(quiz).data)
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
