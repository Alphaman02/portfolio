from django.contrib import admin

from .models import (Achievement, Certification, ContactMessage, Education,
                     Experience, Module, Profile, Project, Skill, Testimonial)

admin.site.site_header = "Portfolio admin"

admin.site.register([Profile, Module, Education, Certification, Achievement, Testimonial])


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "duration", "order")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "technologies", "created")
    list_filter = ("featured",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "sent")
    readonly_fields = ("name", "email", "message", "sent")
