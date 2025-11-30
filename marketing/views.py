from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from .forms import NewsletterForm
from .models import NewsletterSignup


class NewsletterSignupView(View):
    """Handle POST submissions coming from the footer newsletter form."""

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            obj, created = NewsletterSignup.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thanks for subscribing! Check your inbox for updates.")
            else:
                messages.info(request, "You're already on our list. Stay tuned for news!")
        else:
            messages.error(request, "Please enter a valid email address.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("home")))
