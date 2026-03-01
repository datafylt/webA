from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "session" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(200) NOT NULL  /* Titre de la session */,
    "description" TEXT   /* Description\/notes */,
    "start_date" DATE NOT NULL  /* Date de début */,
    "end_date" DATE   /* Date de fin */,
    "start_time" TIME   /* Heure de début */,
    "end_time" TIME   /* Heure de fin */,
    "location_type" VARCHAR(20) NOT NULL  DEFAULT 'in_person' /* Type: in_person, online, hybrid */,
    "location" VARCHAR(200)   /* Lieu physique */,
    "online_link" VARCHAR(500)   /* Lien Zoom\/Teams */,
    "max_participants" INT NOT NULL  DEFAULT 15 /* Places maximum */,
    "min_participants" INT NOT NULL  DEFAULT 1 /* Places minimum */,
    "price" VARCHAR(40)   /* Prix (null = prix du programme) */,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'scheduled' /* Statut: scheduled, in_progress, completed, cancelled */,
    "instructor_name" VARCHAR(100)   /* Nom du formateur */,
    "program_id" BIGINT NOT NULL REFERENCES "program" ("id") ON DELETE CASCADE /* Programme associé */
) /* Modèle Session de formation (cours planifié) */;
CREATE INDEX IF NOT EXISTS "idx_session_created_493c4e" ON "session" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_session_updated_be50f2" ON "session" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_session_title_c15e08" ON "session" ("title");
CREATE INDEX IF NOT EXISTS "idx_session_start_d_92a262" ON "session" ("start_date");
CREATE INDEX IF NOT EXISTS "idx_session_status_d62a4a" ON "session" ("status");
        CREATE TABLE IF NOT EXISTS "session_enrollment" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'enrolled' /* Statut: enrolled, completed, cancelled, no_show */,
    "payment_status" VARCHAR(20) NOT NULL  DEFAULT 'pending' /* Paiement: pending, paid, refunded */,
    "amount_paid" VARCHAR(40) NOT NULL  DEFAULT '0',
    "notes" TEXT,
    "enrolled_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "session_id" BIGINT NOT NULL REFERENCES "session" ("id") ON DELETE CASCADE,
    "student_id" BIGINT NOT NULL REFERENCES "student" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_session_enr_session_e8e465" UNIQUE ("session_id", "student_id")
) /* Inscription d'un étudiant à une session */;
CREATE INDEX IF NOT EXISTS "idx_session_enr_created_124ed8" ON "session_enrollment" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_session_enr_updated_85dc79" ON "session_enrollment" ("updated_at");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "session";
        DROP TABLE IF EXISTS "session_enrollment";"""
