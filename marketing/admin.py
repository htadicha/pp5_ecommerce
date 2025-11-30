from django.contrib import admin

from .models import NewsletterSignup


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "consented", "created_at")
    search_fields = ("email",)
    list_filter = ("consented", "created_at")
