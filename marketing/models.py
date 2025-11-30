from django.db import models


class NewsletterSignup(models.Model):
    """Store newsletter opt-ins captured from the marketing form."""

    email = models.EmailField(unique=True)
    consented = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
