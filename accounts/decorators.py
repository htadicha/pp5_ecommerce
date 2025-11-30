"""
Custom decorators for role-based access control.
"""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    """
    Allow access only to staff or admin-level users.

    Redirects authenticated users without sufficient privileges back to the
    dashboard and anonymous users to the login page.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if not any(
            [
                getattr(request.user, "is_staff", False),
                getattr(request.user, "is_admin", False),
                getattr(request.user, "is_superadmin", False),
            ]
        ):
            messages.error(request, "You do not have permission to access that page.")
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
