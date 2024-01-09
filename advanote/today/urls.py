from django.urls import path
import today.views


app_name = "today"
urlpatterns = [
    path("", today.views.Today.as_view(), name="today"),
]
