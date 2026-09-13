from django.urls import path
from .views import InternalDeductPointsView

urlpatterns = [
    path('deduct-points', InternalDeductPointsView.as_view()),
]
