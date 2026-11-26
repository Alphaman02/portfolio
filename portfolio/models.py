from django.db import models
from django.utils.text import slugify


def split_tags(value):
    return [t.strip() for t in value.split(",") if t.strip()]


class Profile(models.Model):
    """Add one Profile in the admin. The site uses the first one."""
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=120, help_text="e.g. Software Developer")
    intro = models.TextField(help_text="Short introduction for the home page")
    photo = models.ImageField(upload_to="profile/", blank=True)
    about = models.TextField(blank=True)
    cv = models.FileField(upload_to="cv/", blank=True, help_text="PDF version of your CV")
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORIES = [
        ("languages", "Languages"),
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("databases", "Databases"),
        ("tools", "Tools"),
        ("soft", "Soft skills"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=60)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="languages")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=200, blank=True, help_text="Comma separated, e.g. Python, Django, MySQL")
    image = models.ImageField(upload_to="projects/", blank=True)
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tech_list(self):
        return split_tags(self.technologies)

    def __str__(self):
        return self.title


class Education(models.Model):
    qualification = models.CharField(max_length=120)
    institution = models.CharField(max_length=120)
    year = models.CharField(max_length=20, help_text="e.g. 2024 - 2026")

    class Meta:
        ordering = ["-year"]
        verbose_name_plural = "education"

    def __str__(self):
        return f"{self.qualification} - {self.institution}"


class Experience(models.Model):
    position = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    duration = models.CharField(max_length=60, help_text="e.g. 2026 - Present")
    description = models.TextField()
    technologies = models.CharField(max_length=200, blank=True, help_text="Comma separated")
    order = models.PositiveIntegerField(default=0, help_text="Lowest number shows first")

    class Meta:
        ordering = ["order", "-id"]

    def tech_list(self):
        return split_tags(self.technologies)

    def __str__(self):
        return f"{self.position} at {self.company}"


class Certification(models.Model):
    name = models.CharField(max_length=140)
    issuer = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=10, blank=True)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return self.name


class Achievement(models.Model):
    title = models.CharField(max_length=140)
    detail = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Lecturer, Mentor, Employer")
    quote = models.TextField()

    def __str__(self):
        return f"{self.author} ({self.role})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sent"]

    def __str__(self):
        return f"{self.name} - {self.sent:%Y-%m-%d}"


class Module(models.Model):
    """Coursework: a module you studied and what you learned in it."""
    name = models.CharField(max_length=140)
    knowledge = models.CharField(max_length=300)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name
