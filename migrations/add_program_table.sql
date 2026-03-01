-- Migration: Add Program table
-- Date: 2024-12-10
-- Description: Create program table for Formation Électro

CREATE TABLE IF NOT EXISTS program (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    duration_hours INTEGER DEFAULT 30,
    price DECIMAL(10, 2) DEFAULT 0,
    exam_type VARCHAR(50),
    is_active INTEGER DEFAULT 1,
    color VARCHAR(20) DEFAULT '#0277BC',
    icon VARCHAR(50) DEFAULT 'mdi:book-education',
    display_order INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_program_code ON program(code);
CREATE INDEX IF NOT EXISTS idx_program_is_active ON program(is_active);
CREATE INDEX IF NOT EXISTS idx_program_name ON program(name);

-- Insert default programs
INSERT INTO program (name, code, description, duration_hours, price, exam_type, is_active, color, icon, display_order) VALUES
('Licence C - Compagnon Électricien', 'licence_c', 'Préparation complète à l''examen de qualification pour l''obtention de la Licence C d''Emploi-Québec.', 30, 450.00, 'emploi_quebec', 1, '#0277BC', 'mdi:lightning-bolt', 1),
('RCA - Connexions Restreintes', 'rca', 'Formation pour l''obtention du certificat de Raccordement et Connexions d''Appareillage électrique.', 20, 350.00, 'emploi_quebec', 1, '#4CAF50', 'mdi:tools', 2),
('RBQ - Constructeur Propriétaire', 'rbq', 'Préparation aux examens de la RBQ pour les constructeurs-propriétaires.', 25, 400.00, 'rbq', 1, '#FF9800', 'mdi:home-city', 3),
('CMEQ - Entrepreneur Électricien', 'cmeq', 'Formation préparatoire aux examens de la Corporation des maîtres électriciens du Québec.', 35, 550.00, 'cmeq', 1, '#9C27B0', 'mdi:office-building-marker', 4),
('Sceau Rouge - Interprovincial', 'sceau_rouge', 'Préparation à l''examen interprovincial Sceau Rouge pour électriciens.', 40, 500.00, 'sceau_rouge', 1, '#F44336', 'mdi:certificate', 5),
('Formation sur mesure', 'custom', 'Programmes personnalisés adaptés aux besoins spécifiques des entreprises et individus.', 0, 0.00, NULL, 1, '#607D8B', 'mdi:school', 6);
