from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CategoryListView, CustomTokenObtainPairView, QuestionsByCategoryView, GetQuestionView, \
    SubmitAnswerView, UserResultsView, RandomQuestionsView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('questions_by_category/<int:category_id>/', QuestionsByCategoryView.as_view(), name='questions_by_category'),
    path('questions/<int:question_id>/', GetQuestionView.as_view(), name='get_question'),
    path('submit-answer/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('user-results/', UserResultsView.as_view(), name='user_results'),
    path('random-questions/<int:count>/', RandomQuestionsView.as_view(), name='random-questions'),
]
