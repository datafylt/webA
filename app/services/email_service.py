"""
Email Service - SMTP Integration for Formation Électro
Supports multiple providers: Gmail, Outlook, SendGrid, custom SMTP
"""

import smtplib
import ssl
import logging
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path

from app.settings.config import settings

# Configuration logging détaillé
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

    def _create_connection(self):
        try:
            # éviter config incohérente
            if self.smtp_use_ssl and self.smtp_use_tls:
                raise ValueError(
                    "Config SMTP invalide: SMTP_USE_SSL et SMTP_USE_TLS ne peuvent pas être True en même temps")

            if self.smtp_use_ssl:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=30)
                server.ehlo()
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30)
                server.ehlo()
                if self.smtp_use_tls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    server.ehlo()

            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            logger.warning(
                f"SMTP CONFIG => host={self.smtp_host} port={self.smtp_port} "
                f"use_ssl={self.smtp_use_ssl} use_tls={self.smtp_use_tls} user={self.smtp_user}"
            )
            return server
        except Exception as e:
            logger.error(f"SMTP connection error: {e}")
            raise

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
            logger.debug(f"=== SENDING EMAIL ===")
            logger.debug(f"To: {to_email} ({to_name})")
            logger.debug(f"Subject: {subject}")
            logger.debug(f"Body length: {len(body_html)} chars")
            
            # Créer le message avec EmailMessage (RFC-friendly)
            msg = EmailMessage()
            
            # Headers
            from_header = f"{self.smtp_from_name} <{self.smtp_from_email}>" if self.smtp_from_name else self.smtp_from_email
            
            msg["From"] = from_header
            msg["To"] = to_email.strip()
            msg["Subject"] = subject
            
            # Headers importants pour IONOS
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain="formationelectro.com")
            
            if reply_to:
                msg["Reply-To"] = reply_to
            
            if cc:
                msg["Cc"] = ', '.join(cc)
            
            # Corps texte brut
            if not body_text:
                import re
                body_text = re.sub(r'<[^>]+>', '', body_html)
                body_text = body_text.replace('&nbsp;', ' ')
                body_text = re.sub(r'\s+', ' ', body_text).strip()
            
            # Ajouter le contenu
            msg.set_content(body_text)
            msg.add_alternative(body_html, subtype="html")
            
            # Liste des destinataires pour BCC
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            # Envoi avec SSL
            logger.debug(f"Creating SMTP connection...")
            context = ssl.create_default_context()
            
            logger.debug(f"=== SMTP CONNECTION DEBUG ===")
            logger.debug(f"Host: {self.smtp_host}")
            logger.debug(f"Port: {self.smtp_port}")
            logger.debug(f"User: {self.smtp_user}")
            logger.debug(f"Password set: {bool(self.smtp_password)}")
            logger.debug(f"Password length: {len(self.smtp_password) if self.smtp_password else 0}")
            logger.debug(f"Use SSL: {self.smtp_use_ssl}")
            
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=20) as server:
                server.set_debuglevel(1)
                logger.debug(f"Logging in as {self.smtp_user}...")
                server.login(self.smtp_user, self.smtp_password)
                logger.debug("Login successful!")
                logger.debug(f"Sending from {self.smtp_from_email} to {recipients}")
                server.send_message(msg)
                logger.debug("send_message() completed successfully")
            
            message_id = msg["Message-ID"]
            logger.info(f"Email sent successfully to {to_email}: {subject}")
            
            return {
                "success": True,
                "message_id": message_id,
                "sent_at": datetime.now().isoformat(),
                "recipient": to_email,
            }
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication error: {e}")
            return {
                "success": False,
                "error": "Erreur d'authentification SMTP. Vérifiez vos identifiants.",
                "error_code": "AUTH_ERROR"
            }
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"Recipients refused: {e}")
            return {
                "success": False,
                "error": f"Adresse email refusée: {to_email}",
                "error_code": "RECIPIENT_REFUSED"
            }
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return {
                "success": False,
                "error": f"Erreur SMTP: {str(e)}",
                "error_code": "SMTP_ERROR"
            }
        except Exception as e:
            logger.error(f"Email send error: {e}")
            logger.exception("Full traceback:")
            return {
                "success": False,
                "error": str(e),
                "error_code": "UNKNOWN_ERROR"
            }
    
    def send_bulk_emails(
        self,
        recipients: List[Dict[str, str]],
        subject: str,
        body_html: str,
        variables: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Envoyer des emails en masse avec personnalisation
        
        Args:
            recipients: Liste de {"email": "", "name": "", ...variables}
            subject: Sujet (peut contenir {variables})
            body_html: Corps HTML (peut contenir {variables})
            variables: Variables globales
            
        Returns:
            Dict avec sent_count, failed_count, results
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
                personalized_subject = personalized_subject.replace(placeholder, str(value or ''))
                personalized_body = personalized_body.replace(placeholder, str(value or ''))
            
            # Remplacer les variables globales
            if variables:
                for key, value in variables.items():
                    placeholder = f"{{{key}}}"
                    personalized_subject = personalized_subject.replace(placeholder, str(value or ''))
                    personalized_body = personalized_body.replace(placeholder, str(value or ''))
            
            # Envoyer
            result = self.send_email(
                to_email=recipient['email'],
                to_name=recipient.get('name'),
                subject=personalized_subject,
                body_html=personalized_body,
            )
            
            result['recipient'] = recipient['email']
            results.append(result)
            
            if result['success']:
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
