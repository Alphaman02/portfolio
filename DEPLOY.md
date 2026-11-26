# Deploy to Render

**Build command:** `bash build.sh`
**Start command:** `gunicorn config.wsgi:application`
**Environment variables:** PYTHON_VERSION=3.12.8, SECRET_KEY, DATABASE_URL,
DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
(optional: CLOUDINARY_URL for uploaded images, ALLOWED_HOSTS for a custom domain)

Put your CV at `static/cv.pdf` and commit it to show a Download Resume button
without using Cloudinary.
