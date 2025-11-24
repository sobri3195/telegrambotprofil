"""
Example usage of the Data Breach Analyzer components.
This demonstrates how to use the modules programmatically.
"""
from src.parsers import DataExtractor, DocumentParser
from src.analyzers import RiskAssessor, ConsistencyChecker, BehaviorAnalyzer
from src.reporters import ReportGenerator


def analyze_text_sample():
    """Analyze a sample text for demonstration."""
    
    sample_text = """
    FullName: John Doe Smith
    Email: john.doe@example.com
    Phone: +1-555-123-4567
    Address: 123 Main Street, New York, NY 10001
    Date of Birth: 1985-03-20
    Password Hash: 5f4dcc3b5aa765d61d8327deb882cf99
    Passport: A1234567
    
    Source: Database Breach 2023
    Telegram: @johndoe
    Channel: https://t.me/tech_news
    """
    
    print("=" * 80)
    print("DATA BREACH ANALYZER - EXAMPLE USAGE")
    print("=" * 80)
    print()
    
    print("1. Extracting data...")
    extractor = DataExtractor()
    extracted_data = extractor.extract_all(sample_text)
    
    print(f"   - Found {len(extracted_data['names'])} names")
    print(f"   - Found {len(extracted_data['emails'])} emails")
    print(f"   - Found {len(extracted_data['phones'])} phone numbers")
    print(f"   - Found {len(extracted_data['passwords'])} password hashes")
    print()
    
    print("2. Assessing risk...")
    risk_assessor = RiskAssessor()
    risk_assessment = risk_assessor.assess_overall_risk(extracted_data)
    
    print(f"   - Risk Level: {risk_assessment['risk_level']}")
    print(f"   - Risk Score: {risk_assessment['risk_score']}")
    print(f"   - Findings: {len(risk_assessment['findings'])} issues detected")
    print()
    
    print("3. Checking consistency...")
    consistency_checker = ConsistencyChecker()
    consistency_check = consistency_checker.check_consistency(extracted_data)
    
    print(f"   - Has Inconsistencies: {consistency_check['has_inconsistencies']}")
    print(f"   - Consistency Score: {consistency_check['consistency_score']}")
    print()
    
    print("4. Analyzing behavior...")
    behavior_analyzer = BehaviorAnalyzer()
    behavior_analysis = behavior_analyzer.analyze_behavior(extracted_data)
    
    profile = behavior_analysis['user_profile']
    print(f"   - Primary Interest: {profile.get('primary_interest', 'Unknown')}")
    print(f"   - Activity Level: {profile.get('activity_level', 'Unknown')}")
    print(f"   - Data Richness: {profile.get('data_richness', 'Unknown')}")
    print()
    
    print("5. Generating report...")
    report_generator = ReportGenerator()
    report = report_generator.generate_full_report(
        extracted_data,
        risk_assessment,
        consistency_check,
        behavior_analysis
    )
    
    print()
    print("=" * 80)
    print("GENERATED REPORT")
    print("=" * 80)
    print()
    print(report)
    print()


def analyze_file_sample():
    """Analyze a sample file for demonstration."""
    
    print("=" * 80)
    print("FILE ANALYSIS EXAMPLE")
    print("=" * 80)
    print()
    
    try:
        with open('sample_data.txt', 'rb') as f:
            file_content = f.read()
        
        print("1. Parsing document...")
        text = DocumentParser.parse_document(file_content, 'txt')
        print(f"   - Extracted {len(text)} characters")
        print()
        
        print("2. Extracting data...")
        extractor = DataExtractor()
        extracted_data = extractor.extract_all(text)
        
        print(f"   - Names: {len(extracted_data['names'])}")
        print(f"   - Emails: {len(extracted_data['emails'])}")
        print(f"   - Phones: {len(extracted_data['phones'])}")
        print(f"   - Passwords: {len(extracted_data['passwords'])}")
        print(f"   - Sources: {len(extracted_data['sources'])}")
        print()
        
        print("3. Running full analysis pipeline...")
        risk_assessor = RiskAssessor()
        consistency_checker = ConsistencyChecker()
        behavior_analyzer = BehaviorAnalyzer()
        report_generator = ReportGenerator()
        
        risk_assessment = risk_assessor.assess_overall_risk(extracted_data)
        consistency_check = consistency_checker.check_consistency(extracted_data)
        behavior_analysis = behavior_analyzer.analyze_behavior(extracted_data)
        
        report = report_generator.generate_full_report(
            extracted_data,
            risk_assessment,
            consistency_check,
            behavior_analysis
        )
        
        print()
        print("=" * 80)
        print("FULL ANALYSIS REPORT")
        print("=" * 80)
        print()
        print(report)
        
    except FileNotFoundError:
        print("❌ sample_data.txt not found. Please ensure the file exists.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == '__main__':
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "TELEGRAM DATA BREACH ANALYZER" + " " * 34 + "║")
    print("║" + " " * 20 + "Example Usage Script" + " " * 39 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    print("Choose an example to run:")
    print("1. Analyze simple text sample")
    print("2. Analyze sample_data.txt file")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    print()
    
    if choice == '1':
        analyze_text_sample()
    elif choice == '2':
        analyze_file_sample()
    else:
        print("Invalid choice. Running text sample by default...")
        analyze_text_sample()
