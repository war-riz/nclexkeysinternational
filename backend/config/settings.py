"""
Updated settings.py for production deployment - FIXED VERSION
"""

from pathlib import Path
import os
import dj_database_url
from datetime import timedelta
from dotenv import load_dotenv
from celery.schedules import crontab
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decimal import Decimal

# Load .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ALLOWED_HOSTS for production
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'api.nclex.com',
    'nclex-backend.onrender.com',
    '0.0.0.0',
    'nclex-beryl.vercel.app',
]

# Allow .ngrok-free.app domains for testing
if DEBUG:
    ALLOWED_HOSTS.extend(['.ngrok-free.app'])

# Add Render hostname if available
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

# Fixed CORS Settings for production
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://nclex-beryl.vercel.app",
]

# Only allow all origins in development
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# For development, allow any local network IP
if DEBUG:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://192\.168\.\d+\.\d+:\d+$",
        r"^http://10\.\d+\.\d+\.\d+:\d+$",
        r"^http://172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+:\d+$",
        r"^http://localhost:\d+$",
        r"^http://127\.0\.0\.1:\d+$",
    ]

# Fixed Security Settings for Production
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'true').lower() == 'true'
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0

# Fixed Celery Configuration - Use environment variables properly
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'memory://')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
CELERY_TIMEZONE = 'UTC'

# Payment Gateway Settings
PAYMENT_GATEWAYS = {
    'paystack': {
        'public_key': os.getenv('PAYSTACK_PUBLIC_KEY'),
        'secret_key': os.getenv('PAYSTACK_SECRET_KEY'),
        'base_url': 'https://api.paystack.co',
        'webhook_secret': os.getenv('PAYSTACK_WEBHOOK_SECRET'),
        'subaccount_code': os.getenv('PAYSTACK_SUBACCOUNT_CODE', ''),
        'split_code': os.getenv('PAYSTACK_SPLIT_CODE', ''),
    },
    'flutterwave': {
        'public_key': os.getenv('FLUTTERWAVE_PUBLIC_KEY'),
        'secret_key': os.getenv('FLUTTERWAVE_SECRET_KEY'),
        'base_url': 'https://api.flutterwave.com/v3',
        'webhook_secret': os.getenv('FLUTTERWAVE_WEBHOOK_SECRET'),
        'encryption_key': os.getenv('FLUTTERWAVE_ENCRYPTION_KEY'),
    }
}

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

# Payment configuration
PAYMENT_SETTINGS = {
    'MAX_PAYMENT_ATTEMPTS_PER_HOUR': 5,
    'PAYMENT_EXPIRY_MINUTES': 30,
    'MIN_COURSE_PRICE': Decimal('500.00'),
    'MAX_COURSE_PRICE': Decimal('500000.00'),
    'AUTO_REFUND_THRESHOLD': Decimal('50000.00'),
    'INSTRUCTOR_REVENUE_SHARE': Decimal('0.70'),
    'PLATFORM_REVENUE_SHARE': Decimal('0.30'),
}

# Payment Settings
DEFAULT_CURRENCY = 'NGN'
SUPPORTED_CURRENCIES = ['NGN', 'USD', 'GHS', 'KES']
DEFAULT_PAYMENT_GATEWAY = 'paystack'
SITE_URL = os.getenv('SITE_URL', 'https://nclex-beryl.vercel.app')

# Bank Account Information
BANK_ACCOUNT_NUMBER = os.getenv('BANK_ACCOUNT_NUMBER')
BANK_NAME = os.getenv('BANK_NAME')
BANK_ACCOUNT_NAME = os.getenv('BANK_ACCOUNT_NAME')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'django_celery_beat',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    # Your apps
    'users',
    'courses',
    'progress',
    'chats',
    'payments',
    'adminpanel',
    'messaging',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'common.middleware.SecurityHeadersMiddleware',  
    'common.middleware.RequestLoggingMiddleware',
    'common.middleware.UserActivityMiddleware', 
    'common.middleware.SuspiciousActivityMiddleware', 
    'common.course_middleware.PaymentSecurityMiddleware',
    'common.middleware.ErrorHandlingMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - Supabase PostgreSQL
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME = 60  # minutes
JWT_REFRESH_TOKEN_LIFETIME = 7   # days

# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'NCLEX <noreply@nclex.com>')

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://nclex-beryl.vercel.app")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Cache Configuration - Use Redis in production, memory for development
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
else:
    # Use Redis for production caching if available
    REDIS_URL = os.getenv('REDIS_URL')
    if REDIS_URL:
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                }
            }
        }
    else:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }

