from django.urls import path

from library.views.users import (
    UserListCreateGenericView,
)

urlpatterns = [
    path('', UserListCreateGenericView.as_view()),
]