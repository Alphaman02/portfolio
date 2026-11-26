from django.core.management.base import BaseCommand

from portfolio.models import Education, Module, Profile, Project, Skill

ABOUT = (
    "I'm a final-year Computer Science student at Tshwane University of Technology. "
    "Most of my projects are built in teams, with the frontend and backend split between collaborators.\n\n"
    "I've deployed applications to a cloud server and connected them to a hosted PostgreSQL database."
)

SKILLS = {
    "languages": ["Java", "TypeScript", "SQL", "PL/SQL", "HTML and CSS", "Python (learning)"],
    "frontend": ["React"],
    "backend": ["Java EE", "Spring Boot", "Django (learning)"],
    "databases": ["PostgreSQL", "Supabase"],
    "tools": ["Git and GitHub", "IntelliJ IDEA", "NetBeans", "GlassFish", "Docker", "Azure", "Linux"],
    "soft": ["Teamwork", "Problem solving", "Communication"],
}

PROJECTS = [
    ("PPE Trading Clearance",
     "A checklist app built for a client and hosted on Azure with HTTPS.",
     "Built for a client. Edit this description in the admin to say what you built and your role.",
     "Azure, HTTPS", "", True),
    ("ExamGuard",
     "A team project with a Spring Boot backend and a React frontend.",
     "Edit this description in the admin to say what the app does and which part you built.",
     "Spring Boot, React", "https://github.com/Alphaman02", True),
    ("ResyApp",
     "A student accommodation app.",
     "Edit this description in the admin to say what the app does and which part you built.",
     "", "", False),
]

MODULES = [
    ("Software Engineering Fundamentals", "Software architecture"),
    ("Database Principles", "SQL and relational database management systems (RDBMS)"),
    ("Object-Oriented Programming", "Object-oriented design and programming"),
    ("Information Security", "Security tools and practice using Kali Linux"),
    ("Operating Systems", "Linux and common command-line commands"),
    ("Database Programming", "PL/SQL"),
]


class Command(BaseCommand):
    help = "Fill the portfolio with starter content. Safe to run more than once."

    def add_arguments(self, parser):
        parser.add_argument("--if-empty", action="store_true",
                            help="Do nothing if a Profile already exists (used on deploy).")

    def handle(self, *args, **options):
        if options["if_empty"] and Profile.objects.exists():
            self.stdout.write("Profile exists, skipping seed.")
            return
        profile = Profile.objects.first() or Profile()
        defaults = {
            "full_name": "Alpha Ndlangamandla",
            "title": "Final-year Computer Science student",
            "intro": "I build full-stack web applications, from the database to the browser.",
            "about": ABOUT,
            "email": "ndlangamandlaalpha@gmail.com",
            "github": "https://github.com/Alphaman02",
            "linkedin": "https://www.linkedin.com/in/alpha-ndlangamandla-00a340404",
            "location": "Pretoria, South Africa",
        }
        for field, value in defaults.items():
            if not getattr(profile, field):
                setattr(profile, field, value)
        profile.save()

        for category, names in SKILLS.items():
            for name in names:
                Skill.objects.get_or_create(name=name, category=category)

        for title, summary, desc, tech, gh, featured in PROJECTS:
            Project.objects.get_or_create(title=title, defaults={
                "summary": summary, "description": desc,
                "technologies": tech, "github_url": gh, "featured": featured,
            })

        Education.objects.get_or_create(
            qualification="Diploma in Computer Science",
            institution="Tshwane University of Technology",
            defaults={"year": "2024 - 2026"},
        )

        for i, (name, knowledge) in enumerate(MODULES, start=1):
            Module.objects.get_or_create(name=name, defaults={"knowledge": knowledge, "order": i})

        self.stdout.write(self.style.SUCCESS("Portfolio filled. Open /admin/ to edit anything."))
