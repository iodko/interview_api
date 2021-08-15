from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AnswerType(models.Model):
    """Хранит типы ответов."""

    name = models.CharField(max_length=50, verbose_name="Наименование типа")
    is_single_answer = models.BooleanField(default=True)
    is_text_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Тип ответа"
        verbose_name_plural = "Типы ответов"

    def __str__(self):
        return self.name


class Questions(models.Model):
    """Хранит вопросы."""

    text = models.CharField(max_length=250, verbose_name="Текст вопроса")
    answer_type = models.ForeignKey(
        AnswerType, on_delete=models.PROTECT, verbose_name="Тип ответа"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text

    @property
    def is_single_answer(self):
        return self.answer_type.is_single_answer

    @property
    def is_text_answer(self):
        return self.answer_type.is_text_answer


class AnswerOptions(models.Model):
    """Хранит варианты ответов."""

    text = models.CharField(max_length=100, verbose_name="Текст ответа")
    question = models.ForeignKey(
        Questions,
        on_delete=models.PROTECT,
        related_name="answers",
        verbose_name="Вопрос",
    )

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return f"Ответ: {self.text}"


class Interviews(models.Model):
    """Хранит опросы."""

    description = models.CharField(max_length=250, verbose_name="Описание опроса")
    started_at = models.DateField(auto_now_add=True, verbose_name="Дата старта")
    expired_at = models.DateField(verbose_name="Дата окончания")
    questions = models.ManyToManyField(Questions, verbose_name="Вопросы")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.description

    @staticmethod
    def get_available():
        """Получение активных опросов."""
        today = timezone.now().date()
        available_interview = Interviews.objects.filter(expired_at__gte=today)
        return available_interview


class UserAnswers(models.Model):
    """Хранит ответы пользователя."""

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Пользователь"
    )
    user_answer = models.CharField(
        max_length=1000, blank=True, verbose_name="Ответ пользователя"
    )
    choice_answer = models.ManyToManyField(
        AnswerOptions, blank=True, verbose_name="Выбранный ответ"
    )
    interview = models.ForeignKey(
        Interviews,
        related_name="user_answers",
        on_delete=models.PROTECT,
        verbose_name="Опрос",
    )
    questions = models.ForeignKey(
        Questions,
        related_name="user_answers",
        on_delete=models.PROTECT,
        verbose_name="Заданный вопрос",
    )

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"

    def __str__(self):
        return f"{self.questions.text}"
