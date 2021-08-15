from django.contrib import admin

from interviews.models import Interviews, AnswerType, Questions, AnswerOptions

admin.site.register(AnswerType)


class AnswersInline(admin.TabularInline):
    model = AnswerOptions
    extra = 1


@admin.register(Interviews)
class InterviewsAdmin(admin.ModelAdmin):
    list_display = ('description', 'started_at', 'expired_at')
    filter_horizontal = ['questions']


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (AnswersInline,)

