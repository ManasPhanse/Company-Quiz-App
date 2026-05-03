# ================================================
# QUIZ APP - Modular Python + MySQL Version
# ================================================
# Exactly follows your original flow chart + pseudo code
# • 5 BRs (loaded from DB + class validation)
# • Company-specific 10 questions (using $Company$ placeholder)
# • 3 classes preserved (BRsData, CompaniesInfo, QuestionAnswer)
# • Full MySQL integration with secure parameterized queries
# • Application-level RLS security (answers isolated by company_id)
# • Divided into clean modules as requested
# • Sample data included (run once)

# ================================================
# STEP 1: Run this SQL first (setup + sample data)
# ================================================
"""
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
"""

# ================================================
# STEP 2: Install connector (one-time)
# ================================================
# pip install mysql-connector-python

# ================================================
# MODULE 1: classes_objects.py
# ================================================
# python
import sys

class BRsData:
    """Class 1: BRs data (5 Business Rules) - exactly as in your notebook"""
    def __init__(self):
        self.rules = [
            "BR1: Company name must be non-empty and at least 2 characters",
            "BR2: All 10 questions must be answered (no blank answers allowed)",
            "BR3: Answers are stored per company (isolation enforced)",
            "BR4: Questions are always company-specific using $$   Company   $$ placeholder",
            "BR5: Quiz supports exactly 10 questions (no more, no less)"
        ]
    
    def get_rules(self):
        return self.rules
    
    def validate_company(self, company: str) -> bool:
        return len(company.strip()) >= 2

class CompaniesInfo:
    """Class 2: Companies info"""
    def __init__(self, name: str):
        self.name = name.strip().title()
    
    def __str__(self):
        return f"Company: {self.name}"

class QuestionAnswer:
    """Class 3: Question Answer (RLS Security enforced at app level)"""
    def __init__(self, company: str, questions: list, answers: list):
        self.company = CompaniesInfo(company)
        self.questions = questions
        self.answers = answers
        if len(questions) != len(answers) or len(questions) != 10:
            raise ValueError("Exactly 10 questions and 10 answers required (BR5)")

    def display_quiz(self):
        print(f"\n{'='*70}")
        print(f"QUIZ FOR: {self.company}")
        print(f"{'='*70}")
        for i, (q, a) in enumerate(zip(self.questions, self.answers), 1):
            print(f"Q{i}: {q}")
            print(f"   A{i}: {a}")
        print(f"{'='*70}\n")

    def save_to_db(self, db_connector, company_id: int):
        """Saves answers with full security (parameterized queries + company_id isolation)"""
        db_connector.save_quiz(company_id, self.questions, self.answers)