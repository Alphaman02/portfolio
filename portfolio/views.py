from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import (Achievement, Certification, Education, Experience,
                     Module, Profile, Project, Skill, Testimonial)


def skill_groups():
    groups = []
    for key, label in Skill.CATEGORIES:
        names = list(Skill.objects.filter(category=key))
        if names:
            groups.append({"label": label, "skills": names})
    return groups


def home(request):
    profile = Profile.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            if profile:
                send_mail(
                    f"Portfolio message from {msg.name}",
                    f"{msg.message}\n\nReply to: {msg.email}",
                    None,
                    [profile.email],
                    fail_silently=True,
                )
            messages.success(request, "Thanks, your message was sent.")
            return redirect("/#contact")
    else:
        form = ContactForm()

    context = {
        "profile": profile,
        "skill_groups": skill_groups(),
        "projects": Project.objects.all(),
        "education": Education.objects.all(),
        "modules": Module.objects.all(),
        "experience": Experience.objects.all(),
        "certifications": Certification.objects.all(),
        "achievements": Achievement.objects.all(),
        "testimonials": Testimonial.objects.all(),
        "form": form,
    }
    return render(request, "portfolio/home.html", context)


def project_detail(request, slug):
    return render(request, "portfolio/project_detail.html", {
        "profile": Profile.objects.first(),
        "project": get_object_or_404(Project, slug=slug),
    })
