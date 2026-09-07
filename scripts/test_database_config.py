"""Run with python -m unittest discover -s scripts -p test_database_config.py."""
import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch
from django.core.exceptions import ImproperlyConfigured

SETTINGS = Path(__file__).resolve().parents[1] / 'control_asistencia/settings.py'


class DatabaseConfigTests(unittest.TestCase):
    def config(self, url):
        with patch.dict(os.environ, {'DATABASE_URL': url}, clear=True), patch('dotenv.load_dotenv'):
            return runpy.run_path(str(SETTINGS))['DATABASES']['default']

    def test_missing_url_fails(self):
        with self.assertRaisesMessage(ImproperlyConfigured, 'Falta DATABASE_URL'):
            self.config('')

    def test_sqlite_rejected(self):
        with self.assertRaises(ImproperlyConfigured):
            self.config('sqlite:///db.sqlite3')

    def test_invalid_url_hides_credentials(self):
        with self.assertRaises(ImproperlyConfigured) as error:
            self.config('unknown://user:secret@example.invalid/db')
        self.assertNotIn('secret', str(error.exception))

    def test_incomplete_postgres_rejected(self):
        with self.assertRaises(ImproperlyConfigured):
            self.config('postgresql://example.invalid/db')

    def test_encoded_password_ssl_and_pooler(self):
        config = self.config('postgresql://user:test%40value@example.invalid:5432/postgres')
        self.assertEqual(config['PASSWORD'], 'test@value')
        self.assertEqual(config['ENGINE'], 'django.db.backends.postgresql')
        self.assertEqual(config['OPTIONS']['sslmode'], 'require')
        self.assertEqual(config['OPTIONS']['connect_timeout'], 10)
        self.assertTrue(config['DISABLE_SERVER_SIDE_CURSORS'])

    def assertRaisesMessage(self, exception, message):
        return self.assertRaisesRegex(exception, message)
