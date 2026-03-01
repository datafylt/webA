-- Migration: Add Notification tables
-- Date: 2024-12-10
-- Description: Create notification tables for Formation Électro

-- Template table
CREATE TABLE IF NOT EXISTS notification_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL UNIQUE,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'general',
    variables TEXT,
    is_active BOOLEAN DEFAULT 1
);

-- Notification table
CREATE TABLE IF NOT EXISTS notification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recipient_email VARCHAR(255) NOT NULL,
    recipient_name VARCHAR(200),
    student_id INTEGER REFERENCES student(id) ON DELETE SET NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'general',
    template_id INTEGER REFERENCES notification_template(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    scheduled_at TIMESTAMP,
    sent_at TIMESTAMP,
    error_message TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_notification_recipient ON notification(recipient_email);
CREATE INDEX IF NOT EXISTS idx_notification_status ON notification(status);
CREATE INDEX IF NOT EXISTS idx_notification_type ON notification(notification_type);
CREATE INDEX IF NOT EXISTS idx_notification_student ON notification(student_id);

-- Insert sample templates
INSERT INTO notification_template (name, subject, body, notification_type, variables, is_active) VALUES
('Bienvenue', 'Bienvenue chez Formation Électro!', '<h2>Bonjour {student_name}!</h2><p>Bienvenue chez Formation Électro. Nous sommes ravis de vous compter parmi nos étudiants.</p><p>N''hésitez pas à nous contacter si vous avez des questions.</p><p>L''équipe Formation Électro</p>', 'welcome', '{student_name}, {first_name}, {last_name}, {email}', 1),
('Rappel de session', 'Rappel: Votre session approche!', '<h2>Bonjour {student_name}!</h2><p>Nous vous rappelons que votre session de formation approche.</p><p><strong>Date:</strong> {session_date}<br><strong>Lieu:</strong> {session_location}</p><p>À bientôt!</p>', 'reminder', '{student_name}, {session_date}, {session_location}, {session_title}', 1),
('Confirmation d''inscription', 'Confirmation de votre inscription', '<h2>Bonjour {student_name}!</h2><p>Votre inscription à la session <strong>{session_title}</strong> a été confirmée.</p><p><strong>Date:</strong> {session_date}<br><strong>Lieu:</strong> {session_location}</p><p>Merci de votre confiance!</p>', 'confirmation', '{student_name}, {session_title}, {session_date}, {session_location}', 1),
('Facture', 'Votre facture Formation Électro', '<h2>Bonjour {student_name}!</h2><p>Veuillez trouver ci-joint votre facture.</p><p><strong>Numéro:</strong> {invoice_number}<br><strong>Montant:</strong> {invoice_total}</p><p>Merci!</p>', 'invoice', '{student_name}, {invoice_number}, {invoice_total}', 1);

-- Insert sample notifications
INSERT INTO notification (recipient_email, recipient_name, student_id, subject, body, notification_type, status, sent_at) VALUES
('jean.tremblay@email.com', 'Jean Tremblay', 1, 'Bienvenue chez Formation Électro!', '<h2>Bonjour Jean Tremblay!</h2><p>Bienvenue chez Formation Électro.</p>', 'welcome', 'sent', '2025-01-05 10:00:00'),
('marie.lavoie@email.com', 'Marie Lavoie', 2, 'Rappel: Votre session approche!', '<h2>Bonjour Marie Lavoie!</h2><p>Votre session approche.</p>', 'reminder', 'sent', '2025-01-14 09:00:00'),
('pierre.gagnon@email.com', 'Pierre Gagnon', 3, 'Confirmation de votre inscription', '<h2>Bonjour Pierre Gagnon!</h2><p>Votre inscription est confirmée.</p>', 'confirmation', 'pending', NULL);
