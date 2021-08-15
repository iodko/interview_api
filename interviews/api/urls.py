from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interviews.api.views import (
    AvailableInterviewSet,
    UserAnswersSerializerSet
)

router_v1 = DefaultRouter()

router_v1.register('available-interviews', AvailableInterviewSet, 'available_interviews')
router_v1.register('user-answers', UserAnswersSerializerSet, 'user_answers')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
