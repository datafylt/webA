"""
Quick script to check actual configuration values
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.settings.config import settings

print("=" * 60)
print("CURRENT CONFIGURATION VALUES")
print("=" * 60)
print(f"SMTP_HOST: {settings.SMTP_HOST}")
print(f"SMTP_PORT: {settings.SMTP_PORT}")
print(f"SMTP_USER: {settings.SMTP_USER}")
print(f"SMTP_FROM_EMAIL: {settings.SMTP_FROM_EMAIL}")
print(f"SMTP_USE_TLS: {settings.SMTP_USE_TLS}")
print(f"SMTP_USE_SSL: {settings.SMTP_USE_SSL}")
print(f"EMAIL_TEST_MODE: {settings.EMAIL_TEST_MODE}")
print(f"EMAIL_TEST_MODE type: {type(settings.EMAIL_TEST_MODE)}")
print("=" * 60)

if settings.EMAIL_TEST_MODE:
    print("⚠️  WARNING: EMAIL_TEST_MODE is TRUE - emails will be simulated!")
else:
    print("✓ EMAIL_TEST_MODE is FALSE - emails will be sent for real")
