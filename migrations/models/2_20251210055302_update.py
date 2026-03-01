from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "program" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL  /* Nom du programme */,
    "code" VARCHAR(50) NOT NULL UNIQUE /* Code unique */,
    "description" TEXT   /* Description du programme */,
    "duration_hours" INT NOT NULL  DEFAULT 30 /* Durée en heures */,
    "price" VARCHAR(40) NOT NULL  DEFAULT '0' /* Prix */,
    "exam_type" VARCHAR(50)   /* Type d'examen: emploi_quebec, cmeq, rbq, sceau_rouge */,
    "is_active" INT NOT NULL  DEFAULT 1 /* Programme actif */,
    "color" VARCHAR(20) NOT NULL  DEFAULT '#0277BC' /* Couleur hex */,
    "icon" VARCHAR(50) NOT NULL  DEFAULT 'mdi:book-education' /* Icône MDI */,
    "display_order" INT NOT NULL  DEFAULT 0 /* Ordre d'affichage */
) /* Modèle Programme de formation */;
CREATE INDEX IF NOT EXISTS "idx_program_created_d33d13" ON "program" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_program_updated_146e19" ON "program" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_program_name_be4352" ON "program" ("name");
CREATE INDEX IF NOT EXISTS "idx_program_code_cdaed3" ON "program" ("code");
CREATE INDEX IF NOT EXISTS "idx_program_is_acti_145e84" ON "program" ("is_active");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "program";"""
