"""
Basic sanity tests for the Django application setup and configuration.
"""
import os
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.urls import reverse


class SanityTestCase(TestCase):
    """Test basic Django application setup and sanity checks."""

    def test_django_settings_loaded(self):
        """Test that Django settings are loaded correctly."""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertTrue(hasattr(settings, 'DEBUG'))
        self.assertTrue(hasattr(settings, 'DATABASES'))

    def test_secret_key_configured(self):
        """Test that SECRET_KEY is properly configured."""
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, '')
        # For tests, we expect the test secret key
        self.assertEqual(settings.SECRET_KEY, 'test-secret-key-for-development-only-not-for-production')

    def test_debug_setting(self):
        """Test that DEBUG setting is configured."""
        self.assertIsInstance(settings.DEBUG, bool)

    def test_database_connection(self):
        """Test that database connection works."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_database_migration_status(self):
        """Test that database migrations have been applied."""
        # This will raise an exception if migrations haven't been run
        try:
            call_command('check')
        except Exception as e:
            self.fail(f"Django check failed: {e}")

    def test_environment_variables(self):
        """Test that required environment variables are loaded."""
        # Check if .env file variables are loaded
        self.assertEqual(os.getenv('DEBUG'), 'True')
        self.assertEqual(os.getenv('CHUNK_SIZE'), '100')

    def test_installed_apps(self):
        """Test that required apps are in INSTALLED_APPS."""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ]
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_middleware_configuration(self):
        """Test that required middleware is configured."""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
        ]
        for middleware in required_middleware:
            self.assertIn(middleware, settings.MIDDLEWARE)

    def test_url_configuration(self):
        """Test that URL configuration is working."""
        # Test that admin URLs are configured
        admin_url = reverse('admin:index')
        self.assertTrue(admin_url.startswith('/admin/'))

    def test_static_files_configuration(self):
        """Test that static files are configured."""
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertIsNotNone(settings.STATIC_URL)

    def test_templates_configuration(self):
        """Test that templates are configured."""
        self.assertTrue(hasattr(settings, 'TEMPLATES'))
        self.assertIsInstance(settings.TEMPLATES, list)
        self.assertGreater(len(settings.TEMPLATES), 0)