# Session Settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'common.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# Fixed Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Create staticfiles directory if it doesn't exist
STATICFILES_DIRS = []
os.makedirs(STATIC_ROOT, exist_ok=True)

# Use WhiteNoise for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration for Cloudinary
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Use Cloudinary for media storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Media URL and Root (Cloudinary handles this)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging Configuration for Production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rate Limiting Settings
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    # ============= PAYMENT TASKS =============
    
    # Run monthly payout calculation on 1st of every month at 2 AM
    'create-monthly-payouts': {
        'task': 'payments.tasks.create_monthly_payouts_task',
        'schedule': crontab(hour=2, minute=0, day_of_month=1),
    },
    
    # Auto-process small payouts daily at 10 AM
    'auto-process-payouts': {
        'task': 'payments.tasks.process_auto_payouts',
        'schedule': crontab(hour=10, minute=0),
    },
    
    'process-monthly-payouts': {
        'task': 'payments.tasks.process_monthly_payouts',
        'schedule': crontab(day_of_month=1, hour=2, minute=0),  # 1st of every month at 2 AM
    },
    
    'cleanup-expired-payments': {
        'task': 'payments.tasks.cleanup_expired_payments',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    
    'verify-bank-transfers': {
        'task': 'payments.tasks.verify_pending_bank_transfers',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    
    # Payout reminder notifications
    'send-payout-reminders': {
        'task': 'payments.tasks.send_payout_reminders',
        'schedule': crontab(hour=10, minute=0, day_of_month=25),  # 25th of month at 10 AM
    },

    # ============= USER MANAGEMENT TASKS =============
    
    'cleanup-old-records': {
        'task': 'management.tasks.cleanup_old_records',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
    
    'cleanup-expired-tokens': {
        'task': 'management.tasks.cleanup_expired_tokens',
        'schedule': crontab(minute=0, hour='*/6'),  # Run every 6 hours
    },
    
    'process-scheduled-deletions': {
        'task': 'management.tasks.process_scheduled_deletions',
        'schedule': crontab(hour=3, minute=0),  # Run daily at 3 AM
    },
    
    'cleanup-inactive-sessions': {
        'task': 'management.tasks.cleanup_inactive_sessions',
        'schedule': crontab(minute=0, hour='*/12'),  # Run every 12 hours
    },
    
    'cleanup-old-login-attempts': {
        'task': 'management.tasks.cleanup_old_login_attempts',
        'schedule': crontab(hour=4, minute=0, day_of_week=0),  # Run weekly on Sunday
    },
    
    'cleanup-old-email-logs': {
        'task': 'management.tasks.cleanup_old_email_logs',
        'schedule': crontab(hour=5, minute=0, day_of_month=1),  # Run monthly
    },
    
    'send-deletion-reminders': {
        'task': 'management.tasks.send_deletion_reminders',
        'schedule': crontab(hour=10, minute=0),  # Run daily at 10 AM
    },

    # ============= SYSTEM MONITORING TASKS =============
    
    'database-health-check': {
        'task': 'management.tasks.database_health_check',
        'schedule': crontab(hour=1, minute=0),  # Run daily at 1 AM
    },
    
    # System health alerts (more frequent)
    'system-health-check': {
        'task': 'management.tasks.comprehensive_health_check',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    
    # Weekly admin report
    'send-weekly-admin-report': {
        'task': 'management.tasks.send_weekly_admin_report',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Monday at 8 AM
    },

    # ============= INSTRUCTOR & ANALYTICS TASKS =============
    
    # Monthly instructor analytics
    'send-monthly-instructor-analytics': {
        'task': 'management.tasks.send_monthly_instructor_analytics',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),  # 1st of month at 9 AM
    },
    
    # Monthly revenue report for admins
    'generate-monthly-revenue-report': {
        'task': 'analytics.tasks.generate_monthly_revenue_report',
        'schedule': crontab(hour=7, minute=0, day_of_month=1),  # 1st of month at 7 AM
    },
    
    # Track instructor engagement daily
    'track-instructor-engagement': {
        'task': 'analytics.tasks.track_instructor_engagement',
        'schedule': crontab(hour=23, minute=0),  # Daily at 11 PM
    },

    # ============= COURSE & STUDENT TASKS =============
    
    # Student progress reminders
    'send-progress-reminders': {
        'task': 'courses.tasks.send_progress_reminders',
        'schedule': crontab(hour=14, minute=0, day_of_week=3),  # Wednesday at 2 PM
    },
    
    # Course completion follow-ups
    'send-course-completion-followups': {
        'task': 'courses.tasks.send_completion_followups',
        'schedule': crontab(hour=16, minute=0, day_of_week=5),  # Friday at 4 PM
    },
    
    # Inactive student re-engagement
    'reengage-inactive-students': {
        'task': 'courses.tasks.reengage_inactive_students',
        'schedule': crontab(hour=11, minute=0, day_of_week=2),  # Tuesday at 11 AM
    },

    # ============= EXAM & CERTIFICATE TASKS =============
    
    # Certificate expiry warnings
    'check-certificate-expiry': {
        'task': 'exams.tasks.check_certificate_expiry_warnings',
        'schedule': crontab(hour=8, minute=0, day_of_month=15),  # 15th of month at 8 AM
    },
    
    # Exam attempt cleanup (old incomplete attempts)
    'cleanup-old-exam-attempts': {
        'task': 'exams.tasks.cleanup_old_exam_attempts',
        'schedule': crontab(hour=2, minute=30, day_of_week=0),  # Sunday at 2:30 AM
    },

    # ============= SECURITY TASKS =============
    
    # Fraud detection scan
    'fraud-detection-scan': {
        'task': 'security.tasks.run_fraud_detection_scan',
        'schedule': crontab(hour=3, minute=30),  # Daily at 3:30 AM
    },
    
    # Suspicious activity monitoring
    'monitor-suspicious-activity': {
        'task': 'security.tasks.monitor_suspicious_activity',
        'schedule': crontab(minute='*/20'),  # Every 20 minutes
    },
    
    # IP reputation check
    'check-ip-reputation': {
        'task': 'security.tasks.check_ip_reputation',
        'schedule': crontab(hour=4, minute=0),  # Daily at 4 AM
    },

    # ============= BACKUP & MAINTENANCE TASKS =============
    
    # Weekly backup verification
    'verify-backups': {
        'task': 'management.tasks.verify_system_backups',
        'schedule': crontab(hour=6, minute=0, day_of_week=0),  # Sunday at 6 AM
    },
    
    # Monthly maintenance report
    'monthly-maintenance-report': {
        'task': 'management.tasks.generate_maintenance_report',
        'schedule': crontab(hour=5, minute=0, day_of_month=1),  # 1st of month at 5 AM
    },
    
    # Database optimization (weekly)
    'optimize-database': {
        'task': 'management.tasks.optimize_database',
        'schedule': crontab(hour=1, minute=30, day_of_week=0),  # Sunday at 1:30 AM
    },

    # ============= NOTIFICATION TASKS =============
    
    # Send bulk notifications (process queue)
    'process-notification-queue': {
        'task': 'notifications.tasks.process_notification_queue',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes
    },
    
    # Clean up old notifications
    'cleanup-old-notifications': {
        'task': 'notifications.tasks.cleanup_old_notifications',
        'schedule': crontab(hour=3, minute=45, day_of_week=1),  # Monday at 3:45 AM
    },

    # ============= MARKETING & ENGAGEMENT TASKS =============
    
    # Send welcome series to new users
    'send-welcome-series': {
        'task': 'marketing.tasks.send_welcome_email_series',
        'schedule': crontab(hour=9, minute=30),  # Daily at 9:30 AM
    },
    
    # Course recommendation engine
    'generate-course-recommendations': {
        'task': 'recommendations.tasks.generate_course_recommendations',
        'schedule': crontab(hour=12, minute=0, day_of_week=1),  # Monday at noon
    },
    
    # Abandoned cart recovery
    'recover-abandoned-enrollments': {
        'task': 'marketing.tasks.recover_abandoned_enrollments',
        'schedule': crontab(hour=15, minute=0),  # Daily at 3 PM
    },

    # ============= CONTENT MODERATION TASKS =============
    
    # Auto-moderate course content
    'auto-moderate-content': {
        'task': 'moderation.tasks.auto_moderate_content',
        'schedule': crontab(minute='*/45'),  # Every 45 minutes
    },
    
    # Review flagged content
    'review-flagged-content': {
        'task': 'moderation.tasks.review_flagged_content',
        'schedule': crontab(hour=8, minute=15, day_of_week='1-5'),  # Weekdays at 8:15 AM
    },

    # ============= PERFORMANCE MONITORING =============
    
    # Monitor API performance
    'monitor-api-performance': {
        'task': 'monitoring.tasks.monitor_api_performance',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    
    # Generate performance reports
    'generate-performance-reports': {
        'task': 'monitoring.tasks.generate_performance_reports',
        'schedule': crontab(hour=6, minute=30, day_of_week=1),  # Monday at 6:30 AM
    },
}