-- Migration: Add Student table
-- Date: 2024-12-10
-- Description: Create student table for Formation Électro school management

CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(10),
    employer VARCHAR(100),
    ccq_number VARCHAR(50),
    apprentice_hours INTEGER DEFAULT 0,
    goal VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    notes TEXT,
    expires_at TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_student_email ON student(email);
CREATE INDEX IF NOT EXISTS idx_student_first_name ON student(first_name);
CREATE INDEX IF NOT EXISTS idx_student_last_name ON student(last_name);
CREATE INDEX IF NOT EXISTS idx_student_status ON student(status);
CREATE INDEX IF NOT EXISTS idx_student_goal ON student(goal);
CREATE INDEX IF NOT EXISTS idx_student_created_at ON student(created_at);

-- Insert sample data for testing
INSERT INTO student (first_name, last_name, email, phone, city, goal, status, apprentice_hours) VALUES
('Jean', 'Tremblay', 'jean.tremblay@email.com', '514-555-0001', 'Montréal', 'licence_c', 'active', 2500),
('Marie', 'Dubois', 'marie.dubois@email.com', '514-555-0002', 'Laval', 'rca', 'active', 1800),
('Pierre', 'Gagnon', 'pierre.gagnon@email.com', '514-555-0003', 'Longueuil', 'rbq', 'inactive', 3200),
('Sophie', 'Roy', 'sophie.roy@email.com', '450-555-0004', 'Terrebonne', 'cmeq', 'active', 4500),
('Michel', 'Lavoie', 'michel.lavoie@email.com', '438-555-0005', 'Brossard', 'sceau_rouge', 'active', 6000);
