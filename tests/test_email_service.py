"""
Test script to debug email_service
"""
import sys
import os

# Add the webA directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app.services.email_service import email_service

def main():
    print("=" * 60)
    print("Testing Email Service Configuration")
    print("=" * 60)

    print(f"\nSMTP Host: {email_service.smtp_host}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"SMTP User: {email_service.smtp_user}")
    print(f"SMTP From Email: {email_service.smtp_from_email}")
    print(f"SMTP From Name: {email_service.smtp_from_name}")
    print(f"SMTP Use TLS: {email_service.smtp_use_tls}")
    print(f"SMTP Use SSL: {email_service.smtp_use_ssl}")
    print(f"Password Set: {bool(email_service.smtp_password)}")

    print("\n" + "=" * 60)
    print("Testing SMTP Connection")
    print("=" * 60)

    result = email_service.test_connection()
    print(f"\nConnection Result: {result}")

    if not result["success"]:
        print(f"\nERROR: {result.get('error')}")
        return

    print("\n" + "=" * 60)
    print("Sending Test Email")
    print("=" * 60)

    result = email_service.send_email(
        to_email="ric.seedoo@gmail.com",
        subject="Test from Email Service",
        body_html="<h1>Test Email Service</h1><p>Testing the email service directly.</p>"
    )

    print(f"\nSend Result: {result}")

    if result["success"]:
        print("\n✓ Email sent successfully!")
    else:
        print(f"\n✗ Email failed: {result.get('error')}")
        print(f"Error Code: {result.get('error_code')}")

if __name__ == "__main__":
    main()
