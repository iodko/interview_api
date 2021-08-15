from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from interviews.models import Interviews, Questions, AnswerOptions, UserAnswers

User = get_user_model()


class AnswerOptionsSerializer(serializers.ModelSerializer):
    """Сериализация вариантов ответов."""

    class Meta:
        model = AnswerOptions
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    """Сериализация вопросы."""

    answers = AnswerOptionsSerializer(read_only=True, many=True)

    class Meta:
        model = Questions
        fields = [
            'id',
            'text',
            'answers'
        ]


class InterviewsSerializer(serializers.ModelSerializer):
    """Сериализация опросы."""
    questions = QuestionsSerializer(read_only=True, many=True)

    class Meta:
        model = Interviews
        fields = ['id', 'description', 'questions', 'expired_at']


class CreateUserAnswerSerializer(serializers.ModelSerializer):
    """Сериализация ответа пользователя и выполнение проверки."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAnswers
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            try:
                data['user'] = get_object_or_404(User, pk=self.initial_data.get('user'))
            except Http404 as e:
                raise ValidationError(code=404, detail='Не удалось найти пользователя')

        data = super().validate(data)
        user_answer = data.get('user_answer')
        choice_answer = data.get('choice_answer')
        current_question = data.get('questions')
        if not user_answer and not choice_answer:
            raise ValidationError(code=400, detail='Не передан ответ')
        if not choice_answer and not current_question.is_text_answer:
            raise ValidationError(code=400, detail='Вы не ответили на вопрос')
        if current_question.is_single_answer and len(choice_answer) > 1:
            raise ValidationError(code=400, detail='Для этого вопроса можно выбрать только один ответ')
        if current_question.is_text_answer and not user_answer:
            raise ValidationError(code=400, detail='Пожалуйста напишите свой ответ')
        return data


class ListUserAnswersSerializer(serializers.ModelSerializer):
    """Сериализация ответы пользователя."""

    user_answer = serializers.StringRelatedField()
    choice_answer = AnswerOptionsSerializer(read_only=True, many=True)
    questions = serializers.SlugRelatedField(read_only=True, slug_field='text')
    interview = serializers.SlugRelatedField(read_only=True, slug_field='description')

    class Meta:
        model = UserAnswers
        fields = '__all__'
