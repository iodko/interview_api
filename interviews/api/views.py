from django_filters.rest_framework import DjangoFilterBackend

from interviews.models import Interviews, UserAnswers
from rest_framework import viewsets, mixins

from interviews.api.serializers import (
    InterviewsSerializer,
    CreateUserAnswerSerializer,
    ListUserAnswersSerializer
)


class InterviewMixin(viewsets.GenericViewSet, mixins.ListModelMixin):
    filter_backends = [DjangoFilterBackend]


class AvailableInterviewSet(InterviewMixin, mixins.RetrieveModelMixin):
    """Выводит список доступных опросов."""
    queryset = Interviews.get_available()
    serializer_class = InterviewsSerializer
    filterset_fields = ['description']


class UserAnswersSerializerSet(InterviewMixin, mixins.CreateModelMixin):
    """
    Выводит список пройденных опросов пользователей. Если в качестве параметра передать
    идентификатор пользователя, список опросов будет отфильтрован по указанному пользователю.
    Сохраняет ответ пользователя.
    """
    queryset = UserAnswers.objects.all()
    http_method_names = ["get", "post"]
    filterset_fields = ['user']

    def get_serializer_class(self):
        if self.action == 'list':
            return ListUserAnswersSerializer
        if self.action == 'create':
            return CreateUserAnswerSerializer
        return ListUserAnswersSerializer
