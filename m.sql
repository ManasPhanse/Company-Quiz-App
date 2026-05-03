CREATE DATABASE IF NOT EXISTS quiz_app;
USE quiz_app;

-- Table 1: BRs data (5 Business Rules) - exactly as in your notebook
CREATE TABLE IF NOT EXISTS brs_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    description TEXT
);

INSERT IGNORE INTO brs_data (rule_name, description) VALUES
('BR1', 'Company name must be non-empty and at least 2 characters'),
('BR2', 'All 10 questions must be answered (no blank answers allowed)'),
('BR3', 'Answers are stored per company (isolation enforced)'),
('BR4', 'Questions are always company-specific using $Company$ placeholder'),
('BR5', 'Quiz supports exactly 10 questions (no more, no less)');

-- Table 2: Companies info
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table 3: Question Answers (RLS enforced at app level via company_id)
CREATE TABLE IF NOT EXISTS question_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- SAMPLE DATA (run this once - creates 5 companies instantly)
INSERT IGNORE INTO companies (name) VALUES
('Tata Motors'),
('Reliance Industries'),
('Infosys Limited'),
('HDFC Bank'),
('Adani Green Energy');

SELECT * FROM companies;