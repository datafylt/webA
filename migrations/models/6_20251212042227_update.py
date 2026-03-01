from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "notification" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "recipient_email" VARCHAR(255) NOT NULL  /* Email destinataire */,
    "recipient_name" VARCHAR(200)   /* Nom destinataire */,
    "subject" VARCHAR(255) NOT NULL  /* Sujet */,
    "body" TEXT NOT NULL  /* Corps du message */,
    "notification_type" VARCHAR(50) NOT NULL  DEFAULT 'general' /* Type de notification */,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'pending' /* Statut: pending, sent, failed, cancelled */,
    "scheduled_at" TIMESTAMP   /* Date d'envoi programmé */,
    "sent_at" TIMESTAMP   /* Date d'envoi effectif */,
    "error_message" TEXT   /* Message d'erreur si échec */,
    "student_id" BIGINT REFERENCES "student" ("id") ON DELETE SET NULL,
    "template_id" BIGINT REFERENCES "notification_template" ("id") ON DELETE SET NULL
) /* Modèle Notification envoyée */;
CREATE INDEX IF NOT EXISTS "idx_notificatio_created_0db009" ON "notification" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_notificatio_updated_91411c" ON "notification" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_notificatio_recipie_cbbf8c" ON "notification" ("recipient_email");
CREATE INDEX IF NOT EXISTS "idx_notificatio_status_e94356" ON "notification" ("status");
        CREATE TABLE IF NOT EXISTS "notification_template" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL UNIQUE /* Nom du template */,
    "subject" VARCHAR(255) NOT NULL  /* Sujet de l'email */,
    "body" TEXT NOT NULL  /* Corps du message (HTML supporté) */,
    "notification_type" VARCHAR(50) NOT NULL  DEFAULT 'general' /* Type: general, reminder, confirmation, invoice, welcome */,
    "variables" TEXT   /* Variables disponibles: {student_name}, {session_date}, etc. */,
    "is_active" INT NOT NULL  DEFAULT 1 /* Template actif */
) /* Modèle Template de notification */;
CREATE INDEX IF NOT EXISTS "idx_notificatio_created_00143a" ON "notification_template" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_notificatio_updated_3925db" ON "notification_template" ("updated_at");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "notification_template";
        DROP TABLE IF EXISTS "notification";"""
