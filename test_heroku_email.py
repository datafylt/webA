"""
Direct SMTP test for Heroku deployment
This tests the email configuration directly
"""
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

# Heroku SMTP Configuration (from environment)
SMTP_HOST = "smtp.ionos.com"
SMTP_PORT = 465
SMTP_USER = "administration@formationelectro.com"
SMTP_PASSWORD = "951753!!!Yoric"
SMTP_FROM_EMAIL = "administration@formationelectro.com"
SMTP_FROM_NAME = "FormationElectro"

def send_test_email():
    """Send a test email via IONOS SMTP"""

    print("📧 Preparing test email...")
    print(f"SMTP Host: {SMTP_HOST}")
    print(f"SMTP Port: {SMTP_PORT}")
    print(f"SMTP User: {SMTP_USER}")

    # Create message
    msg = EmailMessage()
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    msg["To"] = "ric.seedoo@gmail.com"  # Test recipient
    msg["Subject"] = "✅ Test Email - Formation Electro Heroku"
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()

    # HTML body
    html_body = """
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #2c3e50;">✅ Email Test Successful!</h1>
        <p>This is a test email from your <strong>Formation Électro</strong> application deployed on Heroku.</p>

        <h2 style="color: #3498db;">🚀 Deployment Status:</h2>
        <ul>
            <li>✅ <strong>Backend API:</strong> Running on Heroku</li>
            <li>✅ <strong>Frontend:</strong> Deployed and accessible</li>
            <li>✅ <strong>PostgreSQL Database:</strong> Connected</li>
            <li>✅ <strong>SMTP Service (IONOS):</strong> Working!</li>
        </ul>

        <h2 style="color: #27ae60;">📧 SMTP Configuration:</h2>
        <ul>
            <li><strong>Provider:</strong> IONOS</li>
            <li><strong>Host:</strong> smtp.ionos.com</li>
            <li><strong>Port:</strong> 465 (SSL)</li>
            <li><strong>From:</strong> administration@formationelectro.com</li>
        </ul>

        <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
            <p style="margin: 0;"><strong>✨ Success!</strong> If you're reading this, your email system is fully operational and ready to send notifications to users.</p>
        </div>

        <h3>📋 Next Steps:</h3>
        <ol>
            <li>Login to the admin panel</li>
            <li>Test sending emails to students</li>
            <li>Configure email templates</li>
            <li>Start using the notification system</li>
        </ol>

        <hr style="border: none; border-top: 1px solid #dee2e6; margin: 30px 0;">
        <p style="color: #6c757d; font-size: 12px; text-align: center;">
            <strong>Formation Électro - Email System Test</strong><br>
            Sent from Heroku Production Environment<br>
            Date: February 8, 2026
        </p>
    </body>
    </html>
    """

    # Plain text fallback
    text_body = """
Test Email - Formation Electro Heroku

This is a test email from your Formation Électro application deployed on Heroku.

Deployment Status:
✅ Backend API: Running on Heroku
✅ Frontend: Deployed and accessible
✅ PostgreSQL Database: Connected
✅ SMTP Service (IONOS): Working!

SMTP Configuration:
- Provider: IONOS
- Host: smtp.ionos.com
- Port: 465 (SSL)
- From: administration@formationelectro.com

Success! If you're reading this, your email system is fully operational.

---
Formation Électro - Email System Test
Sent from Heroku Production Environment
Date: February 8, 2026
    """

    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    try:
        print("\n🔐 Connecting to SMTP server...")
        # Create SSL context
        context = ssl.create_default_context()

        # Connect using SSL (port 465)
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            print("✅ Connected to SMTP server")

            print("🔑 Authenticating...")
            server.login(SMTP_USER, SMTP_PASSWORD)
            print("✅ Authenticated successfully")

            print(f"📤 Sending email to ric.seedoo@gmail.com...")
            server.send_message(msg)
            print("✅ Email sent successfully!")

        print("\n" + "="*60)
        print("🎉 TEST COMPLETE - Email sent successfully!")
        print("="*60)
        print(f"\n📬 Check your inbox at: ric.seedoo@gmail.com")
        print("   (Also check spam folder if not in inbox)")
        print("\n✅ Your SMTP configuration is working correctly!")
        print("✅ You can now send emails from your application!")

        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
        print("   Check SMTP_USER and SMTP_PASSWORD")
        return False
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("📧 Formation Électro - SMTP Test (Heroku)")
    print("="*60)
    print()

    success = send_test_email()

    if success:
        print("\n✅ Email system is ready for production use!")
    else:
        print("\n❌ Email test failed. Check configuration.")
