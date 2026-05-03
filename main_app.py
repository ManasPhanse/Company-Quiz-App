# ================================================
# MODULE 3: main_app.py  (Run this file!)
# ================================================
from classes_objects import BRsData, CompaniesInfo, QuestionAnswer
from data_connector import DatabaseConnector
import sys

def main():
    print("=== COMPANY SPECIFIC QUIZ APP (MySQL + RLS) ===")
    print("Follows your exact Flow Chart + Pseudo Code\n")
    
    # === Database Connection ===
    db = DatabaseConnector()   # ←←← CHANGE credentials here if needed
    
    # === Load 5 BRs from database (as per your SQL) ===
    print("Loading 5 BRs from database...")
    brs_rules = db.get_brs()
    for rule in brs_rules:
        print(f"   • {rule}")
    print()
    
    # === Business Rules Class (validation) ===
    brs_validator = BRsData()
    
    # === Input Company (exactly as in your pseudo code) ===
    company_input = input("Enter Company: ").strip()
    if not brs_validator.validate_company(company_input):
        print("Error: Invalid company name (BR1 violated)")
        db.close()
        sys.exit(1)
    
    # === Get/Create Company ID (secure) ===
    company_id = db.get_or_create_company(company_input)
    company = CompaniesInfo(company_input)
    print(f"\nGenerating questions for {company}...\n")
    
    # === Question Templates (exactly as in your pseudo code) ===
    templates = [
        "Q1: $Company$ CEO",
        "Q2: $Company$ Profit",
        "Q3: $Company$ Revenue",
        "Q4: $Company$ Founder",
        "Q5: $Company$ Headquarters",
        "Q6: $Company$ Number of Employees",
        "Q7: $Company$ Year Founded",
        "Q8: $Company$ Main Product/Service",
        "Q9: $Company$ Industry",
        "Q10: $Company$ Policy"
    ]
    
    ques = [q.replace("$Company$", company.name) for q in templates]
    
    # === Collect Answers (exactly as in your pseudo code flow) ===
    ans = []
    print("Enter your answers one by one:\n")
    for i, q in enumerate(ques, 1):
        answer = input(f"   {q}: ").strip()
        if not answer:
            print("Error: Blank answer not allowed (BR2 violated)")
            db.close()
            sys.exit(1)
        ans.append(answer)
    
    # === Create QuestionAnswer object ===
    qa = QuestionAnswer(company_input, ques, ans)
    
    # === Display & Save to MySQL ===
    qa.display_quiz()
    qa.save_to_db(db, company_id)   # Secure RLS save
    
    print("🎉 Quiz completed successfully and saved to database!")
    db.close()


if __name__ == "__main__":
    main()