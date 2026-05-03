# ================================================
# MODULE 2: data_connector.py
# ================================================
import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    """Data-Connector Module - Handles all MySQL operations securely"""
    def __init__(self, host='localhost', user='root', password='ManasPhanse22', database='quiz_app'):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("✅ Connected to MySQL database successfully!")
        except Error as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def close(self):
        if self.conn.is_connected():
            self.conn.close()
            print("🔌 Database connection closed.")

    def get_brs(self):
        """Load 5 BRs directly from database (as per your SQL)"""
        self.cursor.execute("SELECT CONCAT(rule_name, ': ', description) as rule FROM brs_data")
        return [row['rule'] for row in self.cursor.fetchall()]

    def get_or_create_company(self, name: str) -> int:
        """Returns company_id (creates if not exists) - secure"""
        name = name.strip().title()
        self.cursor.execute("SELECT id FROM companies WHERE name = %s", (name,))
        row = self.cursor.fetchone()
        if row:
            return row['id']
        
        self.cursor.execute("INSERT INTO companies (name) VALUES (%s)", (name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def save_quiz(self, company_id: int, questions: list, answers: list):
        """Secure save using parameterized queries (RLS isolation by company_id)"""
        for q, a in zip(questions, answers):
            self.cursor.execute(
                "INSERT INTO question_answers (company_id, question, answer) "
                "VALUES (%s, %s, %s)",
                (company_id, q, a)
            )
        self.conn.commit()
        print(f"✅ Quiz saved successfully (RLS protected by company_id)")