from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models import QuerySet, query
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .models import AcuTest, QuizInfo
from .serializers import AcuTestSerializer, QuizInfoSerializer




def startQuiz(request):
    print(timezone.now())
    quiz = QuizInfo.objects.filter(user__username='barbodak').update(start_time=timezone.now() - timedelta(hours=15))
    return HttpResponse(status=200)

class QuizViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def startQuiz(self, request, quiz_id, serializer):
        match quiz_id:
            case "AcuTest":
                QuerySet = AcuTest.objects.all()
                serializer = AcuTestSerializer(QuerySet, many=True)
                if 
                
            case "ValuTest":
    # Create your views here.
