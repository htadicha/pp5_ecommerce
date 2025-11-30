from django import forms

from .models import NewsletterSignup


class NewsletterForm(forms.ModelForm):
    """Simple email capture form for newsletter opt-ins."""

    class Meta:
        model = NewsletterSignup
        fields = ["email", "consented"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email",
                    "class": "form-control",
                    "aria-label": "Newsletter email",
                }
            ),
        }
        labels = {
            "email": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["consented"].widget = forms.HiddenInput()
        self.fields["consented"].initial = True
