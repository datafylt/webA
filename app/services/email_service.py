"""
Email Service - SMTP Integration for Formation Électro
Supports multiple providers: Gmail, Outlook, SendGrid, custom SMTP
"""

import smtplib
import ssl
import logging
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.settings.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service d'envoi d'emails via SMTP
    """

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from_email = settings.SMTP_FROM_EMAIL
        self.smtp_from_name = settings.SMTP_FROM_NAME
        self.smtp_use_tls = settings.SMTP_USE_TLS
        self.smtp_use_ssl = settings.SMTP_USE_SSL

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        body_text: Optional[str] = None,
        to_name: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Envoyer un email
        """
        try:
            logger.info(f"Attempting to send email to {to_email} with subject: {subject}")
            logger.debug(f"SMTP Config - Host: {self.smtp_host}, Port: {self.smtp_port}, User: {self.smtp_user}")

            # Créer le message avec EmailMessage (RFC-friendly)
            msg = EmailMessage()

            # Headers - exactly like Test_email.py
            from_header = (
                f"{self.smtp_from_name} <{self.smtp_from_email}>" if self.smtp_from_name else self.smtp_from_email
            )

            msg["From"] = from_header
            msg["To"] = to_email.strip()
            msg["Subject"] = subject

            # Headers importants pour IONOS - exactly like Test_email.py
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid()

            if reply_to:
                msg["Reply-To"] = reply_to

            if cc:
                msg["Cc"] = ", ".join(cc)

            if bcc:
                # BCC ne doit pas apparaître dans les headers
                pass

            # Corps texte brut
            if not body_text:
                import re

                body_text = re.sub(r"<[^>]+>", "", body_html)
                body_text = body_text.replace("&nbsp;", " ")
                body_text = re.sub(r"\s+", " ", body_text).strip()

            # Ajouter le contenu - exactly like Test_email.py
            msg.set_content(body_text)
            msg.add_alternative(body_html, subtype="html")

            # Envoi avec SSL - exactly like Test_email.py
            context = ssl.create_default_context()

            logger.debug(f"Connecting to SMTP server {self.smtp_host}:{self.smtp_port}")
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=20) as server:
                logger.debug("Logging in to SMTP server")
                server.login(self.smtp_user, self.smtp_password)
                logger.debug("Sending message")
                server.send_message(msg)

            message_id = msg["Message-ID"]
            logger.info(f"✓ Email sent successfully to {to_email}: {subject} (Message-ID: {message_id})")

            return {
                "success": True,
                "message_id": message_id,
                "sent_at": datetime.now().isoformat(),
                "recipient": to_email,
            }

        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"SMTP Authentication error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": "Erreur d'authentification SMTP. Vérifiez vos identifiants.",
                "error_details": str(e),
                "error_code": "AUTH_ERROR",
            }
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"Recipients refused: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": f"Adresse email refusée: {to_email}",
                "error_details": str(e),
                "error_code": "RECIPIENT_REFUSED",
            }
        except smtplib.SMTPException as e:
            error_msg = f"SMTP error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": f"Erreur SMTP: {str(e)}",
                "error_details": str(e),
                "error_code": "SMTP_ERROR",
            }
        except Exception as e:
            error_msg = f"Email send error: {str(e)}"
            logger.error(error_msg)
            logger.exception("Full traceback:")
            return {"success": False, "error": str(e), "error_details": str(e), "error_code": "UNKNOWN_ERROR"}

    def send_bulk_emails(
        self,
        recipients: List[Dict[str, str]],
        subject: str,
        body_html: str,
        variables: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Envoyer des emails en masse avec personnalisation
        """
        results = []
        sent_count = 0
        failed_count = 0

        for recipient in recipients:
            # Personnaliser le contenu
            personalized_subject = subject
            personalized_body = body_html

            # Remplacer les variables du destinataire
            for key, value in recipient.items():
                placeholder = f"{{{key}}}"
                personalized_subject = personalized_subject.replace(placeholder, str(value or ""))
                personalized_body = personalized_body.replace(placeholder, str(value or ""))

            # Remplacer les variables globales
            if variables:
                for key, value in variables.items():
                    placeholder = f"{{{key}}}"
                    personalized_subject = personalized_subject.replace(placeholder, str(value or ""))
                    personalized_body = personalized_body.replace(placeholder, str(value or ""))

            # Envoyer
            result = self.send_email(
                to_email=recipient["email"],
                to_name=recipient.get("name"),
                subject=personalized_subject,
                body_html=personalized_body,
            )

            result["recipient"] = recipient["email"]
            results.append(result)

            if result["success"]:
                sent_count += 1
            else:
                failed_count += 1

        return {
            "sent_count": sent_count,
            "failed_count": failed_count,
            "total": len(recipients),
            "results": results,
        }

    def test_connection(self) -> Dict[str, Any]:
        """Tester la connexion SMTP"""
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=20) as server:
                server.login(self.smtp_user, self.smtp_password)
            return {
                "success": True,
                "message": "Connexion SMTP réussie",
                "host": self.smtp_host,
                "port": self.smtp_port,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "host": self.smtp_host,
                "port": self.smtp_port,
            }


# Instance singleton
email_service = EmailService()
