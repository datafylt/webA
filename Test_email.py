import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from dotenv import load_dotenv

load_dotenv()


def main(password):
    SMTP_HOST = "smtp.ionos.com"
    SMTP_PORT = 465  # SMTPS (implicit SSL)

    USERNAME = "administration@formationelectro.com"
    TO_EMAIL = "ric.seedoo@gmail.com"

    FROM_NAME = "Formation Électro"
    SUBJECT = "Test SMTP Python - Formation Électro"
    HTML_BODY = "<h1>Test SMTP</h1><p>Ceci est un test depuis Python.</p>"

    # --- Build message (RFC-friendly) ---
    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{USERNAME}>"
    msg["To"] = TO_EMAIL.strip()  # avoid accidental newline/spaces
    msg["Subject"] = SUBJECT

    # Important for IONOS policy checks:
    msg["Date"] = formatdate(localtime=True)  # RFC 2822 Date
    msg["Message-ID"] = make_msgid()

    msg.set_content("Ceci est un test depuis Python.")  # plain fallback
    msg.add_alternative(HTML_BODY, subtype="html")

    context = ssl.create_default_context()

    print("Envoi en cours...")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=20) as server:
        server.set_debuglevel(1)  # like Java mail.debug=true (optional)
        server.login(USERNAME, password)
        server.send_message(msg)

    print("✅ Email envoyé avec succès!")


if __name__ == "__main__":
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    main(SMTP_PASSWORD)
