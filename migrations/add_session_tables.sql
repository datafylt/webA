-- Migration: Add Session and SessionEnrollment tables
-- Date: 2024-12-10
-- Description: Create session tables for Formation Électro

-- Session table
CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    program_id INTEGER NOT NULL REFERENCES program(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    start_time TIME,
    end_time TIME,
    location_type VARCHAR(20) DEFAULT 'in_person',
    location VARCHAR(200),
    online_link VARCHAR(500),
    max_participants INTEGER DEFAULT 15,
    min_participants INTEGER DEFAULT 1,
    price DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'scheduled',
    instructor_name VARCHAR(100)
);

-- Session Enrollment table
CREATE TABLE IF NOT EXISTS session_enrollment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    session_id INTEGER NOT NULL REFERENCES session(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES student(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'enrolled',
    payment_status VARCHAR(20) DEFAULT 'pending',
    amount_paid DECIMAL(10, 2) DEFAULT 0,
    notes TEXT,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, student_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_session_program_id ON session(program_id);
CREATE INDEX IF NOT EXISTS idx_session_start_date ON session(start_date);
CREATE INDEX IF NOT EXISTS idx_session_status ON session(status);
CREATE INDEX IF NOT EXISTS idx_session_title ON session(title);
CREATE INDEX IF NOT EXISTS idx_enrollment_session_id ON session_enrollment(session_id);
CREATE INDEX IF NOT EXISTS idx_enrollment_student_id ON session_enrollment(student_id);

-- Insert sample sessions
INSERT INTO session (program_id, title, description, start_date, end_date, start_time, end_time, location_type, location, max_participants, status, instructor_name) VALUES
(1, 'Licence C - Session Janvier 2025', 'Préparation intensive pour l''examen Licence C', '2025-01-15', '2025-01-17', '08:30', '16:30', 'in_person', '123 rue de la Formation, Montréal', 12, 'scheduled', 'Mahmad Elec'),
(1, 'Licence C - Session Février 2025', 'Préparation intensive pour l''examen Licence C', '2025-02-12', '2025-02-14', '08:30', '16:30', 'in_person', '123 rue de la Formation, Montréal', 12, 'scheduled', 'Mahmad Elec'),
(2, 'RCA - Session Janvier 2025', 'Formation RCA complète', '2025-01-20', '2025-01-21', '09:00', '17:00', 'hybrid', '123 rue de la Formation, Montréal', 15, 'scheduled', 'Yvan Formateur'),
(3, 'RBQ - Session Février 2025', 'Préparation examen RBQ', '2025-02-05', '2025-02-07', '08:30', '16:30', 'in_person', '123 rue de la Formation, Montréal', 10, 'scheduled', 'Mahmad Elec'),
(5, 'Sceau Rouge - Session Mars 2025', 'Préparation examen interprovincial', '2025-03-10', '2025-03-14', '08:00', '16:00', 'in_person', '123 rue de la Formation, Montréal', 8, 'scheduled', 'Mahmad Elec');

-- Insert sample enrollments (students 1,2,3 in first session)
INSERT INTO session_enrollment (session_id, student_id, status, payment_status, amount_paid) VALUES
(1, 1, 'enrolled', 'paid', 450.00),
(1, 2, 'enrolled', 'pending', 0.00),
(1, 3, 'enrolled', 'paid', 450.00),
(2, 4, 'enrolled', 'pending', 0.00),
(3, 5, 'enrolled', 'paid', 350.00);
