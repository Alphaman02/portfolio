from django.conf import settings

from .models import Education, Experience, Module, Profile


def site(request):
    """Make the profile and nav flags available to every template."""
    return {
        "profile": Profile.objects.first(),
        # drop a file named cv.pdf into the static folder and it becomes the CV link
        "static_cv": (settings.BASE_DIR / "static" / "cv.pdf").exists(),
        "nav": {
            "experience": Experience.objects.exists(),
            "education": Education.objects.exists() or Module.objects.exists(),
        },
    }
