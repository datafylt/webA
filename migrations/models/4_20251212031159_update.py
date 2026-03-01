from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "invoice" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "invoice_number" VARCHAR(50) NOT NULL UNIQUE /* Numéro de facture */,
    "subtotal" VARCHAR(40) NOT NULL  DEFAULT '0' /* Sous-total */,
    "tax_tps" VARCHAR(40) NOT NULL  DEFAULT '0' /* TPS (5%) */,
    "tax_tvq" VARCHAR(40) NOT NULL  DEFAULT '0' /* TVQ (9.975%) */,
    "total" VARCHAR(40) NOT NULL  DEFAULT '0' /* Total */,
    "amount_paid" VARCHAR(40) NOT NULL  DEFAULT '0' /* Montant payé */,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'draft' /* Statut: draft, sent, paid, partial, overdue, cancelled */,
    "issue_date" DATE NOT NULL  /* Date d'émission */,
    "due_date" DATE   /* Date d'échéance */,
    "paid_date" DATE   /* Date de paiement */,
    "description" TEXT   /* Description\/notes */,
    "payment_method" VARCHAR(50)   /* Méthode: cash, check, credit_card, transfer, interac */,
    "session_id" BIGINT REFERENCES "session" ("id") ON DELETE SET NULL /* Session associée (optionnel) */,
    "student_id" BIGINT NOT NULL REFERENCES "student" ("id") ON DELETE CASCADE /* Étudiant facturé */
) /* Modèle Facture */;
CREATE INDEX IF NOT EXISTS "idx_invoice_created_487435" ON "invoice" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_invoice_updated_c289e0" ON "invoice" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_invoice_invoice_b4bf31" ON "invoice" ("invoice_number");
CREATE INDEX IF NOT EXISTS "idx_invoice_status_c656d0" ON "invoice" ("status");
        CREATE TABLE IF NOT EXISTS "payment" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "amount" VARCHAR(40) NOT NULL  /* Montant payé */,
    "payment_date" DATE NOT NULL  /* Date du paiement */,
    "payment_method" VARCHAR(50) NOT NULL  /* Méthode de paiement */,
    "reference" VARCHAR(100)   /* Référence\/numéro chèque */,
    "notes" TEXT   /* Notes */,
    "invoice_id" BIGINT NOT NULL REFERENCES "invoice" ("id") ON DELETE CASCADE
) /* Modèle Paiement (historique des paiements sur une facture) */;
CREATE INDEX IF NOT EXISTS "idx_payment_created_d56029" ON "payment" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_payment_updated_e40f62" ON "payment" ("updated_at");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "payment";
        DROP TABLE IF EXISTS "invoice";"""
