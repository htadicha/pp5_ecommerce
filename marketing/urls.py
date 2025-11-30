from django.urls import path

from .views import NewsletterSignupView


app_name = "marketing"

urlpatterns = [
    path("subscribe/", NewsletterSignupView.as_view(), name="newsletter_subscribe"),
]
