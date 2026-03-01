-- Migration: Add Instructor table
-- Date: 2024-12-10
-- Description: Create instructor table for Formation Électro

CREATE TABLE IF NOT EXISTS instructor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    specialization VARCHAR(100),
    bio TEXT,
    certifications TEXT,
    years_experience INTEGER DEFAULT 0,
    hourly_rate DECIMAL(10, 2),
    is_available BOOLEAN DEFAULT 1,
    status VARCHAR(20) DEFAULT 'active',
    photo_url VARCHAR(500),
    notes TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_instructor_email ON instructor(email);
CREATE INDEX IF NOT EXISTS idx_instructor_status ON instructor(status);
CREATE INDEX IF NOT EXISTS idx_instructor_specialization ON instructor(specialization);

-- Insert sample instructors
INSERT INTO instructor (first_name, last_name, email, phone, specialization, bio, certifications, years_experience, hourly_rate, is_available, status) VALUES
('Mahmad', 'Électro', 'mahmad@formationelectro.ca', '514-555-0001', 'licence_c', 'Fondateur et formateur principal de Formation Électro. Plus de 25 ans d''expérience dans le domaine électrique.', 'Licence C, Sceau Rouge, Certificat d''enseignement', 25, 85.00, 1, 'active'),
('Yvan', 'Tremblay', 'yvan@formationelectro.ca', '514-555-0002', 'cmeq', 'Spécialiste en préparation aux examens CMEQ et RBQ. Expert en code de construction.', 'CMEQ, RBQ, Licence C', 18, 75.00, 1, 'active'),
('Marie', 'Gagnon', 'marie@formationelectro.ca', '514-555-0003', 'rca', 'Formatrice spécialisée en connexions restreintes et sécurité électrique.', 'RCA, Certificat SST', 12, 70.00, 1, 'active'),
('Pierre', 'Lavoie', 'pierre@formationelectro.ca', '514-555-0004', 'sceau_rouge', 'Expert en préparation à l''examen interprovincial Sceau Rouge.', 'Sceau Rouge, Licence C', 20, 80.00, 0, 'on_leave');
