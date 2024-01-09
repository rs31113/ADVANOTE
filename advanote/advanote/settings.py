from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_SECRET_KEY=(
        str,
        "django-insecure-f1zq2#vxjbqe8%6c^$rh*s6wk31k6%hnw7$4*g@b99@3qo*4mw",
    ),
    DJANGO_ALLOWED_HOSTS=(list, [".localhost", "127.0.0.1"]),
    DJANGO_STATIC_URL=(str, "/static/"),
    DJANGO_MAIL=(str, "catsshop@yandex.ru"),
    DEFAULT_USER_IS_ACTIVE=(bool, False),
    MAX_AUTH_ATTEMPTS=(int, 3),
)


SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")

LANGUAGE_CODE = "ru"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "six",
    "authorization.apps.AuthorizationConfig",
    "core.apps.CoreConfig",
    "notes.apps.NotesConfig",
    "projects.apps.ProjectsConfig",
    "tag.apps.TagConfig",
    "tasks.apps.TasksConfig",
    "users.apps.UsersConfig",
    "today.apps.TodayConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "advanote.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "notes.context-processors.tasks_count",
                "projects.context_processors.project_count_process",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "advanote.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth"
            ".password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth"
            ".password_validation"
            ".MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth"
            ".password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth"
            ".password_validation"
            ".NumericPasswordValidator"
        ),
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = env("DJANGO_STATIC_URL")

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_MAIL = env("DJANGO_MAIL")

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / "send_mail"

LOGIN_URL = "/"

DEFAULT_USER_IS_ACTIVE = env("DEFAULT_USER_IS_ACTIVE")
if DEFAULT_USER_IS_ACTIVE is None:
    DEFAULT_USER_IS_ACTIVE = DEBUG

MAX_AUTH_ATTEMPTS = env("MAX_AUTH_ATTEMPTS")


AUTHENTICATION_BACKENDS = ("authorization.backends.AuthorizationBackend",)
