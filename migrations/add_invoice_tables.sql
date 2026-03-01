-- Migration: Add Invoice and Payment tables
-- Date: 2024-12-10
-- Description: Create invoice tables for Formation Électro

-- Invoice table
CREATE TABLE IF NOT EXISTS invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    student_id INTEGER NOT NULL REFERENCES student(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES session(id) ON DELETE SET NULL,
    subtotal DECIMAL(10, 2) DEFAULT 0,
    tax_tps DECIMAL(10, 2) DEFAULT 0,
    tax_tvq DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) DEFAULT 0,
    amount_paid DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft',
    issue_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    paid_date DATE,
    description TEXT,
    payment_method VARCHAR(50)
);

-- Payment table
CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    invoice_id INTEGER NOT NULL REFERENCES invoice(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE DEFAULT CURRENT_DATE,
    payment_method VARCHAR(50) NOT NULL,
    reference VARCHAR(100),
    notes TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_invoice_number ON invoice(invoice_number);
CREATE INDEX IF NOT EXISTS idx_invoice_student_id ON invoice(student_id);
CREATE INDEX IF NOT EXISTS idx_invoice_status ON invoice(status);
CREATE INDEX IF NOT EXISTS idx_invoice_issue_date ON invoice(issue_date);
CREATE INDEX IF NOT EXISTS idx_payment_invoice_id ON payment(invoice_id);

-- Insert sample invoices
INSERT INTO invoice (invoice_number, student_id, session_id, subtotal, tax_tps, tax_tvq, total, amount_paid, status, issue_date, due_date, description) VALUES
('FE-202501-0001', 1, 1, 450.00, 22.50, 44.89, 517.39, 517.39, 'paid', '2025-01-10', '2025-01-25', 'Formation Licence C - Session Janvier 2025'),
('FE-202501-0002', 2, 1, 450.00, 22.50, 44.89, 517.39, 0.00, 'sent', '2025-01-10', '2025-01-25', 'Formation Licence C - Session Janvier 2025'),
('FE-202501-0003', 3, 1, 450.00, 22.50, 44.89, 517.39, 517.39, 'paid', '2025-01-10', '2025-01-25', 'Formation Licence C - Session Janvier 2025'),
('FE-202501-0004', 5, 3, 350.00, 17.50, 34.91, 402.41, 200.00, 'partial', '2025-01-15', '2025-01-30', 'Formation RCA - Session Janvier 2025');

-- Insert sample payments
INSERT INTO payment (invoice_id, amount, payment_date, payment_method, reference) VALUES
(1, 517.39, '2025-01-10', 'credit_card', 'VISA-1234'),
(3, 517.39, '2025-01-12', 'interac', 'INT-5678'),
(4, 200.00, '2025-01-15', 'cash', NULL);
