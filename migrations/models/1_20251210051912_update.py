from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "student" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(50) NOT NULL  /* Prénom */,
    "last_name" VARCHAR(50) NOT NULL  /* Nom de famille */,
    "email" VARCHAR(255) NOT NULL UNIQUE /* Email */,
    "phone" VARCHAR(20)   /* Téléphone */,
    "address" VARCHAR(255)   /* Adresse */,
    "city" VARCHAR(100)   /* Ville */,
    "postal_code" VARCHAR(10)   /* Code postal */,
    "employer" VARCHAR(100)   /* Employeur */,
    "ccq_number" VARCHAR(50)   /* No. Carte CCQ */,
    "apprentice_hours" INT NOT NULL  DEFAULT 0 /* Heures d'apprentissage */,
    "goal" VARCHAR(50)   /* Objectif\/Programme visé */,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'active' /* Statut */,
    "notes" TEXT   /* Notes internes */,
    "expires_at" TIMESTAMP   /* Date d'expiration accès */
) /* Modèle Étudiant pour Formation Électro */;
CREATE INDEX IF NOT EXISTS "idx_student_created_49f101" ON "student" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_student_updated_22a2c9" ON "student" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_student_first_n_549a08" ON "student" ("first_name");
CREATE INDEX IF NOT EXISTS "idx_student_last_na_fbd28c" ON "student" ("last_name");
CREATE INDEX IF NOT EXISTS "idx_student_email_e7143f" ON "student" ("email");
CREATE INDEX IF NOT EXISTS "idx_student_goal_7752aa" ON "student" ("goal");
CREATE INDEX IF NOT EXISTS "idx_student_status_9149b4" ON "student" ("status");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "student";"""
