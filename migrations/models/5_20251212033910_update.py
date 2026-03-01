from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "instructor" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(100) NOT NULL  /* Prénom */,
    "last_name" VARCHAR(100) NOT NULL  /* Nom */,
    "email" VARCHAR(255) NOT NULL UNIQUE /* Email */,
    "phone" VARCHAR(20)   /* Téléphone */,
    "specialization" VARCHAR(100)   /* Spécialisation */,
    "bio" TEXT   /* Biographie */,
    "certifications" TEXT   /* Certifications (séparées par virgules) */,
    "years_experience" INT NOT NULL  DEFAULT 0 /* Années d'expérience */,
    "hourly_rate" VARCHAR(40)   /* Taux horaire */,
    "is_available" INT NOT NULL  DEFAULT 1 /* Disponible */,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'active' /* Statut: active, inactive, on_leave */,
    "photo_url" VARCHAR(500)   /* URL photo */,
    "notes" TEXT   /* Notes internes */
) /* Modèle Formateur */;
CREATE INDEX IF NOT EXISTS "idx_instructor_created_8869a3" ON "instructor" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_instructor_updated_7ad97c" ON "instructor" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_instructor_email_9f53db" ON "instructor" ("email");
CREATE INDEX IF NOT EXISTS "idx_instructor_status_c15d0d" ON "instructor" ("status");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "instructor";"""
